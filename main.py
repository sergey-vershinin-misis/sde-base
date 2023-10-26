from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return "Hello"


import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000)
