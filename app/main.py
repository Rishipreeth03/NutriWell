from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="NutriWell API",
    description="Nutrition and wellbeing recommendation system",
    version="1.0.0",
)


app.include_router(router)