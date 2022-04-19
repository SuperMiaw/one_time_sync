from setuptools import setup, find_packages

setup(
    name="one_time_sync",

    version="2.1.0",

    description="Retrieve only one time remote files and folders from a remote host.",

    author="SuperMiaw",

    # classifers=[
    #
    # ],

    python_requires='>=3.4',

    install_requires=[
        'paramiko',
        'configobj',
        'deluge-client'
    ],

    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'one_time_sync': [
            'one_time_sync=one_time_sync:main'
        ]
    }
)
