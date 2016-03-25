from setuptools import setup

setup(name='countdown',
      version='0.1',
      description='Best countdown tool ever',
      url='http://github.com/aaronfc/countdown',
      author='aaronfc',
      author_email='yo@aaron.com.es',
      license='MIT',
      packages=['countdown'],
      install_requires=[
            'pygame',
            'enum34'
      ],
      dependency_links=['https://bitbucket.org/pygame/pygame/get/release_1_9_1release.zip#egg=pygame-1.9.1release'],
      zip_safe=False)
