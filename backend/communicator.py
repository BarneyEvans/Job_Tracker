from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from your frontend (adjust the origin as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/data")
async def receive_data(request: Request):
    """
    Receives a POST request from the frontend with a JWT in the Authorization header.
    Returns the token so it can later be used for backend Supabase access.
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # Extract JWT token from "Bearer <token>"
    token = auth_header.split(" ")[1]

    # (Optional) read body if you expect extra info
    data = await request.json()
    print("Received token:", token)
    # For now, just return the token and any data sent
    return {
        "message": "Token received successfully",
        "token": token,
        "received_data": data,
    }



