from .swagger_registry import swagger_registry

def register_endpoint(
    path,
    method,
    summary="",
    tag="Default",
    auth=True,
    request_body=None,
    parameters=None,
    responses=None
):
    def decorator(func):
        swagger_registry.append({
            "path": path,
            "method": method.lower(),
            "summary": summary,
            "tag": tag,
            "auth": auth,
            "request_body": request_body,
            "parameters": parameters or [],
            "responses": responses or {},
        })
        return func
    return decorator