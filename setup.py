from setuptools import setup, find_packages


install_requires = [
    "Flask==3.1.3",
    "Flask-Bootstrap==3.3.7.1",
    "python-dotenv==1.2.2",
    "pytz==2026.2",
    "dnspython==2.8.0",
    "uwsgi==2.0.31",
]

setup(
    name="vinny-expres-web",
    description="Vinny expres web",
    version="1.0.0",
    author="Matej Feder",
    author_email="feder.mato@gmail.com",
    python_requires=">=3.9",
    classifiers=[
        "Topic :: System :: Web",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={"dev": ["twine", "wheel", "flake8", "black"]},
)
