from setuptools import find_namespace_packages, setup

setup(
    name="flappystream-worker",
    author="Guillem Borrell",
    author_email="guillemborrell@gmail.com",
    packages=find_namespace_packages(),
    description="Backend server for the flappystream application",
    install_requires=[
        "pynng",
        "click",
        "trio",
        "pytest-trio",
        "pytest-postgresql",
        "streamz",
        "numpy",
        "psycopg2",
        "flappystream-analysis",
    ],
    entry_points={
        "console_scripts": [
            "flappystream-worker = flappystream.worker.main:main",
            "flappystream-create-tables = flappystream.worker.db:create_data_tables",
        ]
    },
    include_package_files=True,
)
