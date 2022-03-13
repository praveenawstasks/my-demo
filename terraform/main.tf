provider "aws" {
  region = "us-east-1"
}

### Backend ###
# S3
###############

terraform {
  backend "s3" {
    bucket = "my-demo-terraform-state-bucket"
    key = "my-demo.tfstate"
    region = "us-east-1"
  }
}

