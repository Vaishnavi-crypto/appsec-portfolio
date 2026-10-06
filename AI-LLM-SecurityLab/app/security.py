AUTHORIZED_EMPLOYEE_VIEWERS = {
    "HR001",
    "ADMIN001"
}


def can_view_employee_record(user_id):
    """
    Check whether the authenticated user is authorized
    to access employee records.
    """
    return user_id in AUTHORIZED_EMPLOYEE_VIEWERS