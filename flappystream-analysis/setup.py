from setuptools import find_namespace_packages, setup

setup(
    name="flappystream-analysis",
    author="Guillem Borrell",
    author_email="guillemborrell@gmail.com",
    packages=find_namespace_packages(),
    description="Source server for the flappystream application",
    install_requires=["pytest-asyncio", "pandas"],
    entry_points={"console_scripts":
                  ['flappystream-front = flappystream.source.main:main']},
    include_package_files=True
)
