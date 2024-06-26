variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["kaniko"]
}

target "docker-metadata-action" {
  tags = ["aboutdevops/kaniko-ansible-s3fs:${TAG}"]
}

target "docker-local-registry" {
    tags = ["localhost:8090/test:${TAG}"]
}

target "image" {
  inherits = ["docker-local-registry"]
  contexts = {
    kaniko = "docker-image://gcr.io/kaniko-project/executor:latest"
    alpine = "docker-image://alpine:latest"
  }
  cache-to   = ["type=inline"]
  dockerfile  = "kaniko.Dockerfile"
  output     = ["type=registry"]
}

target "kaniko" {
  inherits  = ["image"]
  platforms = ["linux/amd64", "linux/arm64"]
  output    = ["type=registry"]
}