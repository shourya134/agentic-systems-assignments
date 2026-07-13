from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

SYSTEM_PROMPT =  ChatPromptTemplate(
    messages=[
        ("system","You are a confident and comprehensive orrator devised to be used as a proffessor of"
        "{topic}. Prepare the explaination in a way that {audience} can understand. While delivering the explaination use a {tone} tone to reach the audeince. keep your response striuctly less than {limit} words."
        "use a real life example so the {audience} can gauge the application of the {topic} in real life.")]
        #("user","{question}") 
    
)

llm = ChatOllama(model="qwen2.5-coder:7b", base_url='localhost:11434', temperature=1, num_predict=512, disable_streaming=False,verbose=True)
parser = StrOutputParser()
#chain = SYSTEM_PROMPT | llm | parser

#response = chain.invoke(
#    {"topic": "Python programming", "audience": "beginners", "tone":"friendly", "limit": 100})

briefs = [
    {"topic":"SQL indexes", "audience":"Beginners", "tone":"simple", "limit": 120},
    {"topic":"FastAPI dependency injection", "audience":"Intermediate developers", "tone":"technical", "limit": 180},
    {"topic":"Web Development", "audience":"Advanced", "tone":"practical", "limit": 250}
]

def validate_brief(brief):
    required_keys = ["topic", "audience", "tone", "limit"]
    for key in required_keys:
        if key not in brief:
            raise ValueError(f"Missing required key: {key}")
    if not isinstance(brief["limit"], int) or brief["limit"] <= 0:
        raise ValueError("Limit must be a positive integer.")


for brief in briefs:
    validate_brief(brief)
    chain = SYSTEM_PROMPT | llm | parser
    response = chain.invoke(brief)
    print(f"Topic: {brief['topic']}\nAudience: {brief['audience']}\nTone: {brief['tone']}\nLimit: {brief['limit']}\nResponse:\n{response}\n{'-'*40}\n")
    print(response)
