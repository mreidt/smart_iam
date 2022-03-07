from behave import then


@then("I should get a status {status_code}")
def then_step_get_status_code(context, status_code):
    context.test.assertEqual(context.response.status_code, int(status_code))
    return context


@then("I should get a default forbidden message")
def then_step_get_forbidden_message(context):
    expected_message = {"detail": "You do not have permission to perform this action."}
    context.test.assertEqual(context.response.json(), expected_message)


@then("I should get an error with the required fields and their messages")
def then_step_error_with_required_fields_messages(context):
    response_data = context.response.json()
    expected_response_data = {}
    for required_field in context.required_fields:
        if (
            not hasattr(context, "request_data")
            or required_field not in context.request_data
        ):
            expected_response_data[required_field] = ["This field is required."]
    context.test.assertDictEqual(response_data, expected_response_data)


@then("I should get an unauthorized error")
def step_then_should_get_unauthorized_error(context):
    expected_message = {"detail": "Authentication credentials were not provided."}
    context.test.assertEqual(context.response.json(), expected_message)


@then('I should get the partial updated product data in the response')
def step_then_should_get_partial_updated_data_in_response(context):
    expected_response_data = {
        **context.request_data,
        "is_deleted": False,
        "id": int(context.product.id),
        "description": None,
    }
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.test.assertDictEqual(response_data, expected_response_data)


@then('I should get the updated product data in the response')
def step_then_should_get_updated_data_in_response(context):
    expected_response_data = {
        **context.request_data,
        "id": int(context.product.id),
    }
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.test.assertDictEqual(response_data, expected_response_data)


@then('I should get a "{expected_message}" message')
def step_then_should_get_message(context, expected_message):
    expected_message = {"detail": expected_message}
    context.test.assertEqual(context.response.json(), expected_message)
