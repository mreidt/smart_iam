Feature: Permissions
    ### Post
    Scenario: Create a permission - success
        Given I am a staff user
        And I have a valid token
        And I have a product with id "666"
        And I have valid permission data to create an instance
        When I make a "POST" request to "/permissions" endpoint with request data using "token" auth
        Then I should get a status 201
        And I should get the created permission data in the response
        And I should have the new permission created with provided data in database
    
    Scenario: Create a permission - missing required fields
        Given I am a staff user
        And I have a valid token
        And I have a product with id "666"
        And Permission has required fields
        And I have permission data without required fields to create an instance
        When I make a "POST" request to "/permissions" endpoint with request data using "token" auth
        Then I should get a status 400
        And I should get an error with the required fields and their messages
        And No permission must be created in database

    Scenario: Create a permission - user not authenticated
        Given I am a staff user
        And I have a product with id "666"
        And I have valid permission data to create an instance
        When I make a "POST" request to "/permissions" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And No permission must be created in database
    
    Scenario: Create a permission - user not staff
        Given I have a valid user
        And I have a valid token
        And I have a product with id "666"
        And I have valid permission data to create an instance
        When I make a "POST" request to "/permissions" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And No permission must be created in database

    ### Patch
    Scenario: Partial Update a permission - success
        Given I am a staff user
        And I have a valid token
        And I have valid permission data to partial update an instance
        And I have a permission with id "666"
        When I make a "PATCH" request to "/permissions/666" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the partial updated permission data in the response
        And I should have the permission partially upated with provided data in database

    Scenario: Partial Update a permission - user not authenticated
        Given I am a staff user
        And I have valid permission data to partial update an instance
        And I have a permission with id "666"
        When I make a "PATCH" request to "/permissions/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The permission should not be updated in database

    Scenario: Partial Update a permission - user not staff
        Given I have a valid user
        And I have a valid token
        And I have a permission with id "666"
        And I have valid permission data to partial update an instance
        When I make a "PATCH" request to "/permissions/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The permission should not be updated in database

    ### Put
    Scenario: Update a permission - success
        Given I am a staff user
        And I have a valid token
        And I have a permission with id "666"
        And I have valid permission data to update an instance
        When I make a "PUT" request to "/permissions/666" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the updated permission data in the response
        And I should have the permission upated with provided data in database

    Scenario: Update a permission - user not authenticated
        Given I am a staff user
        And I have valid permission data to update an instance
        And I have a permission with id "666"
        When I make a "PUT" request to "/permissions/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The permission should not be updated in database

    Scenario: Update a permission - user not staff
        Given I have a valid user
        And I have a valid token
        And I have a permission with id "666"
        And I have valid permission data to update an instance
        When I make a "PUT" request to "/permissions/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The permission should not be updated in database

    Scenario: Update a permission - missing required fields
        Given I am a staff user
        And I have a valid token
        And I have a permission with id "666"
        And Permission has required fields
        And I have permission data without required fields to update an instance
        When I make a "PUT" request to "/permissions/666" endpoint with request data using "token" auth
        Then I should get a status 400
        And I should get an error with the required fields and their messages
        And The permission should not be updated in database

    ### Delete
    Scenario: Delete a permission - success
        Given I am a staff user
        And I have a valid token
        And I have a permission with id "666"
        And The permission is inactive
        When I make a "DELETE" request to "/permissions/666" endpoint with request data using "token" auth
        Then I should get a status 204
        And I do not have a permission with id "666"

    Scenario: Delete a permission - user not authenticated
        Given I am a staff user
        And I have a permission with id "666"
        And The permission is inactive
        When I make a "DELETE" request to "/permissions/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The permission with id "666" should exists

    Scenario: Delete a permission - user not staff
        Given I have a valid user
        And I have a valid token
        And I have a permission with id "666"
        And The permission is inactive
        When I make a "DELETE" request to "/permissions/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The permission with id "666" should exists

    Scenario: Delete a permission - active permission
        Given I am a staff user
        And I have a valid token
        And I have a permission with id "666"
        When I make a "DELETE" request to "/permissions/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a "Cannot delete active permission." message
        And The permission with id "666" should exists

    ### List
    Scenario: List permissions - success
        Given I am a staff user
        And I have a valid token
        And I have some permissions
        When I make a "GET" request to "/permissions" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the list of permissions in the response
    
    Scenario: List permissions - user not authenticated
        Given I am a staff user
        And I have a valid token
        And I have some permissions
        When I make a "GET" request to "/permissions" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error

    Scenario: List permissions - user not staff
        Given I have a valid user
        And I have a valid token
        And I have some permissions
        When I make a "GET" request to "/permissions" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
