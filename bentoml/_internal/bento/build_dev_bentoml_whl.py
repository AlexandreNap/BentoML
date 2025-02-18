import os
import uuid
import shutil
import logging
import importlib
import importlib.util

from ..configuration import is_pypi_installed_bentoml
from ..utils.tempdir import TempDirectory

logger = logging.getLogger(__name__)

BENTOML_DEV_BUILD = "BENTOML_BUNDLE_LOCAL_BUILD"


def build_bentoml_editable_wheel(target_path: str) -> None:
    """This is for BentoML developers to create Bentos that contains their local bentoml
    build base on their development branch. To enable this behavior, the developer must
    set env var BENTOML_BUNDLE_LOCAL_BUILD=True before building a Bento.

    If bentoml is installed in editor mode(pip install -e), this will build a wheel
    distribution with the local bentoml source and add it to saved bento directory
    under {bento_path}/env/python/wheels/
    """
    if str(os.environ.get(BENTOML_DEV_BUILD, False)).lower() != "true":
        return

    if is_pypi_installed_bentoml():
        # skip this entirely if BentoML is installed from PyPI
        return

    # Find bentoml module path
    (module_location,) = importlib.util.find_spec("bentoml").submodule_search_locations  # type: ignore # noqa

    bentoml_setup_py = os.path.abspath(os.path.join(module_location, "..", "setup.py"))  # type: ignore

    # this is for BentoML developer to create Service containing custom development
    # branches of BentoML library, it is True only when BentoML module is installed
    # in development mode via "pip install --editable ."
    if os.path.isfile(bentoml_setup_py):
        logger.info(
            "BentoML is installed in `editable` mode; building BentoML distribution with the local BentoML code base. The built wheel file will be included in the target bento."
        )
        # temp dir for creating the distribution
        with TempDirectory() as dist_dir:
            # Assuming developer has setuptools installed from dev-requirements.txt
            from setuptools import sandbox

            bdist_dir = os.path.join("build", str(uuid.uuid4())[0:8])

            sandbox.run_setup(  # type: ignore
                bentoml_setup_py,
                [
                    "--quiet",
                    "bdist_wheel",
                    "--dist-dir",
                    dist_dir,
                    "--bdist-dir",
                    bdist_dir,
                ],
            )
            # copy the built wheel file to target directory
            shutil.copytree(dist_dir, target_path)  # type: ignore
    else:
        logger.info(
            "Custom BentoML build is detected. For a Bento to use the same build at serving time, add your custom BentoML build to the pip packages list, e.g. `packages=['git+https://github.com/bentoml/bentoml.git@13dfb36']`"
        )
