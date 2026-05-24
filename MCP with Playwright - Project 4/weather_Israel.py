import html
import re
import os
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Browser, Page
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WeatherIsrael")

# דפדפן גלובלי שנשאר פתוח בין הכלים
_playwright = None
_browser: Browser = None
_page: Page = None


async def _get_page() -> Page:
    global _playwright, _browser, _page
    if _page is None:
        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(headless=True)
        _page = await _browser.new_page()
    return _page


@mcp.tool()
async def open_weather_forecast_israel() -> str:
    """Navigate to the Israeli weather forecast site (weather2day.co.il)."""
    try:
        page = await _get_page()
        await page.goto("https://www.weather2day.co.il/forecast", timeout=15000)
        await page.wait_for_selector("#city_search", state="attached", timeout=10000)
        return "Weather site loaded successfully."
    except Exception as e:
        return f"FAIL: {e}"


@mcp.tool()
async def enter_weather_forecast_city_israel(city: str) -> str:
    """Type a city name into the weather search field.

    Args:
        city: Name of the Israeli city (e.g. תל אביב, ירושלים, חיפה)
    """
    try:
        page = await _get_page()
        await page.evaluate("document.getElementById('city_search').value = ''")
        await page.evaluate(f"document.getElementById('city_search').value = '{city}'")
        await page.evaluate("document.getElementById('city_search').dispatchEvent(new Event('input', {bubbles: true}))")
        await page.wait_for_timeout(1500)
        return f"Typed '{html.escape(city)}' into search field."
    except Exception as e:
        return f"FAIL: {e}"


@mcp.tool()
async def select_weather_forecast_city_israel() -> str:
    """Click the first city result from the search dropdown."""
    try:
        page = await _get_page()
        await page.wait_for_selector("ul li", state="attached", timeout=7000)
        await page.evaluate("""
            () => {
                const li = document.querySelector('ul li');
                if (li) li.click();
            }
        """)
        await page.wait_for_load_state("networkidle", timeout=10000)
        return "Clicked first city result."
    except Exception as e:
        return f"FAIL: {e}"


@mcp.tool()
async def extract_weather_info() -> str:
    """Extract and return the full weather forecast text from the loaded city page."""
    try:
        page = await _get_page()
        content = await page.content()

        soup = BeautifulSoup(content, "html.parser")

        parts = []
        for div_id in ["temperature-now-container", "ims-forecast-container"]:
            div = soup.find("div", {"id": div_id})
            if div:
                text = re.sub(r'\s+', ' ', div.get_text(separator=" ", strip=True))
                parts.append(text)

        if not parts:
            return "FAIL: Could not extract weather data."

        return "Weather forecast:\n" + "\n".join(parts)
    except Exception as e:
        return f"FAIL: {e}"


def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
