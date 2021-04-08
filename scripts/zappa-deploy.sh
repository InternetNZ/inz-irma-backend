#!/usr/bin/env bash
cd "$(git rev-parse --show-toplevel)" || exit

environments=( demo )

# Print script usage
function usage {
    echo
    echo "Usage is ${0} <environment> <single_source_api_key> <allowed_origins>"
    echo "Valid environments are:"
    for i in "${environments[@]}"
    do
        echo - $i
    done
    echo "single_source_api_key: Single Source API key"
    echo "allowed_origins: Allowed origins to call the APIs"
    echo
    exit 1
}

# Check parameters
if [ "$#" -ne 3 ];
    then echo "Error: Not enough parameters passed"; usage
fi

# Check passed environments against array
for item in "${environments[@]}";
do
    [[ ${1} == "${item}" ]] && current_env=${1}
done

if [ -z "${current_env}" ];
    then echo "Warning: Environment ${1} unknown"; usage
fi

if [ -z "$2" ] || [ -z "$3" ]; then
    echo "Error: Single Source API Key and Allowed Origin are required."; usage
else
    python scripts/zappa-set-secrets.py "${current_env}" --single-source-api-key "$2" --allowed-origins "$3"
fi

# Zappa deployment steps
echo "Deploying broadband map api"
zappa deploy "${current_env}"
if [ $? -eq 0 ]
then
  echo "Ran initial Zappa deployment"
else
  zappa update "${current_env}"
fi
