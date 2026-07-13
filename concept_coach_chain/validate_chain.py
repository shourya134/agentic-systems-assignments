from build_chain import build_chain
from langchain_core.output_parsers import StrOutputParser

chain = build_chain()

results = chain.invoke(
    {"input": "How do I write a for loop in Python?",
        "analogy_domain": "building a house"})

def validatechain():
    """
    Validate the chain by checking if the output is a string.

    Returns:
        bool: True if the output is a string, False otherwise.
    """
    parser = StrOutputParser()
    output = results
    print(parser.parse(output).split())
    if parser.parse(output).strip() is None or parser.parse(output).strip() == "":
        print("Validation failed: Output is empty or None.")
        return False
    if not isinstance(parser.parse(output), str):
        print("Validation failed: Output is not a string.")
        return False
    if len(parser.parse(output).split()) > 100:
        print("Validation failed: Output is too long.")
        return False
    print(len(parser.parse(output).split()))
    return True

validatechain()