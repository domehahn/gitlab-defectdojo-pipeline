# Gitlab Pipeline for Defectdojo
This project contains two pipeline scripts. One for the creation of the defectdojo infrastructure and one for 
uploading the scan results.

To run the `.gitlab-ci.yml` you have first to install some additional tools.

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
`buildkitd.toml` an setup the local registry.
```shell
[registry."host.docker.internal:5000"]
  mirrors = ["https://host.docker.internal:5000"]
  http = true
  insecure = true
```