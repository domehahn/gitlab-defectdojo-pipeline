#!/bin/sh

CONTEXT_PATH="/opt/s3fs/bucket/"
DOCKERFILE_PATH="/opt/s3fs/bucket/Dockerfile"

execute_ansible() {
  cd ../ansible
  ./entrypoint.sh
}

execute_kaniko() {
  ../kaniko/executor --context dir://$CONTEXT_PATH --dockerfile $DOCKERFILE_PATH --destination "$CI_REGISTRY/$IMAGE_NAME" --cleanup --insecure
}