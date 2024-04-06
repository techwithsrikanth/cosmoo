from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.students import router as student_router
from database import connect_to_mongo, close_mongo_connection

app = FastAPI()
@app.on_event("startup")
async def startup_event():
    app.mongodb_client = await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection(app.mongodb_client())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router, prefix="/api/v1")
