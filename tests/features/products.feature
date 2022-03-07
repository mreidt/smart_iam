Feature: Products
    ### Post
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

    ### Patch
    Scenario: Partial Update a Product - success
        Given I am a staff user
        And I have a valid token
        And I have valid product data to partial update an instance
        And I have a product with id "666"
        When I make a "PATCH" request to "/products/666" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the partial updated product data in the response
        And I should have the product upated with provided data in database

    Scenario: Partial Update a Product - user not authenticated
        Given I am a staff user
        And I have valid product data to partial update an instance
        And I have a product with id "666"
        When I make a "PATCH" request to "/products/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The product should not be updated in database

    Scenario: Partial Update a Product - user not staff
        Given I have a valid user
        And I have a valid token
        And I have a product with id "666"
        And I have valid product data to partial update an instance
        When I make a "PATCH" request to "/products/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The product should not be updated in database

    ### Put
    Scenario: Update a Product - success
        Given I am a staff user
        And I have a valid token
        And I have valid product data to update an instance
        And I have a product with id "666"
        When I make a "PUT" request to "/products/666" endpoint with request data using "token" auth
        Then I should get a status 200
        And I should get the updated product data in the response
        And I should have the product upated with provided data in database

    Scenario: Update a Product - user not authenticated
        Given I am a staff user
        And I have valid product data to update an instance
        And I have a product with id "666"
        When I make a "PUT" request to "/products/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The product should not be updated in database

    Scenario: Update a Product - user not staff
        Given I have a valid user
        And I have a valid token
        And I have a product with id "666"
        And I have valid product data to update an instance
        When I make a "PUT" request to "/products/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The product should not be updated in database

    Scenario: Update a Product - missing required fields
        Given I have a valid user
        And I have a valid token
        And I have a product with id "666"
        And Product has required fields
        And I have product data without required fields to update an instance
        When I make a "PUT" request to "/products/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The product should not be updated in database

    ### Delete
    Scenario: Delete a Product - success
        Given I am a staff user
        And I have a valid token
        And I have a product with id "666"
        And The product is inactive
        When I make a "DELETE" request to "/products/666" endpoint with request data using "token" auth
        Then I should get a status 204
        And I do not have a product with id "666"

    Scenario: Delete a Product - user not authenticated
        Given I am a staff user
        And I have a product with id "666"
        And The product is inactive
        When I make a "DELETE" request to "/products/666" endpoint with request data using "no" auth
        Then I should get a status 401
        And I should get an unauthorized error
        And The product with id "666" should exists

    Scenario: Delete a Product - user not staff
        Given I have a valid user
        And I have a valid token
        And I have a product with id "666"
        And The product is inactive
        When I make a "DELETE" request to "/products/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a default forbidden message
        And The product with id "666" should exists

    Scenario: Delete a Product - active product
        Given I am a staff user
        And I have a valid token
        And I have a product with id "666"
        When I make a "DELETE" request to "/products/666" endpoint with request data using "token" auth
        Then I should get a status 403
        And I should get a "Cannot delete active product." message
        And The product with id "666" should exists
