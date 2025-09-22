from fastapi import FastAPI

app = FastAPI(title="wgnet-agent")

@app.get("/status")
def status():
    return {"status": "ok"}
