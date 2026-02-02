# Changelog

All notable changes to this project will be documented in this file.

## [2.2.0](https://github.com/phergoualch/terraform-aws-service-scheduler/compare/v2.1.1...v2.2.0) (2026-02-02)

### Features

* add support for sagemaker, neptune and redshift ([e6bd9c3](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/e6bd9c3d737ca59f99267bedfdbf50a5946a430d))
* update releaserc to manage version in README and docs ([7379269](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/73792694a2a060a0f8267ebf952d751126535aa2))

## [2.1.1](https://github.com/phergoualch/terraform-aws-service-scheduler/compare/v2.1.0...v2.1.1) (2025-04-24)

### Bug Fixes

* fixed a bug on empty tags and use default value if tag value is missing ([1ea6a83](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/1ea6a837e3dac78f37005f60c423a34b8fa636a2))
* **services:** added .get to handle resource with no tags ([fddec60](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/fddec600668701b914cf4081e7fde8bbe6de8d24))
* **src:** skip resource if empty string in tag, closes [#15](https://github.com/phergoualch/terraform-aws-service-scheduler/issues/15) ([4b84d3d](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/4b84d3d68550051692e41587777bed23e56c2268))
* **terraform:** Terraform IAM permissions deprecations resolves [#13](https://github.com/phergoualch/terraform-aws-service-scheduler/issues/13) ([89bc3c1](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/89bc3c1d96b41c1576cab3255b8c3310b57c9b1f))

## [2.1.0](https://github.com/phergoualch/terraform-aws-service-scheduler/compare/v2.0.2...v2.1.0) (2024-11-22)

### Features

* added default schedule without tags ([6ca5d50](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/6ca5d50618836c4d1efd975689447662c220f1b6))
* **services:** adding elasticache support with resizing ([7f555b6](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/7f555b68aa9de1d87a59bdd5bc78d7fd76a84d28))
* **services:** adding support for scheduling cloudwatch alarms ([4f968a2](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/4f968a279bb7ebf12252f1c5c2da102e94067c48))

### Bug Fixes

* fixed a bug in the schedule time calculation when two days overlap ([f1156ec](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/f1156ec127c741af0bcab04e289de5b0c0e92f45))

## [2.0.2](https://github.com/phergoualch/terraform-aws-service-scheduler/compare/v2.0.1...v2.0.2) (2024-04-29)


### Bug Fixes

* **lambda:** fixed a bug where the timezone was not calculated correctly ([54b9c0e](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/54b9c0ef597aaaa4aa98c3cdf711e07cc97d1d3f))

## [2.0.1](https://github.com/phergoualch/terraform-aws-service-scheduler/compare/v2.0.0...v2.0.1) (2024-04-10)


### Bug Fixes

* **aurora:** added filter to avoid getting DocumentDB clusters in the request ([93936e3](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/93936e399a65ba3a22be47ed3b4daa3bbd406c5c))
* **resource:** moved  a condition to ignore a ressource if it does not have an action tag, conflicted with manual ([db28fc2](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/db28fc2ea2b707633db0f1cc0044836dd1a62d40))

## [2.0.0](https://github.com/phergoualch/terraform-aws-service-scheduler/compare/v1.0.1...v2.0.0) (2024-02-06)


### ⚠ BREAKING CHANGES

* default tags_prefix was moved to scheduler instead of finops and manual selectors format changed

### Features

* rework for v2, changed Python code, Terraform and JSON templates ([dfdde1e](https://github.com/phergoualch/terraform-aws-service-scheduler/commit/dfdde1e3889ecbae71dc9c561dcd1ac0a743e226))
