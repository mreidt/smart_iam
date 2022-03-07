Feature: Products
    Scenario: Create a Product - success
        Given I am a staff user
        And I have a valid token
        And I have valid product data to create an instance
        When I make a "POST" request to "/products" endpoint with request data using "token" auth
        Then I should get a status 201
        And I should get the created product data in the response
        And I should have the new product created with provided data in database

    Scenario: Create a Product - missing required fields
        Given I am a staff user
        And I have a valid token
        And Product has required fields
        And I have product data without required fields to create an instance
        When I make a "POST" request to "/products" endpoint with request data using "token" auth
        Then I should get a status 400
        And I should get an error with the required fields and their messages
        And No product must be created in database

    Scenario: Create a Product - user not authenticated
        Given I am a staff user
        And I have valid product data to create an instance
        When I make a "POST" request to "/products" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And No product must be created in database
    
    Scenario: Create a Product - user not staff
        Given I have a valid user
        And I have a valid token
        And I have valid product data to create an instance
        When I make a "POST" request to "/products" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And No product must be created in database
