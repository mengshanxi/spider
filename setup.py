from distutils.core import setup

setup(
    name='spider',
    version='0.1',
    author='songtao',
    author_email='208-816@163.com',
    description='a simple printer of nested lest',
    packages=['src.config', 'src.search', 'src.util', 'src.service', 'src.model', 'src.dao'],
    platforms='python 3.6',
    py_modules=['src.task.schedule_task'],
)
