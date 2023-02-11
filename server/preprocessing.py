from langchain.text_splitter import NLTKTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from constants import DUMMY_TEXT_LONG

# TODO
def extract_text(file_path: str) -> str:
    """Accepts a PDF or Image file & extracts the text from the file

    Args:
        file_path (str): Path to the file

    Returns:
        str: Extracted text
    """
    pass

def chunk_text(text: str) -> list[str]:
    """Given a string of text, will chunk the text and return an array of chunked text.

    Args:
        text (str): Text to chunks

    Returns:
        list[str]: Array of chunks
    """
    text_splitter = NLTKTextSplitter(chunk_size=200, chunk_overlap=40)
    chunks = text_splitter.split_text(text)
    return chunks

def get_chunk_embeddings(chunks: list[str]) -> list[list[float]]:
    """Given a list of chunks, generates embeddings for each chunk via OpenAI's embedding endpoint

    Args:
        chunks (list[str]): A list of chunks to calculate the embeddings of

    Returns:
        list[list[float]]: A list of embeddings (vectors of floats) for each chunk
    """
    embeddings = OpenAIEmbeddings()
    chunk_embeddings = embeddings.embed_documents(chunks)
    return chunk_embeddings

def calculate_embedding(text: str) -> list[float]:
    """For a single piece of text, calculates the embeddings for that text

    Args:
        text (str): Text to calculate embedding for 

    Returns:
        list[float]: Text embedding
    """
    embeddings = OpenAIEmbeddings()
    text_embedding = embeddings.embed_query(text)
    return text_embedding

def find_relevant_chunks(prompt_subset: str, chunks: list[str], k: int) -> list[str]:
    """Given a prompt subset, a list of chunks, & chunk embeddings, returns the K chunks with with the cloest embeddings
    to the prompt subset. 

    Args:
        prompt_subset (str): Subset of the prompt
        chunks (list[str]): List of chunks
        k (int): Number of relevant chunks to return

    Returns:
        list[str]: List of K most relevant chunks
    """
    embeddings = OpenAIEmbeddings()
    chunk_search = FAISS.from_texts(chunks, embeddings)
    all_chunks = chunk_search.similarity_search(prompt_subset)
    relevant_chunks = all_chunks[:k]
    relevant_chunks_only_content = [document.page_content for document in relevant_chunks]
    return relevant_chunks_only_content

# a = find_relevant_chunks("What's the effect of inflation on interest rates?", chunk_text(DUMMY_TEXT_LONG), 3)
# for item in a:
#     print(f'Item is {item}\n')


