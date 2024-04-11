from setuptools import setup, find_packages

setup(
    name='kanban',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'requests',
        'typer',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'kanban = kanban.main:app',
        ],
    },
)
