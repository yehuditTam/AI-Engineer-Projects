from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)
from llama_index.core import VectorStoreIndex
import json
import os
import cohere


class RoutingEvent(Event):
    query: str
    route_type: str


class RetrievalEvent(Event):
    query: str
    route_type: str
    retrieved_data: str


class RAGWorkflow(Workflow):
    def __init__(self, vector_index: VectorStoreIndex, structured_data: dict):
        super().__init__()
        self.vector_index = vector_index
        self.structured_data = structured_data
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

    @step
    async def route_query(self, ev: StartEvent) -> RoutingEvent:
        """Router: classify query as semantic or structured"""
        query = ev.query
        
        # Simple rule-based routing
        keywords_structured = ["רשימה", "תאריך", "השווה", "כל", "מה השתנה", "list", "date"]
        route_type = "structured" if any(k in query.lower() for k in keywords_structured) else "semantic"
        
        return RoutingEvent(query=query, route_type=route_type)

    @step
    async def retrieve_data(self, ev: RoutingEvent) -> RetrievalEvent:
        """Retrieval: fetch from vector store or structured data"""
        if ev.route_type == "semantic":
            # Vector search
            query_engine = self.vector_index.as_query_engine()
            response = await query_engine.aquery(ev.query)
            retrieved = str(response)
        else:
            # Structured JSON
            retrieved = json.dumps(self.structured_data, ensure_ascii=False, indent=2)
        
        return RetrievalEvent(
            query=ev.query,
            route_type=ev.route_type,
            retrieved_data=retrieved
        )

    @step
    async def synthesize_response(self, ev: RetrievalEvent) -> StopEvent:
        """Synthesis: combine retrieved data into natural answer"""
        response = self.co.chat(
            message=f"Query: {ev.query}\n\nContext:\n{ev.retrieved_data}\n\nProvide a clear answer in Hebrew.",
            model="command-r-08-2024"
        )
        return StopEvent(result=response.text)
