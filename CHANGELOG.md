# Changelog

All notable changes to this project will be documented in this file.

## [2.0.1](https://github.com/phergoualch/terraform-aws-service-scheduler/compare/v2.0.0...v2.0.1) (2024-04-10)


### Bug Fixes

* **aurora:** added filter to avoid getting DocumentDB clusters in the request ([93936e3](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/93936e399a65ba3a22be47ed3b4daa3bbd406c5c))
* **resource:** moved  a condition to ignore a ressource if it does not have an action tag, conflicted with manual ([db28fc2](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/db28fc2ea2b707633db0f1cc0044836dd1a62d40))

## [2.0.0](https://github.com/phergoualch/terraform-aws-service-scheduler/compare/v1.0.1...v2.0.0) (2024-02-06)


### ⚠ BREAKING CHANGES

* default tags_prefix was moved to scheduler instead of finops and manual selectors format changed

### Features

* rework for v2, changed Python code, Terraform and JSON templates ([dfdde1e](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/dfdde1e3889ecbae71dc9c561dcd1ac0a743e226))
