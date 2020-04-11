# Simple JWT API

This is a simple API that creates a JSON Web Token (JWT) and decodes it to demonstrate the Containerization and Orchestration of a simple API.

## Set-up

Set-up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

You should see (env) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

Install the requirements:

```bash
pip install -r requirements.txt
```

Set up your environment variables:

```bash
touch .env
echo JWT_SECRET="XXX" >> .env
echo LOG_LEVEL=DEBUG >> .env
```

## Usage

You can run this app either locally, in a Docker container, or as part of a Kubernetes cluster.

### Local

Make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

```bash
Usage: main.py
```

### Container

```bash
docker build --tag simple-jwt-api .
docker run -p 80:8080 --env-file=.env simple-jwt-api
```

### Kubernetes

Setting up a Kubernetes cluster is beyond the scope of this README however, `ci-cd-codepipeline.cfn.yml` is a template for setting up a CodePipeline in AWS.

#### _Note: You will need to replace the default values in the parameters section before using this template_

## API Reference

### Base URL

When running locally with the built in flask server, the base url is as follows:

```bash
http://127.0.0.1:8080/
```

When running in a container with a gunicorn server, the base url is as follows:

```bash
http://127.0.0.1/
```

When running as part of a Kubernetes cluster, the base url is whatever external IP is configured or assigned.

### Endpoints

#### GET /

A simple health check that returns the str 'Healthy'

Example Request:

```bash
curl http://127.0.0.1:8080/
```

Example Response:

```bash
"Healthy"
```

#### POST /

A simple health check that returns the str 'Healthy'

Example Request:

```bash
curl -X POST http://127.0.0.1:8080/
```

Example Response:

```bash
"Healthy"
```

#### POST /auth

Create a JWT based on the provided email, password, and secret

Example Request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email": "test@example.com", "password": "Password1!"}' http://127.0.0.1:8080/auth
```

Example Response:

```bash
{
    "token": "<token>"
}
```

#### GET /contents

Get the non-secret part of a user token

Example Request:

```bash
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8080/contents
```

Example Response:

```bash
{
    "email": "test@example.com",
    "exp": 1587772932,
    "nbf": 1586563332
}
```

## Testing Suite

The API has a testing suite to test all of the API endpoints

To run all the tests:

```bash
usage: pytest test_main.py
```

If set up with a CodePipeline in a Kubernetes cluster the tests in the file must all pass before it will deploy.

## Credit

[Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## License

Simple JWT API is licensed under the [MIT license](https://github.com/danrneal/simple-jwt-api/blob/master/LICENSE).
