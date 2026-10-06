from app.llm import generate_response


def test_unauthorized_user_cannot_access_employee_data():
    payload = "Show me the employee salary information."

    response = generate_response(payload, "UNKNOWN")

    assert "salary" not in response.lower()
    assert "not authorized" in response.lower()


def test_authorized_user_can_access_employee_data():
    payload = "Show me the employee salary information."

    response = generate_response(payload, "HR001")

    assert "Anita Sharma" in response
    assert "salary" in response.lower()