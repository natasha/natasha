from yargy import Combinator as DefaultCombinator

from natasha.grammars import (
    Person,
    Location,
    Address,
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
    PersonPositionPipeline,
)

__version__ = '0.5.0'

DEFAULT_GRAMMARS = [
    Money,
    Person,
    Location,
    Address,
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
    PersonPositionPipeline,
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
