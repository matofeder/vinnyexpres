from setuptools import setup, find_packages


install_requires = [
    "Flask",
    "Flask-Bootstrap",
    "pytz",
    "dnspython",
    "uwsgi",
]

setup(
    name="vinny-expres-web",
    description="Vinny expres web",
    version="1.0.0",
    author="Matej Feder",
    author_email="feder.mato@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Topic :: System :: Web",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={"dev": ["twine", "wheel", "flake8", "black"]},
)
