from fastapi import FastAPI, Request
import main

app = FastAPI()

@app.post("/api/data")
async def receive_functionality(request: Request):
    data = await request.json()  # read JSON sent from frontend
    action = data["action"]
    payload = data["payload"]

    if action == "sign_up":
        main.sign_up(payload["access_token"])
    elif action == "sign_in":
        main.check_updates(payload["access_token"])
    elif action == "connect_new_email":
        main.connect_email(payload)
    print("Received:", data)
    return {"status": "ok"}

