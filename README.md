# FastAPI Social Media Backend

Welcome to the FastAPI Social Media Backend! This project is a backend application built on the principles of a social media platform. It utilizes FastAPI, Pydantic for data modeling, SQLAlchemy as the ORM for database interactions, and Alembic for database migrations. The application supports user authentication using JWTs and provides a set of APIs for managing social media posts and votes.

## Features

- **User Authentication**: Users can log in with authentication using JSON Web Tokens (JWTs).

- **Post Management APIs**:

	- Create a post

	- Fetch all posts by an authenticated user

	- Update a post (by the owner of the post, authenticated with JWT)

	- Delete a post (by the owner of the post, authenticated with JWT)

- **Vote Management APIs**:

	- Vote on any post (by an authenticated user)

	- Retract a vote on any previously voted post

	- Standardized Responses: Each API provides a standard status code response.

## Tech Stack

- **FastAPI**: A modern, fast web framework for building APIs with Python.

- **Pydantic**: For data validation and data modeling.

- **SQLAlchemy**: ORM for database interactions, defining schemas for the user, post, and votes tables.

- **Alembic**: Database migration tool to create and manage databases.

- **PostgreSQL**: Database to store user information, posts, and votes on posts.

- **Pytest**: Unit testing framework with multiple test cases covering various scenarios for each API.

- **Docker**: Containerization for seamless deployment and scalability.

- **GitHub Actions**: CI/CD pipeline using GitHub workflows.

## API Endpoints
### User Management  
-  **Endpoint:**  `/users`  
	-  **Method:** POST 
	-  **Description:** Create a new user. 
	-  **Request Payload:**  - Content-Type: `application/json`  
		```json 
		{ 
		"username": "<username>",
		"password": "<password>",
		"email": "<email>" 
		  } 
		``` 
		-  `username` (string): The username for the new user.
		-  `password` (string): The password for the new user. 
		-  `email` (string): The email address for the new user. 
	-  **Response:**  - A JSON object containing user information upon successful user creation. 

-  **Endpoint:**  `/users/{user_id}`  
	-  **Method:** GET 
	-  **Description:** Get information about a specific user. 
	-  **Path Parameters:**  
		-  `user_id` (integer): The unique identifier of the user. 

	
### User Authentication

-   **Endpoint:** `/login`
    -   **Method:** POST
    -   **Description:** Log in with authentication using JSON Web Tokens (JWTs).
    -  **Request Payload:**  
	    - Content-Type: `application/x-www-form-urlencoded`  
			```
			username=<username>
			password=<password>
			```
			- `username` (string): The email of the user.
			- `password` (string): The password of the user.

### Post Management

-   **Endpoint:** `/posts`
    -   **Method:** POST
    -   **Description:** Create a post
    -  **Request Payload:**  - Content-Type: `application/json` 
	    ```json
	    {
		    "title" :  "<title>",
		    "content" : "<content>",
		    "published" : "<published>"
		}
		```
		- `title` (string): Title of the post.
		- `content` (string): Content inside the post.
		- `published` (boolean): (Optional) `true` or `false`. Defaults to `true`.
		    
-   **Endpoint:** `/posts`
    -   **Method:** GET
    -   **Description:** Fetch all posts by an authenticated user
-   **Endpoint:** `/posts/{post_id}`
    -   **Method:** PUT
    -   **Description:** Update a post (by the owner of the post, authenticated with JWT)
    -  **Request Payload:**  - Content-Type: `application/json` 
	    ```json
	    {
		    "title" :  "<updated-title>",
		    "content" : "<updated-content>"
		}
		```
		- `title` (string): Updated title of the post.
		- `content` (string): Updated ontent inside the post.

-   **Endpoint:** `/posts/{post_id}`
    -   **Method:** DELETE
    -   **Description:** Delete a post (by the owner of the post, authenticated with JWT)

### Vote Management

-   **Endpoint:** `/vote`
    -   **Method:** POST
    -   **Description:** Vote on any post (by an authenticated user)
	-  **Request Payload:**  - Content-Type: `application/json`  
		```json 
		{ 
		"post_id": <post_id>,
		"dir": 1 or 0 
		  } 
		``` 
		- `post_id` (integer): Id of the post.
		- `dir` (integer): `1` to cast a vote and `0` to retract a vote on a post.

## Getting Started

### Prerequisites

- Docker

- Docker Compose

### Development Setup

1. Clone the repository:
```sh
git clone https://github.com/captainsparrow02/fastapi_backend_app.git
```
2. Navigate to the project directory:
```sh
cd fastapi-backend-app
```

3. Create a .env file in the root directory with the necessary environment variables (database credentials, JWT secret, etc.).
```config
DATABASE_USERNAME=<database-username>
DATABASE_PASSWORD=<database-password>
DATABASE_HOSTNAME=<database-hostname>
DATABASE_PORT=<database-port>
DATABASE_NAME=<database-name>
SECRET_KEY=<secret-key>
ALGORITHM=<algorithm>
ACCESS_TOKEN_EXPIRY=<access-token-expiry>
```
4. Run the development Docker Compose file:
```sh
docker-compose -f docker-compose.dev.yml up -d
```

5. The FastAPI application should now be accessible at `'http://localhost:8000'`.

### Production Deployment

For production, use the `'docker-compose.prod.yml'` file instead:
```sh
docker-compose -f docker-compose.prod.yml up -d
```
## Running Tests

1. Ensure the development environment is set up.

2. Run tests using Pytest:
```sh
docker-compose -f docker-compose.dev.yml exec web pytest
```
## Continuous Integration/Continuous Deployment (CI/CD)

The project includes a CI/CD pipeline using GitHub Actions. The CI portion runs on every push to the repository, executing tests to ensure the code quality. The CD portion deploys the application automatically to a remote EC2 instance in AWS.
