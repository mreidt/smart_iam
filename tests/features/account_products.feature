Feature: Account Products
    ### Post
    Scenario: Create an AccountProduct - success
        Given I am a staff user
        And I have a valid token
        And I have an account with id "666"
        And I have a product with id "666"
        And I have valid account_product data to create an instance
        When I make a "POST" request to "/account-products" endpoint with request data using "token" auth
        Then I should get a status 201
        And I should get the created account_product data in the response
        And I should have the new account_product created with provided data in database

    Scenario: Create an AccountProduct - missing required fields
        Given I am a staff user
        And I have a valid token
        And AccountProducts has required fields
        And I have account_product data without required fields to create an instance
        When I make a "POST" request to "/account-products" endpoint with request data using "token" auth
        Then I should get a status 400
        And I should get an error with the required fields and their messages
        And No account_product must be created in database

    Scenario: Create an AccountProduct - user not authenticated
        Given I am a staff user
        And I have an account with id "666"
        And I have a product with id "666"
        And I have valid account_product data to create an instance
        When I make a "POST" request to "/account-products" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And No account_product must be created in database
    
    Scenario: Create an AccountProduct - user not staff
        Given I have a valid user
        And I have a valid token
        And I have an account with id "666"
        And I have a product with id "666"
        And I have valid account_product data to create an instance
        When I make a "POST" request to "/account-products" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And No account_product must be created in database
    
    Scenario: Create an AccountProduct - same product multiple times in account
        Given I am a staff user
        And I have a valid token
        And I have an account with id "666"
        And I have a product with id "666"
        And I have valid account_product data to create an instance
        When I make a "POST" request to "/account-products" endpoint with request data using "token" auth
        Then I should get a status 201
        And I should get the created account_product data in the response
        And I should have the new account_product created with provided data in database
        When I make a "POST" request to "/account-products" endpoint with request data using "token" auth
        Then I should get a status 400
        And I should get a non-field error "This account already has this product." message

    ### Delete
    Scenario: Delete an AccountProduct - success
        Given I am a staff user
        And I have a valid token
        And I have an account_product with id "666"
        When I make a "DELETE" request to "/account-products/666" endpoint with request data using "token" auth
        Then I should get a status 204
        And I do not have a product with id "666"

    Scenario: Delete an AccountProduct - user not authenticated
        Given I am a staff user
        And I have an account_product with id "666"
        When I make a "DELETE" request to "/account-products/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The account_product with id "666" should exists
    
    Scenario: Delete an AccountProduct - user not staff
        Given I have a valid user
        And I have a valid token
        And I have an account_product with id "666"
        When I make a "DELETE" request to "/account-products/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The account_product with id "666" should exists

    ### List
    Scenario: List AccountProduct - success
        Given I am a staff user
        And I have a valid token
        And I have some account_products
        When I make a "GET" request to "/account-products" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the list of account_products in the response

    Scenario: List AccountProduct - user not authenticated
        Given I am a staff user
        And I have some account_products
        When I make a "GET" request to "/account-products" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
    
    Scenario: List AccountProduct - user not staff
        Given I have a valid user
        And I have a valid token
        And I have some account_products
        When I make a "GET" request to "/account-products" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message

    ### Retrieve
    Scenario: Get AccountProduct - success
        Given I am a staff user
        And I have a valid token
        And I have an account_product with id "666"
        When I make a "GET" request to "/account-products/666" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the details of the account_product in response
    
    Scenario: Get AccountProduct - user not authenticated
        Given I am a staff user
        And I have an account_product with id "666"
        When I make a "GET" request to "/account-products/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
    
    Scenario: Get AccountProduct - user not staff
        Given I have a valid user
        And I have a valid token
        And I have an account_product with id "666"
        When I make a "GET" request to "/account-products/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
