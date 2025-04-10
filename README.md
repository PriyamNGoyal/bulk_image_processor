# Bulk Image Compression API

This is a FastAPI application for bulk image processing that allows users to upload CSV files containing product information and images. The images are processed asynchronously, compressed, and stored in an AWS S3 bucket. The application also provides an API for checking the status of image processing.

![Repo Views](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/PriyamNGoyal/bulk_image_processor/main/views.json)

## Features

* Upload CSV files with product names and image URLs.
* Process images asynchronously with Celery and Redis.
* Compress images and store them in AWS S3.
* Query product status and download results in CSV format.

## Requirements

Before running the project, ensure you have the following:

* Python 3.10+
* Docker and Docker Compose (for local development and deployment)
* AWS account for S3 storage
* Redis for Celery task queue
* PostgreSQL for database storage

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/bulk-image-compressor.git
cd bulk-image-compressor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Setup `.env` file

    DATABASE_URL={enter_postgre_connection_url}
    AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID}
    AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY}
    S3_BUCKET_NAME={S3_BUCKET_NAME}
    AUTH_BEARER_TOKEN={AUTH_BEARER_TOKEN}
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0

### 4. Set up Docker
The project includes a `docker-compose.yml` file that will set up the necessary services: Redis, PostgreSQL, and the FastAPI application.

```bash
docker-compose up --build
```
This will build and start the containers for PostgreSQL, Redis, and the FastAPI API application.

#### 5. [Code Documentaton](https://docs.google.com/document/d/1jQzjQnKQsgVLiJQLtZsGGJt4Ho3VGyB1YPoOf_YCeyQ/edit?usp=sharing)
#### 6. [Api Documentaton](https://documenter.getpostman.com/view/36986396/2sAYkHoHtR)
#### 7. [Asynchronous Workers Documentation](https://docs.google.com/document/d/1p5f81hiQNdhA_oXzbY0J-oumBoBn1bx2XJIXj23qn_Q/edit?usp=sharing)
