class ApiResponse:

    @staticmethod
    def success(data=None, message="Success", meta=None):
        return {
            "success": True,
            "message": message,
            "data": data or [],
            "meta": meta or {}
        }

    @staticmethod
    def error(message="Error", code=400):
        return {
            "success": False,
            "message": message,
            "code": code
        }