from behave import given, then

from apps.permissions.models import Permissions
from apps.products.models import Products


@given("I have valid permission data to create an instance")
def step_given_valid_permission_data_to_create_instance(context):
    context.request_data = {
        "name": "test_permission",
        "product": context.product.id,
        "description": "some permission description",
    }


@then("I should get the created permission data in the response")
def step_then_get_created_permission_data_response(context):
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.id = response_data["id"]
    expected_response_data = {
        "id": context.id,
        "name": "test_permission",
        "product": context.product.id,
        "is_active": True,
        "is_deleted": False,
        "description": "some permission description",
    }
    context.test.assertEqual(response_data, expected_response_data)


@then("I should have the new permission created with provided data in database")
def then_step_validate_created_permission(context):
    permission_data = context.response.json()
    product_id = permission_data.pop("product")
    product = Products.objects.get(id=product_id)
    permission_data["product"] = product
    context.instance = Permissions.objects.get(id=permission_data["id"])
    for key, value in permission_data.items():
        context.test.assertEqual(getattr(context.instance, key), value)


@given("I have permission data without required fields to update an instance")
@given("I have permission data without required fields to create an instance")
def step_given_permission_data_without_required_fields(context):
    context.request_data = {}


@given("Permission has required fields")
def step_given_permission_has_required_fields(context):
    context.required_fields = ["name", "product", "description"]


@then("No permission must be created in database")
def step_then_no_permission_must_be_created(context):
    context.test.assertFalse(Permissions.objects.all().exists())


@given("I have valid permission data to partial update an instance")
def step_given_have_valid_permission_data_partial_update(context):
    context.request_data = {
        "name": "test_permission_partial_update",
        "description": "changing description",
    }


@given('I have a permission with id "{id}"')
def step_given_have_permission_with_id(context, id):
    context.product = Products.objects.create(name="product_123")
    permission = Permissions()
    permission.name = "my_permission"
    permission.product = context.product
    permission.description = "short permission description"
    permission.id = int(id)
    permission.save()
    context.permission = permission


@then("I should get the partial updated permission data in the response")
def step_then_should_get_partial_updated_permission_in_response(context):
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.id = response_data["id"]
    expected_response_data = {
        "id": context.id,
        "name": "test_permission_partial_update",
        "is_active": True,
        "is_deleted": False,
        "description": "changing description",
        "product": context.product.id,
    }
    context.test.assertEqual(response_data, expected_response_data)


@then("I should have the permission partially upated with provided data in database")
def step_then_should_have_permission_partially_updated_in_database(context):
    permission = Permissions.objects.all().first()
    context.test.assertEqual(permission.name, context.request_data.get("name"))
    context.test.assertEqual(
        permission.description, context.request_data.get("description")
    )


@then("I should have the permission upated with provided data in database")
def step_then_should_have_permission_updated_in_database(context):
    permission = Permissions.objects.all().first()
    context.test.assertEqual(permission.name, context.request_data.get("name"))
    context.test.assertEqual(permission.product.id, context.request_data.get("product"))
    context.test.assertEqual(
        permission.description, context.request_data.get("description")
    )
    context.test.assertEqual(
        permission.is_active, context.request_data.get("is_active")
    )
    context.test.assertEqual(
        permission.is_deleted, context.request_data.get("is_deleted")
    )


@then("The permission should not be updated in database")
def step_then_permission_should_not_be_updated_database(context):
    permission = Permissions.objects.all().first()
    context.test.assertEqual(context.permission, permission)


@given("I have valid permission data to update an instance")
def step_given_have_valid_permission_data_update_instance(context):
    context.product = Products.objects.create(name="new_product")
    context.request_data = {
        "name": "test_permission__update",
        "product": context.product.id,
        "description": "changing description",
        "is_active": False,
        "is_deleted": True,
    }


@then("I should get the updated permission data in the response")
def step_then_should_get_updated_permission_data_in_response(context):
    response_data = context.response.json()
    response_data.pop("created_at")
    response_data.pop("last_modified")
    context.id = response_data["id"]
    expected_response_data = {
        "id": context.id,
        "name": "test_permission__update",
        "is_active": False,
        "is_deleted": True,
        "description": "changing description",
        "product": context.product.id,
    }
    context.test.assertEqual(response_data, expected_response_data)


@given("The permission is inactive")
def step_given_permission_is_inactive(context):
    context.permission.is_active = False
    context.permission.save()


@then('I do not have a permission with id "{id}"')
def step_dont_have_permission_with_id(context, id):
    context.test.assertFalse(Permissions.objects.filter(id=id).exists())


@then('The permission with id "{id}" should exists')
def step_permission_with_id_should_exists(context, id):
    context.test.assertTrue(Permissions.objects.filter(id=id).exists())


@given("I have some permissions")
def step_have_some_permissions(context):
    product = Products.objects.create(name="product_1")
    for permission in range(5):
        name = f"permission_{permission}"
        description = f"description_{permission}"
        Permissions.objects.create(name=name, description=description, product=product)
    context.list_of_permissions = list(Permissions.objects.values())


@then("I should get the list of permissions in the response")
def step_should_get_list_permissions_response(context):
    response_data = context.response.json()
    expected_data = context.list_of_permissions
    context.test.assertEqual(len(expected_data), len(response_data))
    for expected_permission, response_permission in zip(expected_data, response_data):
        expected_permission.pop("created_at")
        expected_permission.pop("last_modified")
        response_permission.pop("created_at")
        response_permission.pop("last_modified")
        expected_product_id = expected_permission.pop("product_id")
        response_product_id = response_permission.pop("product")
        context.test.assertEqual(expected_product_id, response_product_id)
        context.test.assertEqual(expected_permission, response_permission)
