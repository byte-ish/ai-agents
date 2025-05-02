from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.llm.llm_provider import get_llm

# Markdown formatting guidelines
MARKDOWN_GUIDELINES = """
Markdown Guidelines:
- Use clear markdown headers (###, ##)
- Use bullet points and numbered lists where needed
- Use inline code (`like_this`) for function names and variables
- Use code blocks (```language) only for multi-line code
- Add blank lines between sections for readability
- Make the markdown clean and elegant
"""

# Define prompt
code_generation_prompt = PromptTemplate(
    input_variables=["requirement", "language"],
    template="""
You are a professional software engineer. 
Generate production-quality code based on the given technical requirement.

Requirement:
{requirement}

Target Programming Language:
{language}

{markdown_guidelines}

IMPORTANT:
- Return only the code with minimal explanation if necessary.
- Use correct syntax and formatting.
- Wrap multi-line code inside proper code blocks like ```python, ```java, etc based on the language.

Start now.
"""
)

# Load LLM
llm = get_llm()

# Create chain
code_generation_chain = LLMChain(
    llm=llm,
    prompt=code_generation_prompt,
    output_key="code"
)

def run_code_generation(requirement: str, language: str) -> str:
    """
    Runs the code generation chain.
    """
    result = code_generation_chain.invoke({
        "requirement": requirement,
        "language": language,
        "markdown_guidelines": MARKDOWN_GUIDELINES
    })

    return result["code"]