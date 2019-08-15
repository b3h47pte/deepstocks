from setuptools import setup, find_packages
setup(
    name='DeepStocks',
    version='0.0',
    packages=find_packages(),
    scripts=['apps/apiServer/apiServer.py'],
    install_requires=[
        'requests',
        'SQLAlchemy',
        'appdirs',
        'torch',
        'torchvision',
        'opencv-python',
        'matplotlib',
        'alembic',
        'flask',
    ],
)
