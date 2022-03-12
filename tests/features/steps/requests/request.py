from behave import when


@when(
    'I make a "{request_type}" request to "{endpoint}" endpoint with request data using "{auth_method}" auth'
)
def when_step_request_to_endpoint_with_auth_method(
    context, request_type, endpoint, auth_method
):
    if auth_method.lower() == "no":
        context.test.client.defaults["HTTP_AUTHORIZATION"] = ""
    elif auth_method.lower() == "token":
        context.test.client.defaults["HTTP_AUTHORIZATION"] = f"Token {context.token}"
    request_method_name = request_type.lower()
    full_path = f"/smart-iam/api{endpoint}"
    request_data = getattr(context, "request_data", {})
    request_method = getattr(context.test.client, request_method_name)
    context.response = request_method(
        full_path, request_data, content_type="application/json"
    )
