from yargy import Parser, Combinator

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

def BUILD_DEFAULT_PIPELINES():
    return [
        pipeline() for pipeline in DEFAULT_PIPELINES
    ]
