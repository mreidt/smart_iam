from behave import given, then

from apps.products.models import Products


@given("I have valid product data to create an instance")
def step_given_valid_product_data(context):
    context.request_data = {"name": "test_product"}


@then("I should have the new product created with provided data in database")
def then_step_validate_created_product(context):
    product_data = context.response.json()
    context.instance = Products.objects.get(id=product_data["id"])
    for key, value in product_data.items():
        context.test.assertEqual(getattr(context.instance, key), value)


@then("I should get the created product data in the response")
def then_step_get_created_product_data_response(context):
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.id = response_data["id"]
    expected_response_data = {
        "id": context.id,
        "name": "test_product",
        "is_active": True,
    }
    context.test.assertEqual(response_data, expected_response_data)


@given("I have product data without required fields to create an instance")
def step_given_product_data_without_required_fields(context):
    context.request_data = {}


@given("Product has required fields")
def step_given_product_has_required_fields(context):
    context.required_fields = ["name"]


@then("No product must be created in database")
def step_then_no_product_must_be_created(context):
    context.test.assertFalse(Products.objects.all().exists())
