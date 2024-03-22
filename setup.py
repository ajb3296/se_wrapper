from setuptools import setup, find_packages

setup(
    name                = 'se_wrapper',
    version             = '1.0',
    description         = 'se게시판에 쉽게 글을 쓰거나 지울 수 있는 라이브러리',
    author              = '천상의나무',
    author_email        = 'ajb8533296@gmail.com',
    url                 = 'https://github.com/ajb3296',
    install_requires    =  ["requests", "requests_toolbelt"],
    packages            = find_packages(exclude = []),
    keywords            = ['wrapper'],
    python_requires     = '>=3.10',
    package_data        = {},
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)