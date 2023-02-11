import io
from fastapi import FastAPI, UploadFile, File
from preprocessing import return_relevant_document_context

app = FastAPI()

@app.get("/return-poem")
def return_love_poem(file: UploadFile = File(...)):
    # TODO: Will read file & output love poem
    try:
        pdf_as_bytes = file.file.read()
        # We convert the bytes into a Streamable object of bytes
        pdf_stream = io.BytesIO(pdf_as_bytes)
        prompt, k = "inflation", 5
        relevant_document_context = return_relevant_document_context(pdf_stream, prompt, k)
    except Exception:
        return {"error": "Error uploading file"}
    finally:
        file.file.close()

    return {"Hello": "World"}