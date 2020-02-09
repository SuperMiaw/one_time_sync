from setuptools import setup, find_packages

setup(
    name="one_time_sync",

    version="1.0.0",

    description="Retreive only one time remote files and folders from a remote host.",

    author="SuperMiaw",

    # classifers=[
    #
    # ],

    install_requires=[
        'paramiko',
        'enum34',
        'configobj'
    ],

    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'one_time_sync': [
            'one_time_sync=one_time_sync:main'
        ]
    }
)