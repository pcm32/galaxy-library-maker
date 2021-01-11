from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


print(find_packages())

setup(
        name='galaxy-library-maker',
        version='0.0.1',
        description='Traverses directories to create Galaxy libraries',
        long_description=readme(),
        packages=find_packages(),
        install_requires=['bioblend==0.14.0'],
        author='Pablo Moreno',
        long_description_content_type='text/markdown',
        author_email='',
        scripts=['load-into-galaxy-library.py', 'get-datatypes.py'],
        license='MIT'
    )