import pytest


PYTHON_VERSIONS = ["3.7", "3.8"]
FLAVORS = ["slim", "gpu"]

FLAVOR_ENTRYPOINTS = {"slim": "/opt/python/bin/python3", "gpu": "python"}
PYTHON_PATCH_VERSIONS = {
    "3.7": {"slim": "3.7.13", "gpu": "3.7.13"},
    "3.8": {"slim": "3.8.13", "gpu": "3.8.10"},
}


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    python_version = metafunc.config.option.python_version
    if "python_version" in metafunc.fixturenames:
        metafunc.parametrize(
            "python_version", PYTHON_VERSIONS if python_version in [None, "all"] else [python_version], indirect=True
        )
    flavor = metafunc.config.option.flavor
    if "flavor" in metafunc.fixturenames:
        metafunc.parametrize("flavor", FLAVORS if flavor in [None, "all"] else [flavor], indirect=True)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--python-version", action="store", choices=["all"] + PYTHON_VERSIONS)
    parser.addoption("--flavor", action="store", choices=["all"] + FLAVORS)


@pytest.fixture(scope="session")
def python_version(request: pytest.FixtureRequest) -> str:
    """
    This fixture is parametrized by pytest_generate_tests
    By default it iterates over all python versions, but if the --python-version
    option is given, it only iterates over that version
    """
    return request.param  # type: ignore


@pytest.fixture(scope="session")
def flavor(request: pytest.FixtureRequest) -> str:
    """
    This fixture is parametrized by pytest_generate_tests
    By default it iterates over all flavors, but if the --flavor
    option is given, it only iterates over that flavor
    """
    return request.param  # type: ignore


@pytest.fixture(scope="session")
def python_entrypoint(flavor) -> str:
    return FLAVOR_ENTRYPOINTS[flavor]


@pytest.fixture(scope="session")
def python_patch_version(python_version, flavor) -> str:
    return PYTHON_PATCH_VERSIONS[python_version][flavor]
