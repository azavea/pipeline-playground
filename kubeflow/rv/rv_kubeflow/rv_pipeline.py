#!/usr/bin/env python3
from typing import NamedTuple, Optional
from functools import partial

import kfp
from kfp.components import func_to_container_op, InputPath, OutputPath
from kubernetes.client.models import (
    V1EnvVar, V1Volume, V1VolumeMount, V1EnvFromSource, V1HostPathVolumeSource)
from kubernetes.client import V1SecretEnvSource

# https://stackoverflow.com/questions/5929107/decorators-with-parameters
func_to_container_op = partial(
    func_to_container_op, base_image='rv_kubeflow:latest')


@func_to_container_op
def save_config_op(raw_uri: str, root_uri: str, target: str, test: bool):
    # save the RV pipeline config to a json file before running any of the other commands
    from rv_kubeflow.spacenet_vegas import get_config
    from rv_kubeflow.utils import save_rv_pipeline_config

    runner = 'local'
    cfg = get_config(runner, raw_uri, root_uri, target=target, test=test)
    save_rv_pipeline_config(cfg)


@func_to_container_op
def rv_op(root_uri: str, command: str, split_ind: int = None, num_splits: int = None):
    from rv_kubeflow.utils import run_rv_command
    run_rv_command(root_uri, command, split_ind, num_splits)


def make_rv_op(root_uri: str, command: str, split_ind: int = None,
               num_splits: int = None):
    op = rv_op(root_uri, command, split_ind, num_splits)
    name = command if split_ind is None else f'{command}[{split_ind}]'
    op.set_display_name(name)
    return op


LogMetricsOutput = NamedTuple('LogMetricsOutput', [
    ('mlpipeline_ui_metadata', 'UI_metadata'),
    ('mlpipeline_metrics', 'Metrics')])


@func_to_container_op
def log_metrics_op(root_uri: str) -> LogMetricsOutput:
    # at the end of the pipeline, save outputs for visualization and metrics.
    from os.path import join
    import json
    from typing import NamedTuple

    from rastervision.pipeline.file_system import file_to_json

    # yes, we have to repeat this because the contents of this function cannot
    # use anything in the outer scope.
    LogMetricsOutput = NamedTuple('LogMetricsOutput', [
        ('mlpipeline_ui_metadata', 'UI_metadata'),
        ('mlpipeline_metrics', 'Metrics')])

    # there's no direct way to return an image as an output. so we have to create
    # a webpage that has the image embedded in it. this page cannot reference the file
    # system, so we need to base64 encode the image and embed in the html, which is a
    # pretty crazy hack.
    def make_img_outputs(img_uris):
        def png2html(img_path):
            import base64
            from os.path import splitext

            def get_base64_encoded_image(image_path):
                with open(image_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode('utf-8')

            encoded_img = get_base64_encoded_image(img_path)
            ext = splitext(img_path)[1]
            return f'<h3>{img_path}</h3><img src="data:image/{ext};base64,{encoded_img}"/>'

        outputs = []
        for img_uri in img_uris:
            html = png2html(img_uri)
            outputs.append({
                'type': 'web-app',
                'storage': 'inline',
                'source': html
            })
        return outputs

    # just log a few things as a test of kubeflow's capabilities. more can be added later.
    train_loader_uri = join(root_uri, 'train', 'dataloaders', 'train.png')
    test_preds_uri = join(root_uri, 'train', 'test_preds.png')
    img_uris = [train_loader_uri, test_preds_uri]
    outputs = make_img_outputs(img_uris)
    metadata = {'outputs': outputs}

    metrics_uri = join(root_uri, 'train', 'test_metrics.json')
    avg_f1 = file_to_json(metrics_uri)['avg_f1']
    metrics = {
        'metrics': [
            {
                'name': 'avg_f1',
                'numberValue':  avg_f1,
            }]
    }
    return LogMetricsOutput(json.dumps(metadata), json.dumps(metrics))


# you would think this should be a pipeline parameter, but it can't be because the value
# needs to be available at compile time, ie. when this file is executed and the yaml file
# containing the pipeline graph is created. in other words, it's not possible to control
# the structure of a graph using a pipeline parameter which is only available at
# pipeline run time.
NUM_SPLITS = 2


@kfp.dsl.pipeline(
    name='Spacenet Vegas RV Pipeline',
    description='Train a model on Spacenet Vegas'
)
def pipeline(raw_uri: str='s3://spacenet-dataset',
             root_uri: str='/opt/data/kubeflow/spacenet/',
             target: str='BUILDINGS',
             test: bool=True):
    # the general idea here is to let RV generate its own paths so that commands
    # can communicate. this goes against the kubeflow philosophy, but lets us use RV
    # as-is without any modifications. maybe we should re-examine this, but it was an
    # interesting exercise to see if this was possible.
    save_config = save_config_op(raw_uri, root_uri, target, test)
    train = make_rv_op(root_uri, 'train')
    predict_splits = []
    for split_ind in range(NUM_SPLITS):
        predict_split = make_rv_op(root_uri, 'predict', split_ind, NUM_SPLITS)
        predict_splits.append(predict_split)
    evaluation = make_rv_op(root_uri, 'eval')
    bundle = make_rv_op(root_uri, 'bundle')
    log_metrics = log_metrics_op(root_uri)

    volume = V1Volume(
        name='data', host_path=V1HostPathVolumeSource(path='/opt/data/'))
    volume_mount = V1VolumeMount(mount_path='/opt/data/', name='data')
    aws_secrets = V1EnvFromSource(
        secret_ref=V1SecretEnvSource(name='aws-secrets', optional=False))

    all_ops = [save_config, train] + predict_splits + [evaluation, bundle, log_metrics]
    for op in all_ops:
        # without this, it will try to pull the rv_kubeflow:latest image from
        # docker hub, which we don't want.
        op.container.set_image_pull_policy('IfNotPresent')
        # we need to mount volumes so steps can communicate since we're bypassing
        # kubeflows ability to automatically generate input and output paths.
        op.add_env_from(aws_secrets) \
          .add_volume(volume) \
          .add_volume_mount(volume_mount)
        # don't cache anything. this is just for making it easier to test things and
        # should be re-examined in the future.
        op.execution_options.caching_strategy.max_cache_staleness = "P0D"

    train.after(save_config)
    for predict_split in predict_splits:
        predict_split.after(train)
    evaluation.after(*predict_splits)
    bundle.after(evaluation)
    log_metrics.after(bundle)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline, __file__ + '.yaml')
