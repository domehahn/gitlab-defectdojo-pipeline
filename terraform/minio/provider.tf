terraform {
  required_providers {
    minio = {
      source = "aminueza/minio"
      version = "2.3.2"
    }
  }
}

provider minio {
  // required
  minio_server   = "minio:9000"
  minio_user     = var.minio_admin_username
  minio_password = var.minio_admin_password
}