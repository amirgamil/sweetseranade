import io
from fastapi import FastAPI, UploadFile, File
from preprocessing import return_relevant_document_context
from generate import generate_love_song
from pydantic import BaseModel
from constants import NUM_RELEVANT_CHUNKS

app = FastAPI()


class CompletionRequestBody(BaseModel):
    context: str


@app.get("/")
def root():
    return {"hello": "world"}


@app.post("/return-poem")
def return_love_poem(prompt: str, file: UploadFile = File(...)):
    # TODO: Will read file & output love poem
    try:
        pdf_as_bytes = file.file.read()
        # We convert the bytes into a Streamable object of bytes
        pdf_stream = io.BytesIO(pdf_as_bytes)
        relevant_document_context = return_relevant_document_context(
            pdf_stream, prompt, NUM_RELEVANT_CHUNKS
        )
        return {"relevant_document_context": relevant_document_context}
    except Exception as ex:
        print(ex)
        return {"error": "Error uploading file"}
    finally:
        file.file.close()


# for intermediate testing on GPT
@app.post("/generate-love-song")
def generate_love_song_completion(
    character_first: str, character_second: str, body: CompletionRequestBody
):
    # TODO: Will read file & output love poem
    try:
        completion = generate_love_song(character_first, character_second, body.context)
        return {"completion": completion}
    except Exception as ex:
        print(ex)
        return {"error": "Error generating completion"}
