from yargy import Combinator as DefaultCombinator

from natasha.grammars import (
    Person,
    Geo,
    Money,
    Date,
    Brand,
    Event,
    Organisation,
)
from natasha.grammars.pipelines import (
    CommercialOrganisationPipeline,
    SocialOrganisationPipeline,
    EducationalOrganisationPipeline,
    AbbreviationalOrganisationPipeline,
)

__version__ = '0.4.1'

DEFAULT_GRAMMARS = [
    Money,
    Person,
    Geo,
    Date,
    Brand,
    Event,
    Organisation,
]

DEFAULT_PIPELINES = [
    CommercialOrganisationPipeline,
    SocialOrganisationPipeline,
    EducationalOrganisationPipeline,
    AbbreviationalOrganisationPipeline,
]


class Combinator(DefaultCombinator):

    '''
    Modified version of yargy.Combinator with applied default pipelines
    '''

    def __init__(self, classes, pipelines=None, *args, **kwargs):
        if pipelines is None:
            pipelines = self.build_default_pipelines()
        return super(Combinator, self).__init__(classes, pipelines=pipelines, *args, **kwargs)

    def build_default_pipelines(self):
        return [
            pipeline() for pipeline in DEFAULT_PIPELINES
        ]
