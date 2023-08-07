from setuptools import setup

setup(
    name='ffconverter',
    version='0.1',
    description='file format converter',
    url='https://github.com/saikrishnacom/File-Format-Converter',
    author='srinivas',
    author_email='srinivas@example.com',
    license='MIT',
    packages=['ffconverter'],
    install_reqires=[
          "pandas<=1.5.10"
      ],
    zip_safe=False,
   entry_points = {
        'console_scripts': ['ffconverter=ffconverter:main'],
    }
)