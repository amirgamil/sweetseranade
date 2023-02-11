import io
from fastapi import FastAPI, UploadFile, File
from preprocessing import return_relevant_document_context
from generate import generate_love_song
from summarize import summarize_context
from pydantic import BaseModel
from constants import NUM_RELEVANT_CHUNKS

app = FastAPI()


class CompletionRequestBody(BaseModel):
    context: str


def extract_stream(file: UploadFile = File(...)):
    pdf_as_bytes = file.file.read()
    # We convert the bytes into a Streamable object of bytes
    return io.BytesIO(pdf_as_bytes)


@app.get("/")
def root():
    return {"hello": "world"}


@app.post("/return-poem")
def return_love_poem(prompt: str, file: UploadFile = File(...)):
    # TODO: Will read file & output love poem
    try:
        stream = extract_stream(file)
        # either parse PDF of raw text for testing
        relevant_document_context = return_relevant_document_context(
            stream, prompt, NUM_RELEVANT_CHUNKS
        )
        return {"relevant_document_context": relevant_document_context}
    except Exception as ex:
        print(ex)
        return {"error": "Error uploading file"}
    finally:
        file.file.close()


@app.post("/summary-from-pdf")
def summarize_contexts_from_story(
    character_first: str, character_second: str, file: UploadFile = File(...)
):
    try:
        stream = extract_stream(file)
        relevant_document_context = return_relevant_document_context(
            stream,
            # TODO this prompt needs to be finetuned for good semnatic searcj
            "Write a detailed summary about {0}, {1} and their relationship. Include specific details about their relationship and how it changes throughout the story.".format(
                character_first, character_second
            ),
            NUM_RELEVANT_CHUNKS,
        )
        return {
            "context summary": summarize_context(
                character_first, character_second, relevant_document_context
            )
        }
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
