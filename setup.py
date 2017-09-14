from setuptools import setup


setup(
    name='qiita-analyzer',
    version='1.0.0',
    author="Hiroshi Teraoka",
    description=("Module to analyze qiita's articles"),
    license = "MIT",
    url='https://github.com/aporo4000/qiita-analyzer',
    packages=['django-qiita-analyzer'],
    package_data={
        'qiita-analyzer': ['virtualenv.sh'],
    },
)
