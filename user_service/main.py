from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def health():
    return {"user_service": "works"}
