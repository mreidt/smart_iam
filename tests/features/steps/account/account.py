from behave import given, then

from apps.account.models import IAMAccount


@given("I have valid account data to create an instance")
def step_have_valid_account_data_to_create_instance(context):
    context.request_data = {"email": "my_user@email.com"}


@then("I should get the created account data in the response")
def step_then_should_get_created_account_data_response(context):
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.id = response_data["id"]
    expected_response_data = {
        "id": context.id,
        "email": "my_user@email.com",
        "is_active": True,
        "is_deleted": False,
    }
    context.test.assertEqual(response_data, expected_response_data)


@then("I should have the new account created with provided data in database")
def step_then_should_have_account_created_database(context):
    account_data = context.response.json()
    context.instance = IAMAccount.objects.get(id=account_data["id"])
    for key, value in account_data.items():
        context.test.assertEqual(getattr(context.instance, key), value)


@given("Account has required fields")
def step_given_account_has_required_fields(context):
    context.required_fields = ["email"]


@given("I have account data without required fields to update an instance")
@given("I have account data without required fields to create an instance")
def step_have_account_data_without_required_fields(context):
    context.request_data = {}


@then("No account must be created in database")
def step_no_account_must_be_created_database(context):
    context.test.assertFalse(IAMAccount.objects.all().exists())


@given("I have valid account data to partial update an instance")
def step_have_valid_account_data_partial_update(context):
    context.request_data = {"email": "new_email@email.com"}


@given('I have an account with id "{id}"')
def step_have_account_with_id(context, id):
    account = IAMAccount()
    account.email = "account666@email.com"
    account.id = int(id)
    account.save()
    context.account = account


@then("I should get the partial updated account data in the response")
def step_should_get_partial_updated_account_in_response(context):
    expected_response_data = {
        **context.request_data,
        "is_deleted": False,
        "is_active": True,
        "id": int(context.account.id),
    }
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.test.assertDictEqual(response_data, expected_response_data)


@then("I should have the account upated with provided data in database")
def step_should_have_account_updated_in_database(context):
    account = IAMAccount.objects.all().first()
    context.test.assertEqual(account.email, context.request_data.get("email"))


@then("The account should not be updated in database")
def step_account_should_not_be_updated(context):
    account = IAMAccount.objects.all().first()
    context.test.assertEqual(context.account, account)


@given("I have valid account data to update an instance")
def step_have_valid_account_data_update(context):
    context.request_data = {
        "email": "new_email@email.com",
        "is_active": False,
        "is_deleted": False,
    }


@then("I should get the updated account data in the response")
def step_should_get_updated_account_data_in_response(context):
    expected_response_data = {
        **context.request_data,
        "id": int(context.account.id),
    }
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.test.assertDictEqual(response_data, expected_response_data)


@then('The account with id "{id}" should exists')
def step_account_with_id_should_exists(context, id):
    context.test.assertTrue(IAMAccount.objects.filter(id=int(id)).exists())


@given("I have some accounts")
def step_have_some_accounts(context):
    for account in range(5):
        IAMAccount.objects.create(email=f"email{account}@email.com")
    context.list_of_accounts = list(IAMAccount.objects.values())


@then("I should get the list of accounts in the response")
def step_should_get_list_accounts_in_response(context):
    response_data = context.response.json()
    expected_data = context.list_of_accounts
    context.test.assertEqual(len(expected_data), len(response_data))
    for expected_account, response_account in zip(expected_data, response_data):
        expected_account.pop("created_at")
        expected_account.pop("last_modified")
        response_account.pop("created_at")
        response_account.pop("last_modified")
        context.test.assertEqual(expected_account, response_account)


@then("I should get the details of the account in response")
def step_should_get_details_of_account(context):
    response_data = context.response.json()
    context.test.assertEqual(context.account.id, response_data.get("id"))
    context.test.assertEqual(context.account.email, response_data.get("email"))
    context.test.assertEqual(context.account.is_active, response_data.get("is_active"))
    context.test.assertEqual(
        context.account.is_deleted, response_data.get("is_deleted")
    )
