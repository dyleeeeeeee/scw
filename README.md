# scw
# scw

**Setup Instructions**

1. Clone the repository
2. `cd scw`
3. `docker-compose up -d --build`
6. Open `http://<IP>:8000/` in your web browser

**Architectural Overview**

The system is composed of the following components:

1. **Web Server**: A Django web server, responsible for serving the web API and static files.
2. **Database Server**: A Postgres database server, used to store all data.
3. **Celery Worker**: A Celery worker, responsible for running background tasks.
4. **Redis Server**: A Redis server, used as a message broker for Celery.
5. **ECS Cluster**: An AWS ECS cluster, used to run the Celery worker and Postgres database server.
6. **Docker Compose**: Docker Compose, used to run the web server and Celery worker.

**API Usage**

The API can be accessed by visiting `http://<IP>>:8000/` in your web browser.

**API Endpoints**

### Authentication

* `POST /api/auth/login/`: Login to the API, returning a JSON Web Token.
* `POST /api/auth/register/`: Register a new user, returning a JSON Web Token.

### Tasks

* `GET /api/tasks/`: List all tasks.
* `GET /api/tasks/:id/`: Retrieve a single task by ID.
* `POST /api/tasks/`: Create a new task.

### Architecture

+-------------------+
|   User/Client     |
+--------+----------+
         |
         v
+--------+----------+    +------------------+
| Django REST API   |<-->| Celery Worker(s) |
|   (Gunicorn)      |    +------------------+
+--------+----------+            |
         |                       v
         v               +------------------+
+--------+----------+    |     Redis        |
|   PostgreSQL      |    +------------------+
+-------------------+
         |
         v
+-------------------+
|   AWS ECS/ECR     |
| (Production)      |
+-------------------+


### API Usage

**Authentication**

*   Register: POST /api/register/ (username, password)
*   Obtain token via login (if JWT/Auth enabled)

**Task Endpoints**

*   Create Task:
    *   POST /api/process/
    *   Body: { "email": "...", "message": "..." }
*   List Tasks:
    *   GET /api/tasks/
*   Retrieve Task Status:
    *   GET /api/tasks/{id}/status/

**Example: Create Task**


curl -X POST http://localhost:8000/api/process/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "message": "Hello"}'


### Infrastructure & Deployment

**AWS Infrastructure (Terraform)**

All AWS resources (ECR, ECS, IAM roles, etc.) are defined in /terraform/main.tf.
Update variables as needed, then run:


cd terraform
terraform init
terraform plan
terraform apply


**Deploy to AWS ECS**

*   Build and push Docker images to ECR.
*   Update ECS task definitions (.aws/task-definition.json).
*   Use GitHub Actions workflow (.github/workflows/aws.yml) for CI/CD automation.