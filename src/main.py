from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from src.routes import (quotes_router, indices_router, movers_router, historical_prices_router,
                        similar_stocks_router, finance_news_router, indicators_router, search_router,
                        sectors_router, sockets_router, stream_router)
from src.session_manager import get_global_session, close_global_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_global_session()
    yield
    await close_global_session()

app = FastAPI(
    title="FinanceQuery",
    version="1.4.0",
    description="FinanceQuery is a simple API to query financial data."
                " It provides endpoints to get quotes, historical prices, indices,"
                " market movers, similar stocks, finance news, indicators, search, and sectors."
                " Please use FinanceQueryDemoAWSHT as the demo API key which is limited to 500 requests/day."
                " You are free to deploy your own instance of FinanceQuery to AWS and use your own API key."
                " If you are testing locally you can use the local server and will not need a key."
    ,
    servers=[
        {"url": "https://43pk30s7aj.execute-api.us-east-2.amazonaws.com/prod", "description": "Production server"},
        {"url": "http://127.0.0.1:8000", "description": "Local server"}
    ],
    contact={
        "name": "Harvey Tseng",
        "email": "harveytseng2@gmail.com"
    },
    license_info={
        "name": "MIT License",
        "identifier": "MIT",
    },
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (needed for Android app but should be restricted for web apps)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(quotes_router, prefix="/v1")
app.include_router(historical_prices_router, prefix="/v1")
app.include_router(indicators_router, prefix="/v1")
app.include_router(indices_router, prefix="/v1")
app.include_router(movers_router, prefix="/v1")
app.include_router(similar_stocks_router, prefix="/v1")
app.include_router(finance_news_router, prefix="/v1")
app.include_router(search_router, prefix="/v1")
app.include_router(sectors_router, prefix="/v1")
app.include_router(stream_router, prefix="/v1")
app.include_router(sockets_router)

handler = Mangum(app)