from setuptools import setup, find_packages

project_name = "chat_agent"

# install the package
setup(
    name=project_name,
    description="A project that build agent for chat",
    url="https://github.com/Archermmt/DLRouter",
    author="Archer.M",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
