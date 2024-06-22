# Specify the AWS provider and the region where resources will be created
provider "aws" {
    region = "us-west-2"
}

# Define the EKS (Elastic Kubernetes Service) cluster resource
resource "aws_eks_cluster" "this" {
    name = "example-cluster"
    role_arn = aws_iam_role.eks.arn

    vpc_config {
        subnet_ids = ["subnet-12345", "subnet-67890"]
    }
}

# Define the IAM role for the EKS cluster
resource "aws_iam_role" "eks" {
    name = "example-eks-role"

    assume_role_policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "eks.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    EOF
}
