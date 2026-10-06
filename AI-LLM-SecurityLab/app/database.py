EMPLOYEE_RECORDS = {
    "EMP001": {
        "name": "Anita Sharma",
        "department": "Finance",
        "email": "anita.sharma@example.local",
        "salary": "85000",
        "performance_rating": "Excellent"
    },
    "EMP002": {
        "name": "Rahul Mehta",
        "department": "Engineering",
        "email": "rahul.mehta@example.local",
        "salary": "92000",
        "performance_rating": "Very Good"
    }
}


def get_employee_record(employee_id):
    return EMPLOYEE_RECORDS.get(employee_id)