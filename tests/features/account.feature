Feature: Account
    ### Post
    Scenario: Create an Account - success
        Given I am a staff user
        And I have a valid token
        And I have valid account data to create an instance
        When I make a "POST" request to "/account" endpoint with request data using "token" auth
        Then I should get a status 201
        And I should get the created account data in the response
        And I should have the new account created with provided data in database

    Scenario: Create an Account - missing required fields
        Given I am a staff user
        And I have a valid token
        And Account has required fields
        And I have account data without required fields to create an instance
        When I make a "POST" request to "/account" endpoint with request data using "token" auth
        Then I should get a status 400
        And I should get an error with the required fields and their messages
        And No account must be created in database

    Scenario: Create an Account - user not authenticated
        Given I am a staff user
        And I have valid account data to create an instance
        When I make a "POST" request to "/account" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And No account must be created in database
    
    Scenario: Create an Account - user not staff
        Given I have a valid user
        And I have a valid token
        And I have valid account data to create an instance
        When I make a "POST" request to "/account" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And No account must be created in database

    ### Patch
    Scenario: Partial Update an Account - success
        Given I am a staff user
        And I have a valid token
        And I have valid account data to partial update an instance
        And I have an account with id "666"
        When I make a "PATCH" request to "/account/666" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the partial updated account data in the response
        And I should have the account upated with provided data in database

    Scenario: Partial Update an Account - user not authenticated
        Given I am a staff user
        And I have valid account data to partial update an instance
        And I have an account with id "666"
        When I make a "PATCH" request to "/account/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The account should not be updated in database
    
    Scenario: Partial Update an Account - user not staff
        Given I have a valid user
        And I have a valid token
        And I have valid account data to partial update an instance
        And I have an account with id "666"
        When I make a "PATCH" request to "/account/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The account should not be updated in database

    ### Put
    Scenario: Update an Account - success
        Given I am a staff user
        And I have a valid token
        And I have valid account data to update an instance
        And I have an account with id "666"
        When I make a "PUT" request to "/account/666" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the updated account data in the response
        And I should have the account upated with provided data in database

    Scenario: Update an Account - user not authenticated
        Given I am a staff user
        And I have valid account data to update an instance
        And I have an account with id "666"
        When I make a "PUT" request to "/account/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The account should not be updated in database
    
    Scenario: Update an Account - user not staff
        Given I have a valid user
        And I have a valid token
        And I have valid account data to update an instance
        And I have an account with id "666"
        When I make a "PUT" request to "/account/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The account should not be updated in database
    
    Scenario: Update an Account - missing required fields
        Given I am a staff user
        And I have a valid token
        And Account has required fields
        And I have an account with id "666"
        And I have account data without required fields to update an instance
        When I make a "PUT" request to "/account/666" endpoint with request data using "token" auth
        Then I should get a status 400
        And I should get an error with the required fields and their messages
        And The account should not be updated in database

    ### Delete
    Scenario: Delete an Account - success
        Given I am a staff user
        And I have a valid token
        And I have an account with id "666"
        When I make a "DELETE" request to "/account/666" endpoint with request data using "token" auth
        Then I should get a status 204
        And I do not have a product with id "666"

    Scenario: Delete an Account - user not authenticated
        Given I am a staff user
        And I have an account with id "666"
        When I make a "DELETE" request to "/account/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The account with id "666" should exists
    
    Scenario: Delete an Account - user not staff
        Given I have a valid user
        And I have a valid token
        And I have an account with id "666"
        When I make a "DELETE" request to "/account/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The account with id "666" should exists

    ### List
    Scenario: List Accounts - success
        Given I am a staff user
        And I have a valid token
        And I have some accounts
        When I make a "GET" request to "/account" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the list of accounts in the response

    Scenario: List Accounts - user not authenticated
        Given I am a staff user
        And I have some accounts
        When I make a "GET" request to "/account" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
    
    Scenario: List Accounts - user not staff
        Given I have a valid user
        And I have a valid token
        And I have some accounts
        When I make a "GET" request to "/account" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message

    ### Retrieve
    Scenario: Get Account - success
        Given I am a staff user
        And I have a valid token
        And I have an account with id "666"
        When I make a "GET" request to "/account/666" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the details of the account in response
    
    Scenario: Get Account - user not authenticated
        Given I am a staff user
        And I have an account with id "666"
        When I make a "GET" request to "/account/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
    
    Scenario: Get Account - user not staff
        Given I have a valid user
        And I have a valid token
        And I have an account with id "666"
        When I make a "GET" request to "/account/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
