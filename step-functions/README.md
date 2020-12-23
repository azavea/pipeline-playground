# AWS Step Functions

Here you can find a set of `AWS Step functions` usage examples. Each folder contains a set of [Terraform](https://www.terraform.io/) configuration files that take care of the AWS environment deployment.

Some of playground examples may require docker container builds. Some may require [terraform variables changes](./sfn-sqs/variable.tf).

## Contents

- [A writeup with explanation of playgrounds represented in this folder](./adr-0001-step-functions.md)
- [lambda-seq](./lambda-seq) - `AWS Batch Step functions` simple pipeline that represent itself a chain of [AWS Lambda](https://aws.amazon.com/lambda/) functions
- [lambda-batch-seq](./lambda-batch-seq) - The same `AWS Batch Step functions` from the point above but uses AWS Batch as an execution engine for the first AWS Step functions step.
- [lambda-batch-seq-sqs](./lambda-batch-seq) - Pipeline orchestration through AWS SQS, AWS Batch and AWS Lambda without AWS Step functions usage
- [sfn-sqs](./sfn-sqs) - An example with AWS SQS and AWS Lambda function that triggers AWS Step functions execution
