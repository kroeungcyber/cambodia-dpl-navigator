from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Cambodia DPL Navigator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
