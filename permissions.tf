locals {
  state_machine_services_permissions = {
    # EC2 permissions
    ec2 = {
      update = [
        "ec2:StartInstances",
        "ec2:StopInstances"
      ]
    }

    # ECS permissions
    ecs = {
      describe = [
        "ecs:DescribeServices",
      ]
      update = [
        "ecs:UpdateService"
      ]
    }

    # AutoScaling permissions
    asg = {
      describe = [
        "autoscaling:DescribeAutoScalingGroups",
      ]
      update = [
        "autoscaling:UpdateAutoScalingGroup"
      ]
    }

    # App Runner permissions
    apprunner = {
      update = [
        "apprunner:PauseService",
        "apprunner:ResumeService"
      ]
    }

    # RDS permissions
    rds = {
      update = [
        "rds:StartDBInstance",
        "rds:StopDBInstance"
      ]
    }

    # Aurora permissions
    aurora = {
      update = [
        "rds:StartDBCluster",
        "rds:StopDBCluster"
      ]
    }

    # DocumentDB permissions
    documentdb = {
      update = [
        "rds:StartDBCluster",
        "rds:StopDBCluster"
      ]
    }

    # ElastiCache permissions
    elasticache = {
      update = [
        "elasticache:ModifyCacheCluster"
      ]
    }

    # Lambda permissions
    lambda = {
      update = [
        "lambda:DeleteFunctionConcurrency",
        "lambda:PutFunctionConcurrency"
      ]
    }

    # CloudWatch permissions
    cloudwatch = {
      update = [
        "cloudwatch:EnableAlarmActions",
        "cloudwatch:DisableAlarmActions"
      ]
    }
  }

  list_resources_permissions = {
    # EC2 permissions
    ec2 = [
      "ec2:DescribeInstances"
    ]

    # ECS permissions
    ecs = [
      "ecs:ListServices",
      "ecs:ListClusters",
      "ecs:ListTagsForResource"
    ]

    # AutoScaling permissions
    asg = [
      "autoscaling:DescribeAutoScalingGroups"
    ]

    # App Runner permissions
    apprunner = [
      "apprunner:ListServices",
      "apprunner:ListTagsForResource"
    ]

    # RDS permissions
    rds = [
      "rds:DescribeDBInstances",
      "rds:ListTagsForResource"
    ]

    # Aurora permissions
    aurora = [
      "rds:DescribeDBClusters",
      "rds:ListTagsForResource"
    ]

    # DocumentDB permissions
    documentdb = [
      "rds:Describe*",
      "rds:ListTagsForResource"
    ]

    # ElastiCache permissions
    elasticache = [
      "elasticache:DescribeCacheClusters",
      "elasticache:ListTagsForResource"
    ]

    # Lambda permissions
    lambda = [
      "lambda:ListFunctions",
      "lambda:ListTags"
    ]

    # CloudWatch permissions
    cloudwatch = [
      "cloudwatch:DescribeAlarms",
      "cloudwatch:ListTagsForResource"
    ]
  }
}
