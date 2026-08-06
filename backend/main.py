from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/health_db")
def check_connection_db():
    return ""

