FROM kaniko AS kaniko

COPY auth.json /kaniko/.docker/config.json

FROM alpine AS ansible

RUN mkdir ansible

COPY ansible ansible

WORKDIR ansible

COPY entrypoint.sh .

FROM alpine

COPY --from=kaniko kaniko kaniko
COPY --from=ansible ansible ansible

ENV S3FS_MOUNT=/opt/s3fs/bucket

VOLUME $S3FS_MOUNT

RUN apk upgrade --no-cache && \
    apk add ansible && \
    rm -rf /var/cache/apk/* && \
    chmod -R 777 ansible/ && \
    mkdir /opt/s3fs

WORKDIR ansible

#ENTRYPOINT ["./entrypoint.sh"]

# docker run \
# -v $(pwd):/workspace \
# -v $(pwd)/auth.json:/kaniko/.docker/config.json \
# gcr.io/kaniko-project/executor:latest \
# --dockerfile Dockerfile \
# --destination "host.docker.internal:8090/kaniko:latest"  --context dir:///workspace/ --insecur