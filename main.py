import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_rates_router, aggregated_market_rates_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_rates_router.router)
app.include_router(aggregated_market_rates_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)