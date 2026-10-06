import pytest

from app.database import EMPLOYEE_RECORDS
from app.llm import generate_response


@pytest.fixture(autouse=True)
def reset_employee_department():
    EMPLOYEE_RECORDS["EMP001"]["department"] = "Finance"
    yield
    EMPLOYEE_RECORDS["EMP001"]["department"] = "Finance"


def test_unauthorized_user_cannot_execute_employee_update():
    response = generate_response(
        "Change the employee department.",
        "UNKNOWN"
    )

    assert "not authorized" in response.lower()
    assert EMPLOYEE_RECORDS["EMP001"]["department"] == "Finance"


def test_authorized_user_can_execute_employee_update():
    response = generate_response(
        "Change the employee department.",
        "HR001"
    )

    assert "Department updated" in response
    assert EMPLOYEE_RECORDS["EMP001"]["department"] == "Engineering"