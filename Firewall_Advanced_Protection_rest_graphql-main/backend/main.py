from fastapi import FastAPI
from pydantic import BaseModel
from middleware import APIFirewallMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter

app = FastAPI(title="API Firewall - Advanced Protection")

# Add Middleware
app.add_middleware(APIFirewallMiddleware)

# ----- REST Endpoint -----
class TestRequest(BaseModel):
    message: str

@app.post("/test")
async def test_endpoint(data: TestRequest):
    return {"received_message": data.message}

@app.get("/")
async def home():
    return {"message": "API Firewall is active and monitoring traffic."}

# ----- GraphQL Setup -----
@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return User(id=id, name="John Doe", email="john@example.com")

schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

# Mount the GraphQL route at /graphql
app.include_router(graphql_app, prefix="/graphql")
