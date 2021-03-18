from setuptools import setup, find_packages

setup(
    name='binance-futures',
    version='1.0',
    description='Binance Futures API',
    author='Philippe Remy',
    license='MIT',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'attrs'
        'unicorn-binance-websocket-api'
    ]
)
