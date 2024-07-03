# Gitlab Pipeline for Defectdojo
This project contains two pipeline scripts. One for the creation of the defectdojo infrastructure and one for 
uploading the scan results.

To run the `.gitlab-ci.yml` locally with `gitlab-ci-local` you have to install some additional tools.

### Install Homebrew
Homebrew is a free and open-source package manager for macOS, making it easy to install, update, and manage 
software directly from the command line. It simplifies the process of finding and installing various Unix 
tools and open-source applications that are not included in macOS by default. With a vast repository of 
software, Homebrew helps keep your system up-to-date and organized with minimal effort.
```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc

brew --version
```

### Install gitlab-ci-local
`gitlab-ci-local` is a tool that allows developers to run GitLab CI pipelines locally on their own machines. This tool 
simulates the GitLab CI/CD environment, enabling developers to test and debug their CI/CD configurations without having 
to push changes to the GitLab server. It helps in faster iteration and troubleshooting of CI/CD scripts by providing 
immediate feedback.
```shell
brew install gitlab-ci-local
```

### Install docker compose v2
Docker Compose is a tool for defining and running multi-container Docker applications. It allows you to describe the 
services that make up your application in a YAML file (`docker-compose.yml`), and then use a single command to create and 
start all the services defined. This simplifies the process of managing complex applications with multiple interconnected 
containers by providing a straightforward way to orchestrate their execution and dependencies.
```shell
brew install docker-compose
```
From July 2023 Compose V1 [stopped receiving updates](https://docs.docker.com/compose/reference/).

### Install docker buildx
Docker Buildx is an advanced Docker CLI plugin that extends the capabilities of the traditional `docker build` command. 
It enables building Docker images across multiple platforms and architectures simultaneously, utilizing features like 
BuildKit for improved performance and flexibility. Buildx simplifies the process of building, testing, and distributing 
Docker images for different environments, making it easier to support diverse deployment targets from a single build 
configuration.
```shell
brew install docker-buildx
```

### Install Taskfile
Taskfile is a configuration file used by Task, a task runner and build tool written in Go. It defines a set of tasks with 
dependencies, commands, and configurations, allowing you to automate and streamline repetitive processes such as building, 
testing, and deploying projects. Taskfile provides a clear and concise way to manage project workflows and ensures 
consistent execution across different environments.
```shell
brew install go-task/tap/go-task
brew install go-task
```

## Setup
Checkout the repository.
```shell
mkdir ~/gitlab-defectdojo-pipeline
git clone https://github.com/domehahn/gitlab-defectdojo-pipeline.git
```

After you have cloned the repository you have to setup your local registry to push the kaniko image to it. So first 
switch to the `docker-build`folder.
```shell
cd docker-build/
docker buildx use multiarch > /dev/null 2>&1 || docker buildx create --name multiarch --driver docker-container --driver-opt network=host --config buildkitd.toml --use > /dev/null 2>&1
docker buildx bake --builder multiarch -f docker-bake.hcl kaniko
```
#### Explained:
For building multiarch images you have to use `docker buildx`. To push to local registry you have to tell the builder,
that it will find the image registry on the host docker network with `network=host`. Also you have to configure the 
`buildkitd.toml` and setup the local registry. Last but not least, you have to say, that the push to the registry belongs
to unsecure (because of local registry).
```shell
[registry."host.docker.internal:5000"]
  mirrors = ["https://host.docker.internal:5000"]
  http = true
  insecure = true
```
For more information about `docker buildx bake` please have a look at the official docker documentation
[docker build bake](https://docs.docker.com/reference/cli/docker/buildx/bake/) command.

You will find two separate Gitlab-Pipeline scripts. One for creating the infrastructure and one for uploading the scan 
results. To run the infrastructure pipeline you have to go to the `.gitlab-ci-local-env` file and uncomment the first line. 
```shell
FILE=./infrastructure/.gitlab-ci-infrastructure.yml
```
This file is for the configuration of the the Gitlab-Pipeline.

Another file, called `.gitlab-ci-local-variables.yml` is for the Gitlab environment variables that can be used inside the
pipeline script.

## Run
To run the pipeline script you have to switch to the root directory and use the `gitlab-ci-local` command. After finishing
successful, you should see that every stage has been passed.
```
defectdojo_create_user                  starting alpine:latest (create_user)
defectdojo_create_user                  copied to docker volumes in 315 ms
defectdojo_create_user                  > $ apk add --no-cache curl jq
defectdojo_create_user                  > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/main/aarch64/APKINDEX.tar.gz
defectdojo_create_user                  > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/community/aarch64/APKINDEX.tar.gz
defectdojo_create_user                  > (1/12) Installing ca-certificates (20240226-r0)
defectdojo_create_user                  > (2/12) Installing brotli-libs (1.1.0-r2)
defectdojo_create_user                  > (3/12) Installing c-ares (1.28.1-r0)
defectdojo_create_user                  > (4/12) Installing libunistring (1.2-r0)
defectdojo_create_user                  > (5/12) Installing libidn2 (2.3.7-r0)
defectdojo_create_user                  > (6/12) Installing nghttp2-libs (1.62.1-r0)
defectdojo_create_user                  > (7/12) Installing libpsl (0.21.5-r1)
defectdojo_create_user                  > (8/12) Installing zstd-libs (1.5.6-r0)
defectdojo_create_user                  > (9/12) Installing libcurl (8.8.0-r0)
defectdojo_create_user                  > (10/12) Installing curl (8.8.0-r0)
defectdojo_create_user                  > (11/12) Installing oniguruma (6.9.9-r0)
defectdojo_create_user                  > (12/12) Installing jq (1.7.1-r0)
defectdojo_create_user                  > Executing busybox-1.36.1-r29.trigger
defectdojo_create_user                  > Executing ca-certificates-20240226-r0.trigger
defectdojo_create_user                  > OK: 16 MiB in 26 packages
defectdojo_create_user                  > $ TODAY=$(date +%Y-%m-%d)
defectdojo_create_user                  > $ ENDDAY=$(date +%Y-%m-%d)
defectdojo_create_user                  > $ echo "Creating DefectDojo user"
defectdojo_create_user                  > Creating DefectDojo user
defectdojo_create_user                  > $ USER_ID=$(curl --request POST "$DEFECTDOJO_URL/users/" \ # collapsed multi-line command
defectdojo_create_user                  > $ echo "DEFECTDOJO_USER_ID=$USER_ID" > artifact.env
defectdojo_create_user                  finished in 1.56 s
defectdojo_create_user                  exported artifacts in 285 ms
defectdojo_create_user                  copied artifacts to cwd in 12 ms
defectdojo_create_product_types         starting alpine:latest (create_product_types)
defectdojo_create_product_types         copied to docker volumes in 315 ms
defectdojo_create_product_types         imported artifacts in 20 ms
defectdojo_create_product_types         > $ apk add --no-cache curl jq
defectdojo_create_product_types         > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/main/aarch64/APKINDEX.tar.gz
defectdojo_create_product_types         > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/community/aarch64/APKINDEX.tar.gz
defectdojo_create_product_types         > (1/12) Installing ca-certificates (20240226-r0)
defectdojo_create_product_types         > (2/12) Installing brotli-libs (1.1.0-r2)
defectdojo_create_product_types         > (3/12) Installing c-ares (1.28.1-r0)
defectdojo_create_product_types         > (4/12) Installing libunistring (1.2-r0)
defectdojo_create_product_types         > (5/12) Installing libidn2 (2.3.7-r0)
defectdojo_create_product_types         > (6/12) Installing nghttp2-libs (1.62.1-r0)
defectdojo_create_product_types         > (7/12) Installing libpsl (0.21.5-r1)
defectdojo_create_product_types         > (8/12) Installing zstd-libs (1.5.6-r0)
defectdojo_create_product_types         > (9/12) Installing libcurl (8.8.0-r0)
defectdojo_create_product_types         > (10/12) Installing curl (8.8.0-r0)
defectdojo_create_product_types         > (11/12) Installing oniguruma (6.9.9-r0)
defectdojo_create_product_types         > (12/12) Installing jq (1.7.1-r0)
defectdojo_create_product_types         > Executing busybox-1.36.1-r29.trigger
defectdojo_create_product_types         > Executing ca-certificates-20240226-r0.trigger
defectdojo_create_product_types         > OK: 16 MiB in 26 packages
defectdojo_create_product_types         > $ TODAY=$(date +%Y-%m-%d)
defectdojo_create_product_types         > $ ENDDAY=$(date +%Y-%m-%d)
defectdojo_create_product_types         > $ echo "Creating DefectDojo product types"
defectdojo_create_product_types         > Creating DefectDojo product types
defectdojo_create_product_types         > $ source artifact.env
defectdojo_create_product_types         > $ PRODUCT_TYPE_ID=$(curl --request POST "$DEFECTDOJO_URL/product_types/" \ # collapsed multi-line command
defectdojo_create_product_types         > $ echo "DEFECTDOJO_PRODUCT_TYPE_ID=$PRODUCT_TYPE_ID" >> artifact.env
defectdojo_create_product_types         finished in 1.51 s
defectdojo_create_product_types         exported artifacts in 275 ms
defectdojo_create_product_types         copied artifacts to cwd in 11 ms
defectdojo_create_product_types_members starting alpine:latest (create_product_types_member)
defectdojo_create_product_types_members copied to docker volumes in 362 ms
defectdojo_create_product_types_members imported artifacts in 18 ms
defectdojo_create_product_types_members > $ apk add --no-cache curl jq
defectdojo_create_product_types_members > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/main/aarch64/APKINDEX.tar.gz
defectdojo_create_product_types_members > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/community/aarch64/APKINDEX.tar.gz
defectdojo_create_product_types_members > (1/12) Installing ca-certificates (20240226-r0)
defectdojo_create_product_types_members > (2/12) Installing brotli-libs (1.1.0-r2)
defectdojo_create_product_types_members > (3/12) Installing c-ares (1.28.1-r0)
defectdojo_create_product_types_members > (4/12) Installing libunistring (1.2-r0)
defectdojo_create_product_types_members > (5/12) Installing libidn2 (2.3.7-r0)
defectdojo_create_product_types_members > (6/12) Installing nghttp2-libs (1.62.1-r0)
defectdojo_create_product_types_members > (7/12) Installing libpsl (0.21.5-r1)
defectdojo_create_product_types_members > (8/12) Installing zstd-libs (1.5.6-r0)
defectdojo_create_product_types_members > (9/12) Installing libcurl (8.8.0-r0)
defectdojo_create_product_types_members > (10/12) Installing curl (8.8.0-r0)
defectdojo_create_product_types_members > (11/12) Installing oniguruma (6.9.9-r0)
defectdojo_create_product_types_members > (12/12) Installing jq (1.7.1-r0)
defectdojo_create_product_types_members > Executing busybox-1.36.1-r29.trigger
defectdojo_create_product_types_members > Executing ca-certificates-20240226-r0.trigger
defectdojo_create_product_types_members > OK: 16 MiB in 26 packages
defectdojo_create_product_types_members > $ TODAY=$(date +%Y-%m-%d)
defectdojo_create_product_types_members > $ ENDDAY=$(date +%Y-%m-%d)
defectdojo_create_product_types_members > $ echo "Creating DefectDojo product type members"
defectdojo_create_product_types_members > Creating DefectDojo product type members
defectdojo_create_product_types_members > $ source artifact.env
defectdojo_create_product_types_members > $ curl --request POST "$DEFECTDOJO_URL/product_type_members/" \ # collapsed multi-line command
defectdojo_create_product_types_members > {"id":6,"product_type":4,"user":4,"role":4}
defectdojo_create_product_types_members finished in 1.57 s
defectdojo_create_product_types_members exported artifacts in 319 ms
defectdojo_create_product_types_members copied artifacts to cwd in 9.89 ms
defectdojo_create_product               starting alpine:latest (create_product)
defectdojo_create_product               copied to docker volumes in 313 ms
defectdojo_create_product               imported artifacts in 19 ms
defectdojo_create_product               > $ apk add --no-cache curl jq
defectdojo_create_product               > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/main/aarch64/APKINDEX.tar.gz
defectdojo_create_product               > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/community/aarch64/APKINDEX.tar.gz
defectdojo_create_product               > (1/12) Installing ca-certificates (20240226-r0)
defectdojo_create_product               > (2/12) Installing brotli-libs (1.1.0-r2)
defectdojo_create_product               > (3/12) Installing c-ares (1.28.1-r0)
defectdojo_create_product               > (4/12) Installing libunistring (1.2-r0)
defectdojo_create_product               > (5/12) Installing libidn2 (2.3.7-r0)
defectdojo_create_product               > (6/12) Installing nghttp2-libs (1.62.1-r0)
defectdojo_create_product               > (7/12) Installing libpsl (0.21.5-r1)
defectdojo_create_product               > (8/12) Installing zstd-libs (1.5.6-r0)
defectdojo_create_product               > (9/12) Installing libcurl (8.8.0-r0)
defectdojo_create_product               > (10/12) Installing curl (8.8.0-r0)
defectdojo_create_product               > (11/12) Installing oniguruma (6.9.9-r0)
defectdojo_create_product               > (12/12) Installing jq (1.7.1-r0)
defectdojo_create_product               > Executing busybox-1.36.1-r29.trigger
defectdojo_create_product               > Executing ca-certificates-20240226-r0.trigger
defectdojo_create_product               > OK: 16 MiB in 26 packages
defectdojo_create_product               > $ TODAY=$(date +%Y-%m-%d)
defectdojo_create_product               > $ ENDDAY=$(date +%Y-%m-%d)
defectdojo_create_product               > $ echo "Creating DefectDojo product"
defectdojo_create_product               > Creating DefectDojo product
defectdojo_create_product               > $ source artifact.env
defectdojo_create_product               > $ PRODUCT_ID=$(curl --request POST "$DEFECTDOJO_URL/products/" \ # collapsed multi-line command
defectdojo_create_product               > $ echo "DEFECTDOJO_PRODUCT_ID=$PRODUCT_ID" >> artifact.env
defectdojo_create_product               finished in 1.53 s
defectdojo_create_product               exported artifacts in 332 ms
defectdojo_create_product               copied artifacts to cwd in 10 ms
defectdojo_create_engagement            starting alpine:latest (create_engagement)
defectdojo_create_engagement            copied to docker volumes in 310 ms
defectdojo_create_engagement            imported artifacts in 19 ms
defectdojo_create_engagement            > $ apk add --no-cache curl jq
defectdojo_create_engagement            > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/main/aarch64/APKINDEX.tar.gz
defectdojo_create_engagement            > fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/community/aarch64/APKINDEX.tar.gz
defectdojo_create_engagement            > (1/12) Installing ca-certificates (20240226-r0)
defectdojo_create_engagement            > (2/12) Installing brotli-libs (1.1.0-r2)
defectdojo_create_engagement            > (3/12) Installing c-ares (1.28.1-r0)
defectdojo_create_engagement            > (4/12) Installing libunistring (1.2-r0)
defectdojo_create_engagement            > (5/12) Installing libidn2 (2.3.7-r0)
defectdojo_create_engagement            > (6/12) Installing nghttp2-libs (1.62.1-r0)
defectdojo_create_engagement            > (7/12) Installing libpsl (0.21.5-r1)
defectdojo_create_engagement            > (8/12) Installing zstd-libs (1.5.6-r0)
defectdojo_create_engagement            > (9/12) Installing libcurl (8.8.0-r0)
defectdojo_create_engagement            > (10/12) Installing curl (8.8.0-r0)
defectdojo_create_engagement            > (11/12) Installing oniguruma (6.9.9-r0)
defectdojo_create_engagement            > (12/12) Installing jq (1.7.1-r0)
defectdojo_create_engagement            > Executing busybox-1.36.1-r29.trigger
defectdojo_create_engagement            > Executing ca-certificates-20240226-r0.trigger
defectdojo_create_engagement            > OK: 16 MiB in 26 packages
defectdojo_create_engagement            > $ TODAY=$(date +%Y-%m-%d)
defectdojo_create_engagement            > $ ENDDAY=$(date +%Y-%m-%d)
defectdojo_create_engagement            > $ echo "Creating DefectDojo engagement"
defectdojo_create_engagement            > Creating DefectDojo engagement
defectdojo_create_engagement            > $ source artifact.env
defectdojo_create_engagement            > $ ENGAGEMENT_ID=$(curl --request POST "$DEFECTDOJO_URL/engagements/" \ # collapsed multi-line command
defectdojo_create_engagement            > $ echo "DEFECTDOJO_ENGAGEMENT_ID=$ENGAGEMENT_ID" >> artifact.env
defectdojo_create_engagement            finished in 1.52 s
defectdojo_create_engagement            exported artifacts in 304 ms
defectdojo_create_engagement            copied artifacts to cwd in 12 ms
push_to_minio                           starting minio/minio:latest (push_to_minio)
push_to_minio                           copied to docker volumes in 338 ms
push_to_minio                           imported artifacts in 19 ms
push_to_minio                           > $ echo "Push artifact.env to minIO S3"
push_to_minio                           > Push artifact.env to minIO S3
push_to_minio                           > $ source artifact.env
push_to_minio                           > $ mkdir -p ~/.mc/certs/CAs
push_to_minio                           > $ echo $CERTIFICATE_BASE64 | base64 -d > ~/.mc/certs/CAs/minio.cer
push_to_minio                           > $ echo "Decoded certificate and stored in ~/.mc/certs/CAs/minio.cer"
push_to_minio                           > Decoded certificate and stored in ~/.mc/certs/CAs/minio.cer
push_to_minio                           > $ mc --insecure alias set myminio $AWS_ENDPOINT_URL $AWS_ACCESS_KEY $AWS_SECRET_KEY || (echo "Failed to set alias" && exit 1)
push_to_minio                           > Added `myminio` successfully.
push_to_minio                           > $ echo "Alias set successfully"
push_to_minio                           > Alias set successfully
push_to_minio                           > $ mc --insecure ls myminio || (echo "Failed to list buckets" && exit 1)
push_to_minio                           > [2024-06-26 13:00:57 UTC]     0B defectdojo/
push_to_minio                           > [2024-06-27 13:43:02 UTC]     0B test/
push_to_minio                           > $ echo "Buckets listed successfully"
push_to_minio                           > Buckets listed successfully
push_to_minio                           > $ mc rm --insecure --recursive --force myminio/$S3_BUCKET/ || (echo "Failed to remove objects in bucket" && exit 1)
push_to_minio                           > Removed `myminio/defectdojo/Dockerfile`.
push_to_minio                           > Removed `myminio/defectdojo/artifact.env`.
push_to_minio                           > Removed `myminio/defectdojo/trivy-container-scanning-report.json`.
push_to_minio                           > $ echo "Removed objects in bucket successfully"
push_to_minio                           > Removed objects in bucket successfully
push_to_minio                           > $ if [ -f artifact.env ]; then echo "artifact.env file exists"; else echo "artifact.env file does not exist" && exit 1; fi
push_to_minio                           > artifact.env file exists
push_to_minio                           > $ mc cp --insecure --recursive artifact.env myminio/$S3_BUCKET/ || (echo "Failed to copy files to bucket" && exit 1)
push_to_minio                           > `/gcl-builds/artifact.env` -> `myminio/defectdojo/artifact.env`
push_to_minio                           > Total: 101 B, Transferred: 101 B, Speed: 9.68 KiB/s
push_to_minio                           > $ echo "Copied files to bucket successfully"
push_to_minio                           > Copied files to bucket successfully
push_to_minio                           > $ echo $CERTIFICATE_BASE64 | base64 -d > /tmp/minio.cer
push_to_minio                           > $ export AWS_CA_BUNDLE=/tmp/minio.cer
push_to_minio                           > $ mkdir $HOME/.aws
push_to_minio                           finished in 752 ms
push_to_minio                           exported artifacts in 277 ms
push_to_minio                           copied artifacts to cwd in 9.58 ms

PASS  defectdojo_create_user                 
PASS  defectdojo_create_product_types        
PASS  defectdojo_create_product_types_members
PASS  defectdojo_create_product              
PASS  defectdojo_create_engagement           
PASS  push_to_minio                          
```