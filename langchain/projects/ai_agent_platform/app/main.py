from app.tools.code_reviewer_tool import code_review_tool

if __name__ == "__main__":
    sample_code = """
def process_user_input(input):
    password = "123456"
    print("Processing user input: " + input)
    if input == "admin":
        print("Access granted.")
    else:
        print("Access denied.")
"""

    result = code_review_tool.invoke(sample_code)
    print(result)