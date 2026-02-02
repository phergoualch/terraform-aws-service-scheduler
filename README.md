# AWS Service Scheduler Terraform module

> [!NOTE]
> Full documentation can be found here: [scheduler.pereg.dev](https://scheduler.pereg.dev/)

The Service Scheduler is an open-source project developed to help scheduling AWS resources, primarily for cost-saving purposes. It is designed to be deployed in multiple accounts and regions, and to be able to start and stop resources based on their tags.

It is based on 2 services, Lambda and Step Function. The architecture is as follows:

![Architecture](https://raw.githubusercontent.com/phergoualch/terraform-aws-service-scheduler/main/docs/img/diagram-background.png)


## Usage

```hcl
module "service_scheduler" {
  source = "phergoualch/service-scheduler/aws"
  version = ">= 2.2.0"

  enabled_services   =  ["ec2", "asg", "ecs", "rds", "documentdb", "lambda", "apprunner", "aurora", "elasticache", "cloudwatch", "sagemaker-endpoint", "sagemaker-notebook", "neptune", "redshift"]
  default_timezone   = "Europe/Paris"
  app_name           = "service-scheduler"
  execution_interval = 6
}
```

## Development

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for Python linting and formatting, following industry best practices:

- **Line length**: 88 characters (Black compatible)
- **Target Python version**: 3.14
- **Comprehensive rule sets**: Pyflakes, pycodestyle, isort, and more

#### Quick Commands

```bash
# Run linter with auto-fix
make lint

# Run formatter
make format

# Run both linter and formatter
make fix

# Check code without fixing (CI mode)
make check

# Run all pre-commit hooks
make pre-commit
```

#### Pre-commit Hooks

Install pre-commit hooks to automatically check your code before committing:

```bash
make install-hooks
```

The pre-commit hooks will automatically:
- Fix import sorting
- Format Python code
- Check YAML files
- Format JSON files
- Format Terraform files
- Run security checks with Checkov

## Authors
Module is maintained by [Pereg Hergoualc'h](https://github.com/phergoualch).

## License
GNU GPLv3 Licensed. See [LICENSE](https://github.com/phergoualch/terraform-aws-service-scheduler/blob/main/LICENSE) for full details.
