import pytest

EXECUTOR_REPO = "public.ecr.aws/layerai/executor"


def pytest_addoption(parser):
    parser.addoption("--tag-suffix", action="store")


@pytest.fixture()
def get_full_image_name(pytestconfig):
    tag_suffix = pytestconfig.getoption("tag_suffix")

    def inner(tag_prefix: str) -> str:
        return f"{EXECUTOR_REPO}:{tag_prefix}{tag_suffix}"

    return inner
