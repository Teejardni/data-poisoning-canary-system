from fastapi import FastAPI
from app.core.settings import settings

app = FastAPI(title=settings.app_name)

@app.get("/health")
async def health_check():
    """Health check"""
    from datetime import datetime
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)