# imdb-stream-platform-api
IMDB DRF Backend is a Django and DRF-based service for managing IMDB data. It offers a robust API for CRUD operations on movie records, advanced search, pagination, and user reviews. Secure endpoints with token-based authentication and explore interactive API documentation.

## 📚 Features

**CRUD Operations**: Create, Read, Update, and Delete movie records.

**Search Functionality**: Search for movies based on various criteria.

**Pagination**: Efficiently handle large sets of data with pagination.

**Authentication & Authorization**: Secure endpoints using token-based authentication.

**Swagger Documentation**: Interactive API documentation for easy testing and exploration.

## 🚀 Getting Started
**Prerequisites**
  
  Python
  
  Django
  
  Django Rest Framework

Installation
1. **Clone the Repository**:
   ```bash
    git clone https://github.com/AtharvaVidye/IMDB-DRF-Backend.git
    cd IMDB-DRF-Backend

2. **Create a Virtual Environment and Activate It**:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the Required Dependencies**:
   ```bash
    pip install -r requirements.txt

4. **Apply Database Migrations**:
   ```bash
    python manage.py migrate

5. **Run the Development Server**:
   ```bash
    python manage.py runserver
The backend service should now be running at http://127.0.0.1:8000/.

🛠️ API Endpoints

**Movies**

* GET /movies/: List all movies.
* POST /movies/: Create a new movie.
* GET /movies/{id}/: Retrieve a specific movie.
* PUT /movies/{id}/: Update a specific movie.
* DELETE /movies/{id}/: Delete a specific movie.

**Authentication**

* POST /account/login/: Obtain a token for authentication.
* POST /account/register/: Register a new user.
* POST /account/logout/: Logout a user.

