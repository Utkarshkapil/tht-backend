
# Starlette Full-Stack Document Management Application

This application is a simple full-stack API built using Starlette and `asyncpg` to manage documents stored in a PostgreSQL database. It includes features to fetch and update document data with drag-and-drop functionality on the frontend.

## Prerequisites

Make sure you have the following installed:

- Python 3.8+
- PostgreSQL
- Node.js and npm (for the frontend, if applicable)

## Setting Up the Environment

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database:**

   Make sure you have a running PostgreSQL instance and the necessary database configurations in `dbsetup.py`.

   - You should have a function in `dbsetup.py` to set up the database, tables, and seed data. This will be executed by `asyncio.run(setup_database())` during the app startup.

5. **Database Environment Variables:**

   Ensure the following variables are set in `dbsetup.py`:

   - `DB_NAME` — your database name.
   - `DB_USER` — your database user.
   - `DB_PASSWORD` — your database password.
   - `DB_HOST` — your database host.
   - `DB_PORT` — your database port.

## Running the Application

1. **Start the application:**

   Run the server with

   ```bash
      python3 app.py
   ```

   This starts the server on `http://localhost:8000`.

2. **Accessing the API:**

   You can access the following API endpoints:

   - `GET /documents` — Fetch all documents.
   - `POST /documents` — Update document information.

## API Endpoints

### 1. `GET /documents`

- **Description**: This route fetches all documents from the database, ordered by their `position`.
- **Response**: A JSON array of documents, where each document includes `id`, `type`, `title`, `position`, and `imageurl`.

#### Example Response:

```json
[
  {
    "id": 1,
    "type": "PDF",
    "title": "Document 1",
    "position": 1,
    "imageurl": "https://example.com/image1.png"
  },
  {
    "id": 2,
    "type": "Word",
    "title": "Document 2",
    "position": 2,
    "imageurl": "https://example.com/image2.png"
  }
]
```

### 2. `POST /documents`

- **Description**: This route receives a JSON array of document updates, iterates over each document, and updates their corresponding entries in the database.
- **Request Body**: A JSON array containing document objects with the fields `id`, `type`, `title`, `position`, and `imageurl`.
  
#### Example Request Body:

```json
[
  {
    "id": 1,
    "type": "PDF",
    "title": "Updated Document 1",
    "position": 2,
    "imageurl": "https://example.com/image1-new.png"
  },
  {
    "id": 2,
    "type": "Word",
    "title": "Updated Document 2",
    "position": 1,
    "imageurl": "https://example.com/image2-new.png"
  }
]
```

- **Response**: A success message in JSON format indicating that the update was successful:

```json
{
  "status": "success"
}
```

## Code Explanation

### 1. `setup_database()`

This function, imported from `dbsetup.py`, handles the database initialization and setup. It is executed at the start of the application to ensure the database is ready for operations.

### 2. `get_db_connection()`

This asynchronous function establishes a connection to the PostgreSQL database using `asyncpg`. It returns a connection object that is used in subsequent database queries.

### 3. `get_documents()`

This is an asynchronous route handler that retrieves document data from the `documents` table in the database. It:

- Establishes a connection to the database using `get_db_connection()`.
- Fetches all documents, ordered by their `position`.
- Returns a JSON response with the document data.
- Closes the database connection after the operation.

### 4. `update_documents()`

This route handles updates to the document data. It:

- Receives JSON data from the request.
- For each document in the received data, it performs an `UPDATE` query in a transaction to ensure atomicity.
- Closes the database connection after the updates are completed.
- Returns a success message.

### 5. Middleware

The `CORS` middleware is included to allow cross-origin requests from any domain (`*`), which is useful during development, especially when interacting with a frontend running on a different port or domain.

### 6. `if __name__ == "__main__":`

This block ensures that the application is run using `uvicorn`, with the app served on `http://0.0.0.0:8000`.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
