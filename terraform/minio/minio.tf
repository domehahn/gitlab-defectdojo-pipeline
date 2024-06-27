resource "minio_s3_bucket" "state_terraform_s3" {
  bucket = "test"
  acl    = "public"
}