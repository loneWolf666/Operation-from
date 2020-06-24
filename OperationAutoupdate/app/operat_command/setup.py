# -*- coding: utf-8 -*-
# Author: WangChao
# Version: 更新数据
# Version:  fire-0.3.1 termcolor-1.1.0 fire.Fire(hello)
# click-7.1.2

from setuptools import setup

setup(
    name="operat_command",
    version="0.1",
    py_modules=["dev_command"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        dev_command=dev_command:update_dev
    """,
)
