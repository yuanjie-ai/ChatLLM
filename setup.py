#!/usr/bin/env python

"""The setup script."""
import time
import pandas as pd
from pathlib import Path
from setuptools import setup, find_packages

DIR = Path(__file__).resolve().parent
version = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())

with open('README.md') as readme_file:
    readme = readme_file.read()

get_requirements = lambda p='requirements.txt': pd.read_csv(p, comment='#', names=['name']).name.tolist()
extras_require = {v.name.split('_')[1][:-4]: get_requirements(v) for v in DIR.glob('requirements_*')}
extras_require['all'] = list(set(sum(extras_require.values(), [])))

setup(
    author="yuanjie",
    author_email='313303303@qq.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Create a Python package.",
    entry_points={
        'console_scripts': [
            'chatllm-run=chatllm.clis.cli:cli'
        ],
    },
    setup_requires=["pandas"],
    install_requires=get_requirements(),
    extras_require=extras_require,  # pip install -U meutils\[all\]
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='chatllm',
    name='chatllm',
    # name='llm2openai',  # 抢占包

    packages=find_packages(include=['chatllm', 'chatllm.*']),

    test_suite='tests',
    url='https://github.com/yuanjie-ai/ChatLLM',
    version=version,  # '0.0.0',
    zip_safe=False,
)
