# **Flask REST API – DRU Project**  

## 📌 Project Overview  
This project is a **RESTful API** built with **Flask** following the **MVC (Model-View-Controller) architectural pattern**. The API allows performing **CRUD (Create, Read, Update, Delete) operations** on two entities: **Actors** and **Movies**, stored in a **PostgreSQL database**.  

The main goal is to **learn how to build a RESTful API**, understand how to handle database interactions, and **Dockerize** the application for seamless deployment. This project follows a structured, modular approach, which can be adapted for any similar API development task.  

## 🔧 Technologies Used  
- **Flask** – Lightweight web framework for building APIs  
- **PostgreSQL** – Robust and scalable relational database  
- **Docker** – Containerization for easy deployment  
- **MVC Architecture** – For better separation of concerns and maintainability  

## 🚀 Project Plan & Features  
- **Create Database** and connect it to the Flask app  
- Build **Models** for **Actors** and **Movies**  
- Implement **CRUD operations** (e.g., create(), update(), commit())  
- Design **Controller methods** for request processing and error handling (e.g., get_actor_by_id(), add_movie())  
- Set up **Routes** to map HTTP requests to controller functions  
- **Test** the application for correctness  
- **Dockerize** the app for efficient deployment  

## 🗂️ Folder Structure  
The project follows the **MVC (Model-View-Controller)** pattern to keep the code modular and maintainable. Here’s the structure of the project:

```
app
    ├── models                  # Contains all database models
    │   ├── __init__.py
    │   ├── base.py             # Base class for data management
    │   ├── actor.py            # Actor model
    │   ├── movie.py            # Movie model
    │   └── relations.py        # Relationships between Actor and Movie
    ├── controllers             # Handlers for CRUD operations
    │   ├── actor.py            # Operations related to Actor
    │   ├── movie.py            # Operations related to Movie
    │   └── parse_request.py    # Parses incoming requests
    ├── settings                # Constant values and configuration
    │   └── constants.py        # Stores constant values
    ├── core                    # Core components of the app
    │   ├── __init__.py         # App and DB initialization
    │   └── routes.py           # Application routes
    ├── tests                   # Test cases for handlers
    │   ├── actor_test.py       # Tests for Actor-related handlers
    │   ├── movie_test.py       # Tests for Movie-related handlers
    │   └── relationships_test.py # Tests for Actor-Movie relationships
    ├── run.py                  # App run file
    ├── Dockerfile              # Docker commands for containerization
    └── requirements.txt        # Project dependencies
```

## 📦 Setup & Installation  
1. Clone the repository:
    ```bash
    git clone https://github.com/todmount/Flask_REST_API_Project.git
    cd Flask_REST_API_Project
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure your PostgreSQL database and adjust any necessary settings in `settings/constants.py`.

4. **Run the app:**
    ```bash
    python run.py
    ```

5. For **Docker** deployment, build and run the container:
    ```bash
    docker build -t flask-rest-api .
    docker run -p 5000:5000 flask-rest-api
    ```
