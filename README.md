# Restaurant Reservation System

This project is a Django-based restaurant reservation system.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Docker
-   Docker Compose

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2.  **Create your environment file:**
    Copy the sample environment file to a new `.env` file.
    ```bash
    cp env.sample .env
    ```
    You can customize the database settings in the `.env` file if needed.

3.  **Build and run the containers:**
    Navigate to the `deployment` directory and use Docker Compose to build and start the services.
    ```bash
    cd deployment
    docker-compose up --build
    ```

4.  **Create a superuser:**
    Once the containers are running, you will need to create a superuser to access the Django admin interface. Open a new terminal window and run the following command:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    Follow the prompts to create your superuser account.

5.  **Access the application:**
    You can now access the application at [http://localhost:80](http://localhost:80) and the Django admin panel at [http://localhost:80/admin/](http://localhost:80/admin/).
