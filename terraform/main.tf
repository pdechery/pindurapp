terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.22.1"
    }
  }

  required_version = ">= 1.14.0"
}

provider "aws" {
  region = "us-east-2"
}

data "aws_vpc" "default" {
  default = true
}

resource "aws_instance" "pindurapp" {
  ami           = "ami-025ca978d4c1d9825"
  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.mlsecgrp.id]

  tags = {
    Name = "PindurappEC2"
  }
}

resource "aws_security_group" "mlsecgrp" {
  name = "pindurapp_ec2"
  tags = {
    Terraform = "true"
  }
  vpc_id = data.aws_vpc.default.id
}

resource "aws_security_group_rule" "postgres_in" {
  description = "Allow Postgres"
  type              = "ingress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.mlsecgrp.id
}

resource "aws_security_group_rule" "ssh_in" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.mlsecgrp.id
}

resource "aws_security_group_rule" "all_out" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.mlsecgrp.id
}

