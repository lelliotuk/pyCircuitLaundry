import setuptools

setuptools.setup(
    name='pyCircuitLaundry',
    author='lelliotuk',
    version='1.0.0',
    description='Circuit Laundry Circuit View API wrapper',
    packages=setuptools.find_packages(),
    url='https://github.com/lelliotuk/pyCircuitLaundry',
    install_requires=['requests','beautifulsoup4'],
    python_requires='>=3.0'
)