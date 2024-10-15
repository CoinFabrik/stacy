import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

if __name__=="__main__":
    setuptools.setup(
        name='stacy-analyzer',
        author='CoinFabrik',
        author_email='',
        description='Clarity Static Analyzer',
        keywords='stacks, auditor, security, clarity, smart-contracts',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/coinfabrik/stacy',
        project_urls={
            'Documentation': 'https://github.com/coinfabrik/stacy',
            'Bug Reports':
                'https://github.com/coinfabrik/stacy/issues',
            'Source Code': 'https://github.com/coinfabrik/stacy',

        },
        package_dir={'': 'src'},
        packages=setuptools.find_packages(where='src'),
        classifiers=[
            "Intended Audience :: Developers",
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Topic :: Software Development",
            "Topic :: Utilities"
        ],
        python_requires='>=3.6',
        install_requires=['tree-sitter', 'ts-clarity==0.0.4'],
        entry_points={
            'console_scripts': [  # This can provide executable scripts
                'stacy-analyzer=stacy_analyzer:main',
            ],
        },
    )
