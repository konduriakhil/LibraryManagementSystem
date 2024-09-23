# Users Service API Documentation

This document provides an overview of the Users Service API endpoints and how to use them.

## Base URL

All API requests should be made to: `http://localhost:8001/api/v1`

## Authentication

Most endpoints require authentication using a JWT token. Include the token in the `Authorization` header of your requests:

Authorization: Bearer <your_access_token>

## Endpoints

### 1. Create a new user

- **URL:** `/users/`
- **Method:** `POST`
- **Auth required:** No

#### Request Body

json
{
"username": "johndoe",
"email": "johndoe@example.com",
"password": "securepassword123",
"user_type": "member"
}

#### Response

json
{
"id": 1,
"username": "johndoe",
"email": "johndoe@example.com",
"user_type": "member",
"created_at": "2023-04-01T12:00:00",
"modified_at": "2023-04-01T12:00:00"
}

### 2. Login (Get access and refresh tokens)

- **URL:** `/token`
- **Method:** `POST`
- **Auth required:** No

#### Request Body

json
{
"username": "johndoe",
"password": "securepassword123"
}

#### Response

json
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"token_type": "bearer"
}

### 3. Refresh access token

- **URL:** `/token/refresh`
- **Method:** `POST`
- **Auth required:** No

#### Request Body

json
{
"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

#### Response

json
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"token_type": "bearer"
}

### 4. Get current user information

- **URL:** `/users/me`
- **Method:** `GET`
- **Auth required:** Yes

#### Response

json
{
"id": 1,
"username": "johndoe",
"email": "johndoe@example.com",
"user_type": "member",
"created_at": "2023-04-01T12:00:00",
"modified_at": "2023-04-01T12:00:00"
}

### 5. Get all users

- **URL:** `/users/`
- **Method:** `GET`
- **Auth required:** Yes
- **Query parameters:**
  - `skip`: Number of records to skip (default: 0)
  - `limit`: Maximum number of records to return (default: 100)

#### Response

json
[
{
"id": 1,
"username": "johndoe",
"email": "johndoe@example.com",
"user_type": "member",
"created_at": "2023-04-01T12:00:00",
"modified_at": "2023-04-01T12:00:00"
},
{
"id": 2,
"username": "janedoe",
"email": "janedoe@example.com",
"user_type": "librarian",
"created_at": "2023-04-02T10:30:00",
"modified_at": "2023-04-02T10:30:00"
}
]

### 6. Get user by ID

- **URL:** `/users/{user_id}`
- **Method:** `GET`
- **Auth required:** Yes

#### Response

json
{
"id": 1,
"username": "johndoe",
"email": "johndoe@example.com",
"user_type": "member",
"created_at": "2023-04-01T12:00:00",
"modified_at": "2023-04-01T12:00:00"
}

### 7. Update user

- **URL:** `/users/{user_id}`
- **Method:** `PUT`
- **Auth required:** Yes

#### Request Body

json
{
"username": "johndoe_updated",
"email": "johndoe_updated@example.com",
"password": "newpassword123",
"user_type": "librarian"
}

#### Response

json
{
"id": 1,
"username": "johndoe_updated",
"email": "johndoe_updated@example.com",
"user_type": "librarian",
"created_at": "2023-04-01T12:00:00",
"modified_at": "2023-04-03T15:45:00"
}

### 8. Delete user

- **URL:** `/users/{user_id}`
- **Method:** `DELETE`
- **Auth required:** Yes

#### Response

json
{
"id": 1,
"username": "johndoe_updated",
"email": "johndoe_updated@example.com",
"user_type": "librarian",
"created_at": "2023-04-01T12:00:00",
"modified_at": "2023-04-03T15:45:00"
}

## Error Responses

In case of errors, the API will return appropriate HTTP status codes along with a JSON response containing error details. For example:

json
{
"detail": "User not found"
}

Common error status codes:
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 422: Unprocessable Entity

## Usage Examples

Here are some examples using `curl` to interact with the API:

1. Create a new user:
bash
curl -X POST http://localhost:8001/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"username": "newuser", "email": "newuser@example.com", "password": "password123", "user_type": "member"}'

2. Login and get tokens:
bash
curl -X POST http://localhost:8001/api/v1/token \
-H "Content-Type: application/json" \
-d '{"username": "newuser", "password": "password123"}'

3. Get current user information:
bash
curl -X GET http://localhost:8001/api/v1/users/me \
-H "Authorization: Bearer <your_access_token>"

4. Update user information:
bash
curl -X PUT http://localhost:8001/api/v1/users/1 \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json" \
-d '{"username": "updateduser", "email": "updateduser@example.com", "password": "newpassword123", "user_type": "librarian"}'

Remember to replace `<your_access_token>` with the actual access token received from the login endpoint.

## Notes

- The `user_type` field can be one of: "administrator", "librarian", or "member".
- All authenticated endpoints require a valid JWT token in the Authorization header.
- The refresh token endpoint can be used to obtain a new access token when the current one expires.
- Be sure to keep your access and refresh tokens secure and never expose them publicly.
This updated documentation provides a comprehensive guide on how to use the Users Service API, including:
1. Base URL information
Authentication requirements
Detailed descriptions of all endpoints
Request and response examples for each endpoint
Error handling information
Usage examples using curl
Additional notes on using the API
This documentation will help developers understand and interact with the Users Service API effectively.