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
resource "aws_subnet" "emr_public_subnet" {
  vpc_id                   = aws_vpc.vpc.id
  cidr_block               = "172.31.0.0/20"
  availability_zone        = "us-east-1a"
  map_public_ip_on_launch  = true

  tags      = {
    Name    = "My Demo Subnet"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.emr_public_subnet.id
  route_table_id = aws_route_table.public-route-table.id
}

#
# Security group resources
#
resource "aws_security_group" "emr_master" {
  vpc_id                 = aws_vpc.vpc.id
  revoke_rules_on_delete = true

  tags = {
    Name = "sg-my-demo-Master"
  }
}

resource "aws_security_group" "emr_slave" {
  vpc_id                 = aws_vpc.vpc.id
  revoke_rules_on_delete = true

  tags = {
    Name = "sg-my-demo-Slave"
  }
}

# IAM role for EMR Service
resource "aws_iam_role" "iam_emr_service_role" {
  name = "iam_emr_service_role"

  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "elasticmapreduce.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "iam_emr_service_policy" {
  name = "iam_emr_service_policy"
  role = aws_iam_role.iam_emr_service_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Resource": "*",
        "Action": "*"
    }]
}
EOF
}

# IAM Role for EC2 Instance Profile
resource "aws_iam_role" "iam_emr_profile_role" {
  name = "iam_emr_profile_role"

  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "emr_profile" {
  name = "emr_profile"
  role = aws_iam_role.iam_emr_profile_role.name
}

resource "aws_iam_role_policy" "iam_emr_profile_policy" {
  name = "iam_emr_profile_policy"
  role = aws_iam_role.iam_emr_profile_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Resource": "*",
        "Action": "*"
    }]
}
EOF
}

#
# EMR resources
#
resource "aws_emr_cluster" "emr-cluster" {
  name = "my-demo-emr-cluster"
  release_label = "emr-5.31.0"
  applications  = ["Spark"]
  depends_on    = [aws_route_table.public-route-table]


  termination_protection = false
  keep_job_flow_alive_when_no_steps = true

  ec2_attributes {
    subnet_id = aws_subnet.emr_public_subnet.id
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group = aws_security_group.emr_slave.id
    instance_profile = aws_iam_instance_profile.emr_profile.arn
  }

  ebs_root_volume_size = "12"

  master_instance_group {
    name = "EMR master"
    instance_type = "m4.large"
    instance_count = "1"
  }

  core_instance_group {
    name = "EMR slave"
    instance_type = "m4.large"
    instance_count = "1"
  }

  tags = {
    Name = "My Demo Spark cluster"
  }

  service_role = aws_iam_role.iam_emr_service_role.arn
}