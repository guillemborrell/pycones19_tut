from setuptools import find_namespace_packages, setup

setup(
    name="flappystream-source",
    author="Guillem Borrell",
    author_email="guillemborrell@gmail.com",
    packages=find_namespace_packages(),
    description="Source server for the flappystream application",
    install_requires=["starlette", "uvicorn", "pynng", "click", "trio", "ujson", "aiofiles", "jinja2"],
    entry_points={"console_scripts":
                  ['flappystream-front = flappystream.source.main:main']},
    include_package_files=True
)
