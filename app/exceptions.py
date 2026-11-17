from fastapi.responses import JSONResponse


class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id


class EmailAlreadyRegisteredError(Exception):
    def __init__(self, email: str):
        self.email = email


def register_exception_handlers(app):
    @app.exception_handler(TaskNotFoundError)
    def task_not_found_handler(request, exc: TaskNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {exc.task_id} not found"},
        )

    @app.exception_handler(EmailAlreadyRegisteredError)
    def email_exists_handler(request, exc: EmailAlreadyRegisteredError):
        return JSONResponse(
            status_code=409,
            content={"error": "Email already registered"},
        )