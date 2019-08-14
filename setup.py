from setuptools import setup, find_packages
setup(
    name='DeepStocks',
    version='0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'SQLAlchemy',
        'appdirs',
        'torch',
        'torchvision',
        'opencv-python',
        'matplotlib',
    ],
)
