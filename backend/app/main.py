from fastapi import FastAPI

app = FastAPI(title="FastAPI Backend Template")


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
