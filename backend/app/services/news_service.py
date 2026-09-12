import httpx

from app.config import settings


GNEWS_URL = "https://gnews.io/api/v4/search"


INDIAN_COMPANIES = {
    "RELIANCE.NS": "Reliance Industries",
    "RELIANCE": "Reliance Industries",

    "TCS.NS": "Tata Consultancy Services",
    "TCS": "Tata Consultancy Services",

    "INFY.NS": "Infosys",
    "INFY": "Infosys",

    "HDFCBANK.NS": "HDFC Bank",
    "HDFCBANK": "HDFC Bank",

    "ICICIBANK.NS": "ICICI Bank",
    "ICICIBANK": "ICICI Bank",

    "SBIN.NS": "State Bank of India",
    "SBIN": "State Bank of India",

    "BHARTIARTL.NS": "Bharti Airtel",
    "BHARTIARTL": "Bharti Airtel",

    "ITC.NS": "ITC Limited",
    "ITC": "ITC Limited",

    "LT.NS": "Larsen Toubro",
    "LT": "Larsen Toubro",

    "AXISBANK.NS": "Axis Bank",
    "AXISBANK": "Axis Bank",

    "TATAMOTORS.NS": "Tata Motors",
    "TATAMOTORS": "Tata Motors",

    "WIPRO.NS": "Wipro",
    "WIPRO": "Wipro",

    "HCLTECH.NS": "HCL Technologies",
    "HCLTECH": "HCL Technologies",

    "ASIANPAINT.NS": "Asian Paints",
    "ASIANPAINT": "Asian Paints",

    "HINDUNILVR.NS": "Hindustan Unilever",
    "HINDUNILVR": "Hindustan Unilever",
}


def get_company_name(symbol: str | None) -> str | None:
    if not symbol:
        return None

    clean_symbol = symbol.strip().upper()

    return INDIAN_COMPANIES.get(
        clean_symbol,
        clean_symbol.replace(".NS", "").replace(".BO", ""),
    )


async def get_market_news(
    symbol: str | None = None,
    limit: int = 20,
):
    api_key = settings.gnews_api_key

    if not api_key:
        raise ValueError(
            "GNEWS_API_KEY is not configured."
        )

    company = get_company_name(symbol)

    if company:
        query = f'"{company}" stock market'
    else:
        query = "stock market finance"

    params = {
        "q": query,
        "lang": "en",
        "country": "in",
        "max": limit,
        "sortby": "publishedAt",
        "apikey": api_key,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            GNEWS_URL,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

    if "errors" in data:
        raise ValueError(
            str(data["errors"])
        )

    articles = data.get("articles", [])

    news = []

    for article in articles:
        news.append(
            {
                "title": article.get("title"),
                "summary": article.get("description"),
                "source": (
                    article.get("source") or {}
                ).get("name"),
                "url": article.get("url"),
                "published_at": article.get(
                    "publishedAt"
                ),
                "category": "Market News",
                "tickers": [],
            }
        )

    return news