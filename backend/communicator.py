from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from main import check_updates

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
    Receives a POST request from the frontend with user_id in the JSON body.
    Uses the service role key to access Supabase on behalf of that user.
    """
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id in request body")

    print("Received user_id:", user_id)

    # Call your backend function with user_id instead of token
    check_updates(user_id)

    return {
        "message": "User ID received successfully",
        "user_id": user_id,
        "received_data": data,
    }