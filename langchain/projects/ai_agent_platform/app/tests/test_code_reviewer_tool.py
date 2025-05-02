from app.tools.code_reviewer_tool import code_review_tool

def test_code_review_tool():
    sample_code = "def foo():\n    pass"
    result = code_review_tool.invoke(sample_code)

    assert "FINAL REVIEWED CODE" in result
    assert "foo" in result
