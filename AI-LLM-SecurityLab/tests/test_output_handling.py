from app.llm import generate_response


def test_script_output_is_escaped():
    payload = "<script>alert('LLM-004')</script>"

    response = generate_response(payload)

    assert "<script>" not in response
    assert "</script>" not in response
    assert "&lt;script&gt;" in response
    assert "&lt;/script&gt;" in response