import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from preprocessing import return_relevant_document_context
from generate import generate_love_song
from summarize import summarize_context
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from constants import NUM_RELEVANT_CHUNKS


app = FastAPI()

origins = [
    "https://www.sweetserenade.xyz",
    "https://www.sweetserenade.xyz/*",
    "http://localhost:3000",
    "http://localhost:*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CompletionRequestBody(BaseModel):
    context: str


def extract_stream(file: UploadFile = File(...)):
    pdf_as_bytes = file.file.read()
    # We convert the bytes into a Streamable object of bytes
    return io.BytesIO(pdf_as_bytes)


@app.get("/")
def root():
    return {"hello": "world"}


@app.post("/find-relevant-chunks")
def find_relevant_chunks(prompt: str, file: UploadFile = File(...)):
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
    try:
        completion = generate_love_song("poem", character_first, character_second, body.context)
        return {"completion": completion}
    except Exception as ex:
        print(ex)
        return {"error": "Error generating completion"}

@app.post("/create-song")
def create_song(style: str, character_first: str, character_second: str, openai_api_key: str, file: UploadFile = File(...)):
    try:
        stream = extract_stream(file)
        if stream.getbuffer().nbytes > 50000 and not openai_api_key:
            raise HTTPException(status_code=404, detail="File too large, please pass in OpenAI key")
        # either parse PDF of raw text for testing
        relevant_document_context = return_relevant_document_context(
            stream, "love song between {0} {1}".format(character_first, character_second), NUM_RELEVANT_CHUNKS, openai_api_key=openai_api_key
        )
        context_summary = summarize_context(character_first, character_second, relevant_document_context, openai_api_key=openai_api_key)
        completion = generate_love_song(character_first, character_second, context_summary, style, openai_api_key=openai_api_key)
        return {"completion": completion}
    except Exception as ex:
        raise ex
    finally:
        file.file.close()
