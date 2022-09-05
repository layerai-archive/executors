import argparse
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from urllib import request

LAYER_REQUIREMENTS_FILE_NAME = "layer.txt"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_url")
    args = parser.parse_args()

    zip_url = args.zip_url

    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path, _ = request.urlretrieve(zip_url)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)

        # TODO: remove once we no longer want to support old SDK versions
        layer_requirements_file_path = Path(tmp_dir) / LAYER_REQUIREMENTS_FILE_NAME
        if os.path.exists(layer_requirements_file_path):
            pip_install = [
                sys.executable,
                "-m",
                "pip",
                "--quiet",
                "--disable-pip-version-check",
                "--no-color",
                "install",
                "--requirement",
                LAYER_REQUIREMENTS_FILE_NAME,
            ]

            result = subprocess.run(
                pip_install, text=True, check=False, capture_output=True, cwd=tmp_dir
            )

            if result.returncode != 0:
                raise Exception(
                    f"package instalation failed:\n{result.stdout}\n{result.stderr}"
                )

        # TODO: Once we remove the build-in layer package from the executor, we should be able to replace
        # spawning a new process with the following:

        # user_site = site.getusersitepackages()
        # if user_site not in sys.path:
        #     sys.path.append(user_site)
        # from layer.executables.runtime import BaseFunctionRuntime
        # BaseFunctionRuntime.main()

        # For now, spawn a child process as otherwise we end up loading the old version

        run = [sys.executable, "-m", "layer.executables.runtime", zip_url]
        result = subprocess.run(run, check=False)
        exit(result.returncode)
