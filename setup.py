

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='CssDeadwood',
    version='0.3.1a1',
    author='Stefaan Lippens',
    author_email='soxofaan@gmail.com',
    url='https://github.com/soxofaan/CssDeadwood/',
    packages=['cssdeadwood', 'cssdeadwood.test'],
    entry_points={
        'console_scripts': [
            'cssdeadwood = cssdeadwood.app:main',
        ],
    },
    include_package_data=True,
    license='MIT',
    keywords="css deadcode",
    description='Tool to search CSS files for unused CSS selectors.',
    long_description=open('README.rst').read(),
    install_requires=[
        "lxml >= 3.1.1",
        "cssselect >= 0.8",
    ],
    test_suite='cssdeadwood.test',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)
