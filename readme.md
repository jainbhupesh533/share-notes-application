# Note-Taking Application API

This README provides instructions for interacting with the Note-Taking Application API. The API allows users to perform basic CRUD operations on notes.
## Prerequisites

Before you begin, ensure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Running the Project

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-project.git
    cd your-project
    ```

2. Create a `.env` file in the root directory with the following environment variables:
    Follow the .env_example file
    ```plaintext
    SECRET_KEY=your_secret_key
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    ```

3. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

4. Once the containers are up and running, the Django application should be accessible at `http://127.0.0.1:8000/`.

5. At the time of intialization, it ll automatically test the django application

## API Endpoints

### User Registration

- **POST /signup**: Create a new user account.
  - Request Body: `{ "username": "example", "email": "example@example.com", "password": "password" }`
  - Response: Returns the newly created user object if successful, along with a 201 Created status code.

### User Login

- **POST /login**: Authenticate and login a user.
  - Request Body: `{ "username": "example", "password": "password" }`
  - Response: Returns an authentication token if successful, along with a 200 OK status code.

### Create a New Note

- **POST /notes/create**: Create a new note.
  - Requires authentication.
  - Request Body: `{ "content": "Note content here" }`
  - Response: Returns the newly created note object if successful, along with a 201 Created status code.

### Get a Specific Note

- **GET /notes/{id}**: Retrieve a specific note by its ID.
  - Requires authentication.
  - Response: Returns the requested note object if the user has access, along with a 200 OK status code. Otherwise, returns a 403 Forbidden status code.

### Share a Note

- **POST /notes/share**: Share a note with other users.
  - Requires authentication.
  - Request Body: `{ "note_id": 1, "user_ids": [2, 3] }`
  - Response: Returns a success message if the note is shared successfully, along with a 201 Created status code.

### Update a Note

- **PUT /notes/{id}**: Update an existing note.
  - Requires authentication.
  - Request Body: `{ "content": "Updated note content here" }`
  - Response: Returns a success message if the note is updated successfully, along with a 200 OK status code.

### Get Note Version History

- **GET /notes/version-history/{id}**: Get the version history of a note.
  - Requires authentication.
  - Response: Returns the version history of the note, including timestamps, user who made the changes, and the changes made to the note, along with a 200 OK status code.