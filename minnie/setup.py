from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()
    print(required)

setup(
    name="minnie",
    description="an experiment with build-time feature flags",
    author="Christos Papadopoulos",
    url="https://github.com/Cpapa97/python-config-test.git",
    packages=find_packages(),
    # include_package_data=True,
    install_requires=required,
    # extras_require={"DJ": ["datajoint==0.12.9"]},
    # cmdclass={"test": PyTest}, # Could use a similar command to only install the config?
)