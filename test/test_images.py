import os
import warnings
from contextlib import contextmanager

import pytest

_DOCKER_CLIENT_TIMEOUT = 600  # in seconds

EXECUTOR_TAGS = ["python3.7", "python3.8", "python3.7-gpu", "python3.8-gpu"]


def _get_python_path_from_tag(tag: str) -> bool:
    if "gpu" in tag:
        return "python"
    return "/opt/python/bin/python3"


preinstalled_deps = [
    "layer",
    "scipy",
    "sklearn",
    "torch",
    "xgboost",
    "nltk",
    "tensorflow",
    "lightgbm",
    "pandas",
    "matplotlib",
    "seaborn",
]


@pytest.mark.integration()
@pytest.mark.parametrize("tag", EXECUTOR_TAGS)
@pytest.mark.parametrize("module_name", preinstalled_deps)
def test_imports(tag, get_full_image_name, module_name):
    with _run_container(
        image=get_full_image_name(tag),
        command=f"-c 'import {module_name}'",
        entrypoint=_get_python_path_from_tag(tag),
    ) as container:
        assert _wait_for_container(container) == {"Error": None, "StatusCode": 0}
        assert _container_logs(container) == b""


@pytest.mark.integration()
@pytest.mark.parametrize("tag", EXECUTOR_TAGS)
def test_layer_import(tag, get_full_image_name):
    with _run_container(
        image=get_full_image_name(tag),
        command="-c 'import layer'",
        entrypoint=_get_python_path_from_tag(tag),
    ) as container:
        assert _wait_for_container(container) == {"Error": None, "StatusCode": 0}
        assert _container_logs(container) == b""


@pytest.mark.integration()
@pytest.mark.parametrize(
    "tag, output",
    zip(
        EXECUTOR_TAGS,
        [
            b"Python 3.7.13\n",
            b"Python 3.8.13\n",
            b"Python 3.7.13\n",
            b"Python 3.8.10\n",
        ],
    ),
)
def test_python_version(tag, output, get_full_image_name):
    with _run_container(
        image=get_full_image_name(tag),
        command="--version",
        entrypoint=_get_python_path_from_tag(tag),
    ) as container:
        assert _wait_for_container(container) == {"Error": None, "StatusCode": 0}
        assert _container_logs(container) == output


@contextmanager
def _run_container(image, command, entrypoint=None):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import docker

        client = docker.from_env(timeout=_DOCKER_CLIENT_TIMEOUT)

        try:
            container = client.containers.run(
                image,
                command,
                entrypoint=entrypoint,
                detach=True,
                stdout=True,
                stderr=True,
                tty=False,
            )
            try:
                yield container
            finally:
                container.remove(force=True)
        finally:
            client.close()


def _wait_for_container(container):
    return container.wait(timeout=_DOCKER_CLIENT_TIMEOUT)


def _container_logs(container):
    return container.logs(stdout=True, stderr=True, tail=100)
