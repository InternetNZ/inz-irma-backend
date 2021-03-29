# InternetNZ IRMA Backend
This software is used as a proxy between irma front-end and irma server. At this stage it is used to map SingleSource
APIs. To call the APIs you need to have access to API key.

## How to run it on your local
First, make sure to create `.env` file from `.env.sample` and set the value for `SINGLE_SOURCE_API_KEY` environment
variable.

### In a Container
You can run and manage irma backend in a container using these command:
* Create/Start your containers `docker-compose up --build -d` / `make build`
* Destroy your containers `docker-compose down` / `make down`
* Restart your containers `docker-compose restart` / `make restart`
* Stop your containers `docker-compose stop` / `make stop`
* Start your containers `docker-compose start` / `make start`

### Python Virtual Environment
This software can be run in a python virtual environment:

```
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.dev.txt
python ./runserver.py
```

Source should be accessible on http://localhost:5050

## Deployment
This software will be deployed to `inzsandbox` AWS account by Github actions.
