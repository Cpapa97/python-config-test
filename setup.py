from setuptools import setup

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()
    print(required)

setup(
    name="minnie-example-config",
    description="an experiment with build-time feature flags",
    author="Christos Papadopoulos",
    url="https://github.com/Cpapa97/python-config-test.git",
    packages=["minnie_config"],
    # include_package_data=True,
    install_requires=required,
    # extras_require={"DJ": ["datajoint==0.12.9"]},
)