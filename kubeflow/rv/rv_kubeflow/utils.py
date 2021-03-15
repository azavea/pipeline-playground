from os.path import join

from rastervision.pipeline.config import save_pipeline_config, build_config
from rastervision.pipeline.cli import _run_command

def save_rv_pipeline_config(cfg):
    cfg.update()
    cfg.recursive_validate_config()
    # This is to run the validation again to check any fields that may have changed
    # after the Config was constructed, possibly by the update method.
    build_config(cfg.dict())
    cfg_json_uri = cfg.get_config_uri()
    save_pipeline_config(cfg, cfg_json_uri)


def run_rv_command(root_uri, command, split_ind=None, num_splits=None):
    cfg_uri = join(root_uri, 'pipeline-config.json')
    _run_command(cfg_uri, command, split_ind, num_splits)
