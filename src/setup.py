from setuptools import setup
import os

path = os.path.dirname(os.path.realpath(__file__))+"/trafficSimulator"

setup(name="trafficSimulator",
      version="0.0",
      packages=[path])