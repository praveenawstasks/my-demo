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

# Create Internet Gateway and Attach it to VPC
# terraform aws create internet gateway
resource "aws_internet_gateway" "internet-gateway" {
  vpc_id    = aws_vpc.vpc.id

  tags      = {
    Name    = "My Demo IGW"
  }
}

# Create Route Table and Add Public Route
# terraform aws create route table
resource "aws_route_table" "public-route-table" {
  vpc_id       = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet-gateway.id
  }

  tags       = {
    Name     = "My Demo Route Table"
  }
}

# Create Private Subnet 1
# terraform aws create subnet
resource "aws_subnet" "EMR_public_subnet" {
  vpc_id                   = aws_vpc.vpc.id
  cidr_block               = "172.31.0.0/20"
  availability_zone        = "us-east-1a"
  map_public_ip_on_launch  = false

  tags      = {
    Name    = "My Demo Subnet"
  }
}