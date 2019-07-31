#/bin/bash

docker run -it --rm \
    --name mongo-express \
    -p 8081:8081 \
    -e ME_CONFIG_OPTIONS_EDITORTHEME="ambiance" \
    -e ME_CONFIG_MONGODB_SERVER="" \
    -e ME_CONFIG_MONGODB_PORT=27017 \
    -e ME_CONFIG_MONGODB_ADMINUSERNAME="" \
    -e ME_CONFIG_MONGODB_ADMINPASSWORD="" \
    mongo-express
