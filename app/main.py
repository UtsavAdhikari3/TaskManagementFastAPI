from fastapi import FastAPI

app = FastAPI(
    title="Task Management RBAC API",
    version="1.0.0",
    description="Taskmanagement API."
)


@app.get("/health")
def health_check():
    return {"status": "ok"}