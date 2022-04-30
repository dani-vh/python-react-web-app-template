from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"description": "An API built to interact with BIOS synchronized data."}
