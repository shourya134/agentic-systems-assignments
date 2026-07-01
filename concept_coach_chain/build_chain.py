from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser



def build_chain():
    """
    Build a chain using the provided prompt template.

    Args:
        prompt_template (ChatPromptTemplate): The prompt template to use for the chain.

    Returns:
        ChatOllama: An instance of ChatOllama configured with the provided prompt template.
    """
    # Create an instance of ChatOllama with the given prompt template
    llm = ChatOllama(model="qwen2.5-coder:7b",base_url="http://localhost:11434", temperature=1)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """you are a helpful assistant that instructs users on best coding practices for beginners."""),
         ("user","""explain{input} using {analogy_domain}"""),
         
    ])
    parser = StrOutputParser()

    # LCEL chain
    chain = prompt |llm |parser
    return chain
chain = build_chain()

results = chain.invoke(
    {"input": "How do I write a for loop in Python?",
     "analogy_domain": "building a house"})



print(results)