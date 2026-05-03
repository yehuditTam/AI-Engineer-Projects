# 🌤️ Weather MCP Agent

An AI-powered weather agent built with [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), Claude (Anthropic), and Playwright.  
The agent can answer weather questions for both **Israel** (via web scraping) and the **USA** (via the National Weather Service API).

---

## 🏗️ Architecture

```
host.py  ←→  Claude (Anthropic)
              ├── weather_USA.py   (MCP Server — NWS REST API)
              └── weather_Israel.py (MCP Server — Playwright scraper → weather2day.co.il)
```

- **host.py** — Chat loop that connects to both MCP servers and routes tool calls via Claude
- **weather_USA.py** — MCP server with tools for US weather alerts and forecasts
- **weather_Israel.py** — MCP server that uses Playwright to scrape weather2day.co.il

---

## ⚙️ Setup

### 1. Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key → [console.anthropic.com](https://console.anthropic.com)

### 2. Install dependencies

```bash
uv sync
uv run playwright install chromium
```

### 3. Configure environment

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Run

```bash
uv run host.py
```

---

## 💬 Example Questions

```
מה מזג האוויר בתל אביב?
מה מזג האוויר בירושלים?
מה מזג האוויר בחיפה?

What are the weather alerts in California?
What is the forecast for New York? (latitude: 40.71, longitude: -74.00)
```

---

## 🛠️ Tools

### 🇮🇱 WeatherIsrael (weather_Israel.py)

| Tool | Description |
|------|-------------|
| `open_weather_forecast_israel()` | Navigates to weather2day.co.il/forecast |
| `enter_weather_forecast_city_israel(city)` | Types the city name into the search field |
| `select_weather_forecast_city_israel()` | Clicks the first result from the dropdown |
| `extract_weather_info()` | Scrapes and returns weather data from the loaded city page |

### 🇺🇸 WeatherUSA (weather_USA.py)

| Tool | Description |
|------|-------------|
| `get_alerts_in_USA(state)` | Returns active weather alerts for a US state (e.g. `CA`, `NY`) |
| `get_forecast_in_USA(latitude, longitude)` | Returns a 5-period forecast for a US location |

---

## 📦 Tech Stack

- [FastMCP](https://github.com/jlowin/fastmcp) — MCP server framework
- [Anthropic Claude](https://www.anthropic.com) — LLM with tool calling (`claude-haiku-4-5-20251001`)
- [Playwright](https://playwright.dev/python/) — Browser automation for scraping
- [httpx](https://www.python-httpx.org/) — Async HTTP client
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management
