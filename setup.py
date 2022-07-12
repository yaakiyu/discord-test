from setuptools import setup, find_packages


setup(
    name="discord_test",
    packages=find_packages(),
    version="0.0.1",
    install_requires=["discord.py", "aioconsole"],
    extras_require={},
    py_modules=["discord_test"]
)
