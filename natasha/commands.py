from setuptools import Command
from natasha import DEFAULT_PIPELINES


class BuildDictionariesCommand(Command):

    user_options = []

    def initialize_options(self):
        self.pipelines = DEFAULT_PIPELINES

    def finalize_options(self):
        pass

    def run(self):
        print('=> Building pipeline dictionaries ...')
        for pipeline in self.pipelines:
            pipeline = pipeline()
            print('Building', pipeline.__class__.__name__, '...')
            pipeline.build()
