#!/bin/bash

# Source environment variables from set_env.sh in this directory.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/set_env.sh"

cd "$HYGIENE_DIR"
docker-compose pull hygiene

# Start the hygiene container in detached mode
docker-compose up -d hygiene

# create local output dir
mkdir -p "$OUTPUT_DIR"

# create container dirs
docker exec hygiene mkdir /input
docker exec hygiene mkdir /output

# Copy repo contents to container
docker cp "$REPO_DIR" hygiene:"/input/$ONTPUB_FAMILY"

# Run the hygiene tests in the container
docker exec hygiene /publisher/publish.sh hygiene

# Copy results to the local output dir
docker cp hygiene:"/output/$ONTPUB_FAMILY" "$OUTPUT_DIR"

docker-compose down

npx verify-junit-xml "$OUTPUT_DIR/$ONTPUB_FAMILY/ontology/"*"/latest/hygiene_test.dev.xml"
