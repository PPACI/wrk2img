from setuptools import setup, find_packages

with open('Readme.md') as f:
    long_desc = f.read()

setup(
    name='wrk2img',
    version='1.0.2',
    packages=find_packages(),
    url='https://github.com/PPACI/wrk2img',
    license='MIT',
    author='Pierre PACI',
    author_email='',
    description='Create beautiful graph from wrk',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    python_requires='>=3.5',
    install_requires=['matplotlib>=2.0.0'],
    entry_points={
        'console_scripts': [
            'wrk2img=wrk2img.main:cli',
        ],
    },
    classifiers=(
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Networking'
    )
)
