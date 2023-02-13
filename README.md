# SweetSerenade

Generate love songs between characters in a book, article, or literally anything you can turn into a PDF document. Website here (TODO). Built by [Amir](https://twitter.com/amirbolous) & [Verumlotus](https://twitter.com/verumlotus).

## Background & Architecture
SweetSerenade is a Valentine's day hack that accepts a PDF (generated from a book, text message history, etc.), extracts relevant context from the PDF for 2 characters, and generates a love poem in any style you choose. 

Our backend server is written in python & uses [FastAPI](https://fastapi.tiangolo.com/) as the web framework. We use [PyPDF](https://pypdf2.readthedocs.io/en/3.0.0/) to parse the uploaded PDF document into text. With the text in hand, we use [NLTK](https://www.nltk.org/) to slice up the text into smaller chunks composed of complete sentences. This will allow us to identify the most relevant chunks of text with rich content about the 2 characters. We calculate the [word embeddings](https://machinelearningmastery.com/what-are-word-embeddings) for each of our chunks – the embeddings come from [OpenAI's Embedding Model](https://platform.openai.com/docs/guides/embeddings). With embeddings in hand, we compute a similarity search using [Facebook Research's FAISS library](https://github.com/facebookresearch/faiss) against a prompt including the 2 characters name in order to extract the most relevant chunks in the text. In order to capture surrounding context, we also retrieve neighboring textual chunks (the +/- 2 chunks that surround the relevant chunks we have found). We then compress this context by summarizing it while preserving detail. We then use a [few shot prompt](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00485/111728/True-Few-Shot-Learning-with-Prompts-A-Real-World) that contains the computed summary and use [GPT's Davinci model](https://platform.openai.com/docs/models/overview) to generate a love song that is returned to the user. 

For deployment, we deploy a [docker](https://www.docker.com/) container on [AWS ECS](https://aws.amazon.com/ecs/) using [Fargate](https://aws.amazon.com/fargate/) as our compute engine to autoscale compute resources depending on website load. Our container fleet sits behind an [Elastic Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) that provides SSL termination. 

![serenade](https://user-images.githubusercontent.com/97858468/218360673-ddae3f56-2bd1-4cf1-8fb6-e236b7963e46.png)

## Build
### Backend
For our backend code we use a Makefile for our build process and [Poetry](https://python-poetry.org/) as our dependency manager for Python. Install poetry, change directories into the `server` folder, and then run `poetry install` to install all dependencies. Note that we require `python 3.9.13` and that the [Rust Compiler](https://www.rust-lang.org/) must be installed on your machine in order to build certain dependencies. An OpenAI API Key is required for the project, and must be available in the environment as `OPENAI_API_KEY`. You can run `export OPENAI_API_KEY=<your key>` in your current shell or add the key to your `.zshenv` file. 

Afterwards, run `make setup` to configure your environment to run our application. To run the server run `make server`. To build a docker image for the server run `make docker-build-local`. To create a docker container based on the image run `make docker-run-local`. 

### Frontend
Our frontend is built using [React](https://reactjs.org/), [Next.js](https://nextjs.org/), and [Tailwind CSS](https://tailwindcss.com/). To run our web app locally, change directories into the `frontend` directory and run `yarn install` to install all dependencies. Then run `yarn dev`. 

## Improvements
There are many parameters to tune that could possibly lead to improved love song outputs. There is room for experimentation in all of these. We chunked the extracted PDF text into chunks of roughly size 200, and had a chunk overlap of roughly 40 characters. We find the 4 most relevant chunks via semantic search, and for each relevant chunk we also find the +/- 2 neighboring chunks in the original text. It is possible that by changing these parameters we may be able to capture richer context. One of the biggest areas of experimentation is prompt tuning[^1] in both the prompt to summarize our relevant chunks and also in the prompt to generate the love song. 

[^1]: There is ongoing research in prompt tuning. See [here](https://aclanthology.org/2021.emnlp-main.243/)

## Acknowledgement & Disclaimer
We do not make any active efforts to store the contents of the PDF you upload, character names, or the style names, but cannot fully guarantee that these values are not captured in logs in the event of an error.
