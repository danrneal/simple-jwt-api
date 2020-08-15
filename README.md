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
pip install -U pip
pip install -r requirements.txt
```

Set up your environment variables:

```bash
touch .env
echo JWT_SECRET="XXX" >> .env
```

## Usage

You can run this app either locally, in a Docker container, or as part of a Kubernetes cluster.

### Local

Make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

```bash
Usage: flask run
```

### Container

You will need the [Docker Engine](https://docs.docker.com/engine/install/) installed. On Ubuntu:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Then you can build the Docker image and create the container.

```bash
docker build --tag simple-jwt-api .
docker run -p 80:5000 --env-file=.env simple-jwt-api
```

### Kubernetes

Setting up a Kubernetes cluster is beyond the scope of this README however, `ci-cd-codepipeline.cfn.yml` is a template for setting up a CodePipeline in AWS.

#### _Note: You will need to replace the default values in the parameters section before using this template_

## API Reference

The API reference documentation is available [here](https://documenter.getpostman.com/view/10868159/SzfCVS1d?version=latest).

## Testing Suite

The API has a testing suite to test all of the API endpoints

To run all the tests:

```bash
Usage: test_app.py
```

If set up with a CodePipeline in a Kubernetes cluster the tests in the file must all pass before it will deploy.

## Credit

[Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## License

Simple JWT API is licensed under the [MIT license](https://github.com/danrneal/simple-jwt-api/blob/master/LICENSE).
