from setuptools import setup


setup(
    name="discord_test",
    version="0.0.1",
    install_requires=["discord.py"],
    extras_require={},
    entry_points={
        "console_scripts": [
            "discord_test = discord_test.__main__:main",
        ]
    }
)
