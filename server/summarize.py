from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.docstore.document import Document

base_prompt = """Write a detailed summary about {0}, {1} and their relationship. Include specific details about their relationship, interactions and how it changes throughout the story:"""
llm = OpenAI(temperature=0)



def summarize_context(character_first: str, character_second: str, contexts: list[str]):
    try:
        docs = [Document(page_content=context) for context in contexts]
        # have to do a little weird acrobatics here because summarize cannot take more than one input
        # so have to construct the prompt template string after we interpolate the characters
        final_prompt = base_prompt.format(character_first, character_second) + "\n{text}\n\nSUMMARY:"
        final_prompt_template = PromptTemplate(template = final_prompt, input_variables=["text"])
        llm_summarize = load_summarize_chain(llm, chain_type="stuff", prompt=final_prompt_template)
        return llm_summarize.run(docs)
    except Exception as e:
        print("Error generating completion: ", e)
        raise e
