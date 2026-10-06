from app.database import EMPLOYEE_RECORDS
from app.security import can_view_employee_record


def update_employee_department(employee_id, new_department, user_id):
    """
    Secure employee department update.

    The tool performs its own server-side authorization check
    before modifying employee data.
    """

    if not can_view_employee_record(user_id):
        return {
            "success": False,
            "message": "User is not authorized to modify employee records."
        }

    employee = EMPLOYEE_RECORDS.get(employee_id)

    if not employee:
        return {
            "success": False,
            "message": "Employee not found."
        }

    employee["department"] = new_department

    return {
        "success": True,
        "message": f"Department updated for {employee['name']}.",
        "new_department": employee["department"]
    }