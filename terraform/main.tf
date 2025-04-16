# Provider Setup
provider "aws" {
  region = "us-east-1"
}

# ECR Repository for your Docker Images
resource "aws_ecr_repository" "scw_project" {
  name = "scw-project"
}

# ECS Execution Role
resource "aws_iam_role" "ecs_execution_role" {
  name = "ecs_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Attach the required policy to the execution role
resource "aws_iam_role_policy_attachment" "ecs_execution_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ECS Task Role
resource "aws_iam_role" "ecs_task_role" {
  name = "ecs_task_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Security Group for ECS service and ALB
resource "aws_security_group" "ecs_service_sg" {
  name        = "ecs_service_sg"
  description = "Allow inbound traffic on port 8000"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Application Load Balancer (ALB) Setup
resource "aws_lb" "scw_alb" {
  name               = "scw-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.ecs_service_sg.id]
  subnets            = data.aws_subnet_ids.default.ids

  enable_deletion_protection = false
  enable_cross_zone_load_balancing = true
}

# ALB Listener (Port 8000)
resource "aws_lb_listener" "scw_listener" {
  load_balancer_arn = aws_lb.scw_alb.arn
  port              = 8000
  default_action {
    type             = "fixed-response"
    fixed_response {
      status_code = 200
      content_type = "text/plain"
      message_body = "ALB is up and running!"
    }
  }
}

# ECS Cluster Definition
resource "aws_ecs_cluster" "scw_cluster" {
  name = "scw-cluster"
}

# ECS Task Definition
resource "aws_ecs_task_definition" "scw_task" {
  family                   = "scw-task"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  network_mode             = "awsvpc"
  container_definitions    = jsonencode([
    {
      name      = "scw-service"
      image     = "${aws_ecr_repository.scw_project.repository_url}:latest"
      cpu       = 256
      memory    = 512
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    }
  ])
}

# ECS Service (Task running on ECS)
resource "aws_ecs_service" "scw_service" {
  name            = "scw-service"
  cluster         = aws_ecs_cluster.scw_cluster.id
  task_definition = aws_ecs_task_definition.scw_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnet_ids.default.ids
    security_groups = [aws_security_group.ecs_service_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.scw_target_group.arn
    container_name   = "scw-service"
    container_port   = 8000
  }
}

# Target Group for ECS Load Balancer
resource "aws_lb_target_group" "scw_target_group" {
  name     = "scw-target-group"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id
}

# Default VPC Lookup (for existing VPC)
data "aws_vpc" "default" {
  default = true
}

# Default Subnet Lookup (for existing subnets)
data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}
