import setuptools

setuptools.setup(
    name="iterable_orm",
    version="0.2",
    url="https://github.com/Said007/iterable_orm",

    author="Said Ali",
    author_email="said.ali@msn.com",

    description="Query API similar to Django for Python objects and dictionaries",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
