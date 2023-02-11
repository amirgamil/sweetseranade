import io
from fastapi import FastAPI, UploadFile, File
from preprocessing import return_relevant_document_context
from constants import NUM_RELEVANT_CHUNKS

app = FastAPI()

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
        relevant_document_context = return_relevant_document_context(pdf_stream, prompt, NUM_RELEVANT_CHUNKS)
        return {
            "relevant_document_context": relevant_document_context
        }
    except Exception:
        return {"error": "Error uploading file"}
    finally:
        file.file.close()