from fastapi import FastAPI
from dotenv import dotenv_values
from routes import router as book_router
from neo4j_client import Neo4jClient
from models import UserNode, UserRelationship
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")
print(config.get("NEO4J_URI"))
app = FastAPI()

origins = [
    "*",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.neo4j_client = Neo4jClient(config["NEO4J_URI"], config["NEO4J_USER"], config["NEO4J_PASSWORD"])
    app.auth_service = config["AUTH_SERVICE_URL"]
    print("Neo4j connection established")
    


@app.on_event("shutdown")
def shutdown_db_client():
    app.neo4j_client.close()

app.include_router(book_router, tags=["friends"], prefix="")

if __name__ == "__main__":
    uvicorn.run(app, host="", port=8000)