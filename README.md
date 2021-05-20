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

### Sign Verification
We have a small Go app as a wrapper on `irmago` libs to call `Verify` function in order to verify signatures.
Use below command to build the Go app:
```
# go build -o ./go/irma_signature_verify.so -buildmode=c-shared ./go/irma_signature_verify.go
make build-go
```

Also, make sure to download the submodules (irma-demo-schememanager):
```
# When you clone the repo
git clone --recurse-submodules https://github.com/InternetNZ/inz-irma-backend.git

# Load the submodules
git submodule update --init --recursive
```

## SingleSource API endpoints
Below API endpoints from SingleSource can be called through INZ IRMA Backend.

`NOTE:` For more details about SingleSource APIs see https://ekyc.centralityapp.com/swagger/

### /drivers-licences
Is used to verify a driver licence by the given image. The mapped endpoint on the backend is:

```
https://f9emnttxd6.execute-api.ap-southeast-2.amazonaws.com/demo/single-source/drivers-licences
```

A sample api call:
```
curl --request POST 'https://f9emnttxd6.execute-api.ap-southeast-2.amazonaws.com/demo/single-source/drivers-licences' \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: API_KEY' \
  --data-raw '{
     "country_code": "NZL",
     "document_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
  }'
```

### /passports
Is used to verify a passport by the given image. The mapped endpoint on the backend is:

```
https://f9emnttxd6.execute-api.ap-southeast-2.amazonaws.com/demo/single-source/passports
```

A sample api call:
```
curl --request POST 'https://f9emnttxd6.execute-api.ap-southeast-2.amazonaws.com/demo/single-source/passports' \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: API_KEY' \
  --data-raw '{
     "country_code": "NZL",
     "document_image": "/9j/4AAQSkZJRgABAQAAAQABAAD..."
  }'
```

### /doughnuts
Is used to verify a doughnut and  get relevant information from the doughnut. The mapped endpoint on the backend is:

```
https://f9emnttxd6.execute-api.ap-southeast-2.amazonaws.com/demo/single-source/doughnuts/{doughnut}
```

A sample api call:
```
curl --request GET 'https://f9emnttxd6.execute-api.ap-southeast-2.amazonaws.com/demo/single-source/doughnuts/EQe123312' \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: API_KEY'
```

## IRMA API endpoints
### /irma/signature/verify
This API endpoint is used to verify an IRMA signature. It receives a signature payload for the input.

```
https://f9emnttxd6.execute-api.ap-southeast-2.amazonaws.com/demo/irma/signature/verify'
```

## Deployment
This software will be deployed to `inzsandbox` AWS account by Github actions.
