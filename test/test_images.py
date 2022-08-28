import os
import warnings
from contextlib import contextmanager

import pytest


_DOCKER_CLIENT_TIMEOUT = 600  # in seconds


@pytest.mark.integration()
def test_layer_import(python_version, flavor, python_entrypoint):
    with _run_container(
        _get_image_name(python_version, flavor),
        "-c 'import layer'",
        entrypoint=python_entrypoint,
    ) as container:
        assert _wait_for_container(container) == {"Error": None, "StatusCode": 0}
        assert _container_logs(container) == b""


@pytest.mark.integration()
def test_python_version(python_version, flavor, python_entrypoint, python_patch_version):
    expected_output = f"Python {python_patch_version}\n".encode()
    with _run_container(
        _get_image_name(python_version, flavor),
        "--version",
        entrypoint=python_entrypoint,
    ) as container:
        assert _wait_for_container(container) == {"Error": None, "StatusCode": 0}
        assert _container_logs(container) == expected_output


@pytest.mark.integration()
def test_gpu_available(python_version, flavor, python_entrypoint):
    if flavor != "gpu":
        return
    with _run_container(
        _get_image_name(python_version, flavor),
        "-c 'import tensorflow; print(tensorflow.test.is_built_with_gpu_support())'",
        entrypoint=python_entrypoint,
    ) as container:
        assert _wait_for_container(container) == {"Error": None, "StatusCode": 0}
        assert _container_logs(container) == b"True\n"


@contextmanager
def _run_container(container_image, command, entrypoint=None):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import docker

        client = docker.from_env(timeout=_DOCKER_CLIENT_TIMEOUT)

        try:
            container = client.containers.run(
                container_image,
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


def _get_image_name(python_version, flavor):
    return f"layerai/executor-python{python_version}-{flavor}:latest"


def _wait_for_container(container):
    return container.wait(timeout=_DOCKER_CLIENT_TIMEOUT)


def _container_logs(container):
    return container.logs(stdout=True, stderr=True, tail=100)


def _require_env_var(name):
    if name not in os.environ:
        raise ValueError(f"missing environment variable: {name}")
    return os.environ[name]
