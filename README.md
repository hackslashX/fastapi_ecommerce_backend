# FastAPI Ecommerce Backend

This project is a web-based e-commerce platform that allows users to browse and purchase products, and provides administrators with tools for managing products, sales, and inventory. The platform is built using the FastAPI web framework and a MySQL database, and includes features such as user authentication, product categorization, and sales data analysis. The project aims to provide a scalable and maintainable solution for online retail businesses.

### Requirements

This project supports Python versions betweeen `3.11.1` and `3.11.3`.

- `fastapi`: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- `SQLAlchemy`: A SQL toolkit and ORM that provides a set of high-level API for connecting to relational databases.
- `pydantic`: A data validation and settings management library using Python type annotations.
- `aiomysql`: A library for accessing a MySQL database from the asyncio framework.
- `fastapi-restful`: A library for building RESTful APIs with FastAPI.
- `passlib`: A password hashing library for Python that provides cross-platform implementations of over 30 password hashing algorithms.
- `pyjwt`: A Python library for encoding and decoding JSON Web Tokens (JWTs).
- `alembic`: A lightweight database migration tool for usage with SQLAlchemy.
- `python-dotenv`: A library for loading environment variables from a `.env` file.
- `pydantic-settings`: A library for managing application settings using Pydantic models.
- `aiosqlite`: A library for accessing a SQLite database from the asyncio framework.
- `pytz`: A library for working with time zones in Python.
- `starlette-context`: A library for managing context variables in Starlette and FastAPI applications.
- `uvicorn`: A lightning-fast ASGI server implementation, using uvloop and httptools.
- `typing-inspect`: A library for runtime inspection of Python typing information.
- `python-multipart`: A library for parsing multipart/form-data requests in Python.
- `argon2-cffi`: A Python binding of the Argon2 password hashing algorithm.
- `pandas`: A library for data manipulation and analysis.

### Steps to Run the Project

1. Clone the project repository to your local machine using `git clone <repository-url>` command.
2. Navigate to the project directory using `cd <project-directory>` command.
3. Install Poetry using the instructions provided on the official website: https://python-poetry.org/docs/#installation
4. Run `poetry install` command to install the project dependencies.
5. Create a MySQL database and update the database connection string in the `.vars` file. You can also leave it as it is to automatically use the SQLite database included with the project.
6. Run the database migrations using `poetry run alembic upgrade head` command.
7. Start the server using `poetry run uvicorn app.main:app --reload` command.

Note: Before running the project, make sure that you have Python 3.11.1 or higher installed on your machine. Also, make sure that the required dependencies are installed using Poetry and the database connection string is updated in the `.vars` file.

### Dummy Data

The project includes a populated SQLite database that can be used to play around with the APIs. While products data was hardcoded, sales data was generated using the scripts in `common/data` folder.

### Database Design

The project uses a relational database to store data. Specifically, it uses a MySQL database with the following tables:

- `users`: Stores information about registered users, such as their username, email, and password hash.
- `categories`: Stores information about product categories, such as their name and description.
- `products`: Stores information about products, such as their name, description, price, and category ID.
- `inventories`: Stores information about product inventory, such as the product ID, quantity, and last updated timestamp.
- `sales`: Stores information about sales, such as the user ID, total revenue, and timestamp.
- `sale_items`: Stores information about individual sale items, such as the sale ID, product ID, quantity, and revenue.
- `tokens`: Stores information about authentication tokens, such as the user ID, token hash, and expiration timestamp.

The relationships between the tables are as follows:

- A user can have many sales, but a sale can only belong to one user. This is a one-to-many relationship between the `users` and `sales` tables.
- A sale can have many sale items, and a sale item can only belong to one sale. This is a one-to-many relationship between the `sales` and `sale_items` tables.
- A product can belong to one category, but a category can have many products. This is a one-to-many relationship between the `categories` and `products` tables.
- A product can have one inventory, and an inventory can only belong to one product. This is a one-to-one relationship between the `products` and `inventories` tables.
- A user can have many authentication tokens, and a token can only belong to one user. This is a one-to-many relationship between the `users` and `tokens` tables.

The relationships are enforced using foreign key constraints in the database schema.

### Endpoint Details

Please see the `endpoints.json` file in the repository for a Postman/HoppScotch compatible collection to test the APIs. Furthermore, the request parameters for all endpoints are managed in `api/v1/endpoints/schemas`, this is useful to get a list of possible parameters that can be forwarded to a request.

- Register User (ecommerce/v1/register_user)
  
  This endpoint is used to register a new user. It accepts a `PUT` request with a JSON payload containing the user's information. The `request_schema` attribute specifies the expected schema for the request payload, which is a `UserCreate` schema. The `response_schema` attribute specifies the expected schema for the response payload, which is a `User` schema.
  
  The endpoint first checks if a user with the specified email already exists in the database. If a user with the specified email exists, the endpoint returns a `422 Unprocessable Entity` response with an error message. If the user does not exist, the endpoint creates a new user in the database using the `crud.user.create` method and returns a `200 OK` response with the newly created user's information in the response payload.
  
  The `authentication_required` attribute is set to `False`, meaning that authentication is not required to access this endpoint. The `api_name` and `api_url` attributes specify the name and URL of the endpoint, respectively.
  
- Login User (ecommerce/v1/login_user)
  
  This endpoint used to log in a user. It accepts a `POST` request with a JSON payload containing the user's email and password. The endpoint first retrieves the user with the specified email from the database using the `crud.user.get_by_email` method. If a user with the specified email does not exist, the endpoint returns a `422 Unprocessable Entity` response with an error message.
  
  The endpoint then verifies the user's password by comparing the hashed password stored in the database with the password provided in the request payload using the `verify_password` function. If the password does not match, the endpoint returns a `422 Unprocessable Entity` response with an error message.
  
  If the user's email and password are valid, the endpoint generates an access token for the user using the `create_jwt_token` function and returns a `200 OK` response with the access token in the response payload. The `touch_last_login` method is called to update the user's last login time in the database.
  
  The `authentication_required` attribute is set to `False`, meaning that authentication is not required to access this endpoint.
  
- Create Category (ecommerce/v1/create_category)
  
  This endpoint is used to create a new category. It accepts a `PUT` request with a JSON payload containing the category's information. The `request_schema` attribute specifies the expected schema for the request payload, which is a `CreateCategoryRequest` schema. The `response_schema` attribute specifies the expected schema for the response payload, which is a `CreateCategoryResponse` schema.
  
  The endpoint first checks if a category with the specified slug already exists in the database using the `check_if_category_exists` method. If a category with the specified slug exists, the endpoint returns a `422 Unprocessable Entity` response with an error message.
  
  If the category does not exist, the endpoint creates a new category in the database using the `create_category` method and returns a `200 OK` response with the newly created category's information in the response payload.
  
  The `authentication_required` attribute is set to `True`, meaning that authentication is required to access this endpoint.
  
- Create Product (ecommerce/v1/create_product)
  
  This endpoint is used to create a new product. It accepts a `PUT` request with a JSON payload containing the product's information. The `request_schema` attribute specifies the expected schema for the request payload, which is a `CreateProductRequest` schema. The `response_schema` attribute specifies the expected schema for the response payload, which is a `CreateProductResponse` schema.
  
  The endpoint first checks if the category specified in the request payload exists in the database using the `check_if_category_exists` method. If the category does not exist, the endpoint returns a `404 Not Found` response with an error message.
  
  If the category exists, the endpoint creates a new product in the database using the `create_product` method and returns a `200 OK` response with the newly created product's information in the response payload.
  
  The `authentication_required` attribute is set to `True`, meaning that authentication is required to access this endpoint.
  
- Get Categories (ecommerce/v1/get_categories)
  
  This endpoint is used to retrieve a list of categories. It accepts a `GET` request with optional query parameters for pagination, sorting, and ordering. The `request_schema` attribute specifies the expected schema for the request payload, which is a `GetCategoriesRequest` schema. The `response_schema` attribute specifies the expected schema for the response payload, which is a `GetCategoriesResponse` schema. The `authentication_required` attribute is set to `True`, meaning that authentication is required to access this endpoint.
  
  The endpoint retrieves a list of categories from the database using the `crud.category.get_multi` method with the specified pagination, sorting, and ordering parameters. It then generates a `200 OK` response with the list of categories in the response payload.
  
- Get Low Stock Products (ecommerce/v1/get_low_stock_products)
  
  This endpoint is used to retrieve a list of low stock products. It accepts a `GET` request with a query parameter for the quantity threshold. The `request_schema` attribute specifies the expected schema for the request payload, which is a `LowStockProductsRequest` schema. The `response_schema` attribute specifies the expected schema for the response payload, which is a `LowStockProductsResponse` schema. The `authentication_required` attribute is set to `True`, meaning that authentication is required to access this endpoint.
  
  The endpoint retrieves a list of products from the database using the `crud.product.get_products_quantity_le` method with the specified quantity threshold parameter. It then generates a `200 OK` response with the list of low stock products in the response payload.
  
- Add Inventory (ecommerce/v1/add_inventory)
  
  This endpoint is used to add inventory to a product. It accepts a `PUT` request with a JSON payload containing the product ID and the quantity of inventory to add. The `request_schema` attribute specifies the expected schema for the request payload, which is an `AddInventoryRequest` schema. The `response_schema` attribute specifies the expected schema for the response payload, which is an `AddInventoryResponse` schema. The `authentication_required` attribute is set to `True`, meaning that authentication is required to access this endpoint.
  
  The endpoint first checks if the product with the specified ID exists in the database using the `check_if_product_exists` method. If the product does not exist, the endpoint returns a `422 Unprocessable Entity` response with an error message.
  
  If the product exists, the endpoint adds the specified quantity of inventory to the product using the `add_inventory` method and updates the product's quantity in the database using the `update` method. It then generates a `200 OK` response with the newly created inventory's information in the response payload using the `generate_response` method.
  
- Get Products (ecommerce/v1/get_products)
  
  This endpoint is used to retrieve a list of products with their associated categories. It accepts a `GET` request with optional query parameters for pagination, sorting, and ordering. The `request_schema` attribute specifies the expected schema for the request payload, which is a `GetProductsRequest` schema. The `response_schema` attribute specifies the expected schema for the response payload, which is a `GetProductsResponse` schema. The `authentication_required` attribute is set to `True`, meaning that authentication is required to access this endpoint.
  
  The endpoint retrieves a list of products with their associated categories from the database using the `crud.product.get_multi_with_category` method with the specified pagination, sorting, and ordering parameters. It then generates a `200 OK` response with the list of products in the response payload.
  
- Purchase Products (ecommerce/v1/purchase_products)
  
  This endpoint is used to purchase one or more products. It accepts a `POST` request with a JSON payload containing a list of `Item` objects, each representing a product to be purchased. The `request_schema` attribute specifies the expected schema for the request payload, which is a `PurchaseProductsRequest` schema. The `response_schema` attribute specifies the expected schema for the response payload, which is a `PurchaseProductsResponse` schema. The `authentication_required` attribute is set to `True`, meaning that authentication is required to access this endpoint.
  
  The endpoint first initializes two lists to keep track of successful and failed purchases. It then iterates over the list of `Item` objects in the request payload and attempts to purchase each product using the `purchase_product` method.
  
  The `purchase_product` method first retrieves the product information from the database using the `crud.product.get_active` method. If the product does not exist, the purchase is considered a failure and the `Item` object is added to the `failed_purchases` list. If the product exists, the method retrieves the product's inventory information using the `crud.inventory.get_by_product_id` method. If the product's inventory is insufficient to fulfill the purchase, the purchase is considered a failure and the `Item` object is added to the `failed_purchases` list. If the product's inventory is sufficient, the method creates a new sale and sale item in the database using the `crud.sale.create` and `crud.sale_item.create` methods, respectively. The product's inventory and sales data are then updated in the database using the `crud.inventory.update` and `crud.product.update` methods, respectively. The purchase is considered a success and the `Item` object is added to the `successful_purchases` list.
  
  After all purchases have been attempted, the endpoint generates a `200 OK` response with the list of successful and failed purchases in the response payload using the `generate_response` method.
  
- Get Sales Data (ecommerce/v1/get_sales_data)
  
  This endpoint is used to retrieve sales and revenue data for a specified date range. It accepts a `GET` request with query parameters for the start and end dates, product IDs, category IDs, and bucketing options. The `request_schema` attribute specifies the expected schema for the request payload, which is a `GetSalesDataRequest` schema. The `response_schema` attribute specifies the expected schema for the response payload, which is a `GetSalesDataResponse` schema. The `authentication_required` attribute is set to `True`, meaning that authentication is required to access this endpoint.
  
  The endpoint first retrieves the sales data from the database using the `crud.sale.get_sales_data` method with the specified request parameters. It then calculates the revenue for each sale and stores the sales data as a list of dictionaries.
  
  If the `buckets` parameter is specified, the endpoint creates buckets based on the specified time interval (daily, weekly, monthly, or yearly) using the `create_buckets` method. It then populates the sales data into the appropriate bucket based on the sale date using the `populate_buckets` method. If the `include_sales_items` parameter is set to `True`, the endpoint also adds the sale to the `sales` list for that bucket.
  
  If the `buckets` parameter is not specified, the endpoint populates the sales data without the bucketing logic using the `populate_metrics` method.
  
  The endpoint generates a `200 OK` response with the sales and revenue data in the response payload using the `generate_response` method.
