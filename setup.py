

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='CssDeadwood',
    version='0.2.4',
    author='Stefaan Lippens',
    author_email='soxofaan@gmail.com',
    url='https://github.com/soxofaan/CssDeadwood/',
    packages=['cssdeadwood', 'cssdeadwood.test'],
    scripts=['bin/cssdeadwood'],
    license='MIT',
    keywords="css deadcode",
    description='Tool to search for unused CSS selectors.',
    long_description=open('README.rst').read(),
    install_requires=[
        "lxml >= 3.1.1",
        "cssselect >= 0.8",
    ],
    test_suite='cssdeadwood.test'
)
