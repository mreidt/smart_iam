from behave import given, then

from apps.account.models import AccountProducts, IAMAccount
from apps.account.serializers import IAMAccountSerializer
from apps.products.models import Products
from apps.products.serializers import ProductSerializer


@given("I have valid account_product data to create an instance")
def step_given_have_valid_account_product_data_to_create_instance(context):
    context.request_data = {
        "account": context.account.id,
        "product": context.product.id,
    }


@then("I should get the created account_product data in the response")
def step_then_should_get_created_account_product_in_response(context):
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.id = response_data["id"]
    expected_response_data = {
        "id": context.id,
        "account": context.account.id,
        "product": context.product.id,
        "is_active": True,
        "is_deleted": False,
    }
    context.test.assertEqual(response_data, expected_response_data)


@then("I should have the new account_product created with provided data in database")
def step_then_should_have_new_account_product_created_database(context):
    account_product_data = context.response.json()
    context.instance = AccountProducts.objects.get(id=account_product_data["id"])
    account_id = account_product_data.pop("account")
    context.test.assertEqual(context.account.id, account_id)
    product_id = account_product_data.pop("product")
    context.test.assertEqual(context.product.id, product_id)
    for key, value in account_product_data.items():
        context.test.assertEqual(getattr(context.instance, key), value)


@given("AccountProducts has required fields")
def step_given_account_product_has_required_fields(context):
    context.required_fields = ["account", "product"]


@given("I have account_product data without required fields to create an instance")
def step_given_have_account_product_data_without_required_fields(context):
    context.request_data = {}


@then("No account_product must be created in database")
def step_then_no_account_product_must_be_created_database(context):
    context.test.assertFalse(AccountProducts.objects.all().exists())


@given('I have an account_product with id "{id}"')
def step_given_have_account_product_with_id(context, id):
    context.account = IAMAccount.objects.create(email="new_account2@email.com")
    context.product = Products.objects.create(name="product_test")
    account_product = AccountProducts()
    account_product.account = context.account
    account_product.product = context.product
    account_product.id = int(id)
    account_product.save()
    context.account_product = account_product


@then('The account_product with id "{id}" should exists')
def step_account_product_with_id_should_exists(context, id):
    context.test.assertTrue(AccountProducts.objects.filter(id=int(id)).exists())


@then("I should get the details of the account_product in response")
def step_then_should_get_details_of_account_product_response(context):
    response_data = context.response.json()
    context.test.assertEqual(context.account_product.id, response_data.get("id"))
    context.test.assertEqual(
        ProductSerializer(context.product).data, response_data.get("product")
    )
    context.test.assertEqual(
        IAMAccountSerializer(context.account).data, response_data.get("account")
    )
    context.test.assertEqual(context.account.is_active, response_data.get("is_active"))
    context.test.assertEqual(
        context.account.is_deleted, response_data.get("is_deleted")
    )


@given("I have some account_products")
def step_given_have_some_account_products(context):
    context.account = IAMAccount.objects.create(email="randommail@email.com")
    context.product = Products.objects.create(name="random_product")
    for _ in range(5):
        AccountProducts.objects.create(account=context.account, product=context.product)
    context.list_of_account_products = list(AccountProducts.objects.values())


@then("I should get the list of account_products in the response")
def step_then_should_get_list_account_products_in_response(context):
    response_data = context.response.json()
    expected_data = context.list_of_account_products
    context.test.assertEqual(len(expected_data), len(response_data))
    for expected_account, response_account in zip(expected_data, response_data):
        expected_account.pop("created_at")
        expected_account.pop("last_modified")
        response_account.pop("created_at")
        response_account.pop("last_modified")
        context.test.assertEqual(
            expected_account.pop("account_id"),
            response_account.pop("account").get("id"),
        )
        context.test.assertEqual(
            expected_account.pop("product_id"),
            response_account.pop("product").get("id"),
        )
