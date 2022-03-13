provider "aws" {
  region = "us-east-1"
}

### Backend ###
# S3 for terraform state
###############


terraform {
  backend "s3" {
    bucket = "my-demo-terraform-state-bucket"
    key = "my-demo.tfstate"
    region = "us-east-1"
  }
}

#module "vpc" {
#  source = "terraform_modules/aws-vpc"
#
#  vpc-location                        = "Virginia"
#  namespace                           = "my-demo-emr-vpc"
#  name                                = "vpc"
#  stage                               = "main"
#  vpc-cidr                            = "172.31.0.0/16"
#}
resource "aws_vpc" "vpc" {
  cidr_block           = "172.31.0.0/16"

  tags      = {
    Name    = "My Demo EMR VPC"
  }
}