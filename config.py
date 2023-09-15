import abc
import os
from pathlib import Path

import openai
import yaml
from log import logger

PROJECT_ROOT = Path.cwd()


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NotConfiguredException(Exception):
    """Exception raised for errors in the configuration.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="The required configuration is not set"):
        self.message = message
        super().__init__(self.message)


class Config(metaclass=Singleton):
    _instance = None
    default_yaml_file = "secret.yaml"

    def __init__(self, yaml_file=default_yaml_file):
        self._configs = {}
        self._init_with_config_files_and_env(self._configs, yaml_file)
        logger.info("Config loading done.")
        # self.global_proxy = self._get("global_proxy")
        self.openai_api_key = self._get("openai_api_key")
        if not self.openai_api_key or "your_api_key" == self.openai_api_key:
            raise NotConfiguredException("Set openai_api_key first")
        self.openai_api_base = self._get("openai_api_base")
        if not self.openai_api_base or "your_api_base" == self.openai_api_base:
            openai_proxy = self._get("openai_proxy") or self.global_proxy
            if openai_proxy:
                openai.proxy = openai_proxy
            else:
                logger.info("Set OPENAI_API_BASE in case of network issues")
        self.openai_api_rpm = self._get("rpm", 3)
        self.openai_api_model = self._get("openai_api_model", "gpt-4")
        self.max_tokens_rsp = self._get("max_tokens", 2048)

        self.serpapi_api_key = self._get("serpapi_api_key")

    def _init_with_config_files_and_env(self, configs: dict, yaml_file):
        configs.update(os.environ)

        with open(yaml_file, "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
            os.environ.update(
                {k: v for k, v in yaml_data.items() if isinstance(v, str)}
            )
            configs.update(yaml_data)

    def _get(self, *args, **kwargs):
        return self._configs.get(*args, **kwargs)

    def get(self, key, *args, **kwargs):
        value = self._get(key, *args, **kwargs)
        if value is None:
            raise ValueError(
                f"Key '{key}' not found in environment variables or in the YAML file"
            )
        return value


CONFIG = Config()


if __name__ == "__main__":
    config = Config("secret.yaml")
    secret_key = config.get("openai_api_key")
    print("Secret key:", secret_key)
