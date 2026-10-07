from fastapi import FastAPI

app = FastAPI(title="Sentinel")

@app.get("/health")
def health_check():
    return {"status":"ok"}
