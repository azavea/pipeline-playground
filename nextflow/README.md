# Nextflow

Here you can find a set of `Nextflow` usage examples. Each folder contains Makefile with a set of commands that should simplify the playground usage. This playground also assumes that user is familiar enough with [Nextflow](https://www.nextflow.io) or uis ready to use [Nextflow docs](https://www.nextflow.io/docs/latest/getstarted.html) as an additional source of resources to get started.

Some of playground examples may require docker container builds. Some may require `nextflow.config` changes (i.e. change the [AWS Batch configuration](https://github.com/pomadchin/pipeline-playground/blob/main/nextflow/docker-aws/nextflow.config#L3-L5)).

## Contents

- [A writeup with explanation of playgrounds represented in this folder](./adr-0002-nextflow.md)
- [tutorial](./tutorial) - The `Nextflow` [Get Started](https://www.nextflow.io/docs/latest/getstarted.html) tutorial
- [docker-tutorial](./docker-tutorial) - The [Dockerized](https://www.docker.com/) `Nextflow` [get started](https://www.nextflow.io/docs/latest/getstarted.html) tutorial
- [docker](./docker) - A more advanced [dockerized](https://www.docker.com/) pipeline example
- [docker-aws](./docker-aws) - A more advanced pipeline example that uses [AWS Batch](https://aws.amazon.com/batch/) as an execution engine
