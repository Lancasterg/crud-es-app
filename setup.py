from setuptools import setup, find_packages

setup(
    name='crud fs elasticsearch app',
    version=open('VERSION', 'r').read().strip(),
    long_description=__doc__,
    packages=find_packages(),
    python_version='>=3.8',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'behave==1.2.6',
        'Flask-RESTful==0.3.9',
        'Flask-Testing==0.8.1',
        'elasticsearch==7.13.1'
    ],
    entry_points={
        'console_scripts': [
            'run_server=src.run.run_flask_server:main'
        ]

    }




)
