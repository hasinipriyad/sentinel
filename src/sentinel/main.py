from fastapi import FastAPI

from sentinel.api.incidents import router as incidents_router

app = FastAPI(title="Sentinel")

@app.get("/health")
def health_check():
    return {"status":"ok"}

app.include_router(incidents_router)