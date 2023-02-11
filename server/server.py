from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def return_love_poem() -> str:
    # Will read file & output love poem
    return {"Hello": "World"}