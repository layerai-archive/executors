import os
import warnings
from contextlib import contextmanager

import pytest


_DOCKER_CLIENT_TIMEOUT = 600  # in seconds


python_versions = ["python3.7", "python3.8"]


@pytest.mark.integration()
@pytest.mark.parametrize("python_version", python_versions)
def test_layer_import(python_version):
    with _run_container(
        "-c 'import layer'", python_version, entrypoint="/opt/python/bin/python3"
    ) as container:
        assert _wait_for_container(container) == {"Error": None, "StatusCode": 0}
        assert _container_logs(container) == b""


@pytest.mark.integration()
@pytest.mark.parametrize(
    "python_version, output",
    zip(python_versions, [b"Python 3.7.13\n", b"Python 3.8.13\n"]),
)
def test_python_version(python_version, output):
    with _run_container(
        "--version", python_version, entrypoint="/opt/python/bin/python3"
    ) as container:
        assert _wait_for_container(container) == {"Error": None, "StatusCode": 0}
        assert _container_logs(container) == output


@contextmanager
def _run_container(command, python_version, entrypoint=None):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import docker

        client = docker.from_env(timeout=_DOCKER_CLIENT_TIMEOUT)

        try:
            container_image = f"layerai/executor-{python_version}:latest"
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


def _wait_for_container(container):
    return container.wait(timeout=_DOCKER_CLIENT_TIMEOUT)


def _container_logs(container):
    return container.logs(stdout=True, stderr=True, tail=100)


def _require_env_var(name):
    if name not in os.environ:
        raise ValueError(f"missing environment variable: {name}")
    return os.environ[name]
