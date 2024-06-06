# Specify the AWS provider and the region where resources will be created
provider "aws" {
    retion = "us-west-2"
}

# Define the EKS (Elastic Kubernetes Service) cluster resource
resource "aws_eks_cluster" "this" {
    name = "text-gen-cluster"       # Name of the EKS cluster
    role_arn = aws_iam_role.eks.arn # ARN of the IAM role for the EKS cluster to assume

    # VPC configuration for the EKS cluster, spcifying the subnets to use
    vpc_config {
        subnet_ids = ["subnet-12345", "subnet-67890"] # List of subnet IDs in which the EKS cluster will operate
    }
}

# Define the IAM role for the EKS cluster
resource "aws_iam_role" "eks" {
    name = "eks-role"               # Name of the IAM role

    # Policy that allows the EKS service to assume this role
    assume_role_policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow"
                "Principal": {
                    "Service": "eks.amazonaws.com"  # Principal service that is allowed to assume the role (EKS)
                },
                "Action": "sts:AssumeRole"          # Action that is allowed (AssumeRole) 
            }
        ]
    }
EOF
}