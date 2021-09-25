from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Decentralised Issue Tracking System. Developed as a part of dissertation.'

setup(
    name='Git Issues',
    version='1.0.0',
    author='Varun Kumar Kadambala',
    author_email='varunkmr26@gmail.com',
    url='https://github.com/varunkumarkadambala/git-dit',
    description='Python package for DIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'git-issue = git_issue.git_issue:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='python git issue-tracker decentralised strathclyde',
    install_requires=requirements,
    zip_safe=False
)
