resource "aws_s3_bucket" "my_bucket" {
  bucket = "my_bucket_name634"

  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket_object" "file_upload" {
  bucket = "my_bucket"
  key    = "code"
  source = "driver_job.py"
}

output "my_bucket_file_version" {
  value = "${aws_s3_bucket_object.file_upload.version_id}"
}