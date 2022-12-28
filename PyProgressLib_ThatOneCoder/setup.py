try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='PyProgressLib',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    version='0.0.3',
    description='A small package for progress bars and spinners with customisable graphics, on a standard terminal view.',
    license='MIT',
    author='ThatOneCoder',
    author_email='trex31415@gmail.com',
    install_requires=[
        'termcolor',
    ],
    url="https://github.com/UnethicalBear/PyProgressBar",
    download_url="https://github.com/UnethicalBear/PyProgressBar",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
)