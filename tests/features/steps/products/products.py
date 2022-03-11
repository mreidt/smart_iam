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
        "is_deleted": False,
        "description": None,
    }
    context.test.assertEqual(response_data, expected_response_data)


@given("I have product data without required fields to update an instance")
@given("I have product data without required fields to create an instance")
def step_given_product_data_without_required_fields(context):
    context.request_data = {}


@given("Product has required fields")
def step_given_product_has_required_fields(context):
    context.required_fields = ["name"]


@then("No product must be created in database")
def step_then_no_product_must_be_created(context):
    context.test.assertFalse(Products.objects.all().exists())


@given("I have valid product data to partial update an instance")
def step_given_have_valid_product_data_to_partial_update_instance(context):
    context.request_data = {"name": "updated product", "is_active": False}


@given('I have a product with id "{id}"')
def step_given_have_product_with_id(context, id):
    product = Products()
    product.name = "update this product"
    product.id = int(id)
    product.save()
    context.product = product


@then("I should have the product upated with provided data in database")
def step_then_should_have_product_updated_in_database(context):
    product = Products.objects.all().first()
    context.test.assertEqual(product.name, context.request_data.get("name"))
    context.test.assertEqual(product.is_active, context.request_data.get("is_active"))


@then("The product should not be updated in database")
def step_then_product_should_not_updated_database(context):
    product = Products.objects.all().first()
    context.test.assertEqual(context.product, product)


@given("I have valid product data to update an instance")
def step_given_have_valid_product_data_to_update_instance(context):
    context.request_data = {
        "name": "updated product",
        "is_active": False,
        "is_deleted": False,
        "description": "some text",
    }


@given("The product is inactive")
def step_given_product_is_inactive(context):
    context.product.is_active = False
    context.product.save()


@then('I do not have a product with id "{id}"')
def step_then_do_not_exist_product_with_id(context, id):
    context.test.assertFalse(Products.objects.filter(id=int(id)).exists())


@then('The product with id "{id}" should exists')
def step_then_product_with_id_should_exists(context, id):
    context.test.assertTrue(Products.objects.filter(id=int(id)).exists())


@given(u'I have some products')
def step_have_some_products(context):
    for product in range (5):
        Products.objects.create(name=f"product_{product}")
    context.list_of_products = list(Products.objects.values())


@then(u'I should get the list of products in the response')
def step_should_get_list_products_response(context):
    response_data = context.response.json()
    expected_data = context.list_of_products
    context.test.assertEqual(len(expected_data), len(response_data))
    for expected_product, response_product in zip(expected_data, response_data):
        expected_product.pop("created_at")
        expected_product.pop("last_modified")
        response_product.pop("created_at")
        response_product.pop("last_modified")
        context.test.assertEqual(expected_product, response_product)


@then("I should get the partial updated product data in the response")
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


@then("I should get the updated product data in the response")
def step_then_should_get_updated_data_in_response(context):
    expected_response_data = {
        **context.request_data,
        "id": int(context.product.id),
    }
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.test.assertDictEqual(response_data, expected_response_data)
