# coding: utf-8
from __future__ import unicode_literals

import os

from yargy.pipeline import CustomGrammemesPipeline

DICTIONARY_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'dictionaries',
)


class CommercialOrganisationPipeline(CustomGrammemesPipeline):

    Grammemes = {
        'Orgn/Commercial',
    }
    Dictionary = {
        'агентство',
        'компания',
        'организация',
        'издание',
        'интернет-издание',
        'издательство',
        'газета',
        'концерн',
        'фирма',
        'завод',
        'торговый_дом',
        'предприятие',
        'корпорация',
        'группа',
        'группа_компания',
        'санаторий',
        'производственный_объединение',
        'совет_директор',
        'бюро',
        'подразделение',
        'филиал',
        'представительство',
        'ф-л',
        'фонд',
        'банк',
        'биржа',
        'бар',
        'ресторан',
        'клуб',
    }
    Path = os.path.join(DICTIONARY_DIRECTORY, 'orgn_commercial.dawg')


class SocialOrganisationPipeline(CustomGrammemesPipeline):

    Grammemes = {
        'Orgn/Social',
    }
    Dictionary = {
        'ассамблея',
        'оргкомитет',
        'пресс-служба',
        'подразделение',
        'комитет',
        'редакция',
        'храм',
        'центр',
        'союз',
        'совет',
        'служба',
        'театр',
        'музей',
        'общество',
        'объединение',
        'министерство',
        'правительство',
        'руководство',
        'администрация',
        'кабинет_министр',
        'правительство',
        'больница',
        'госпиталь',
        'клиника',
    }
    Path = os.path.join(DICTIONARY_DIRECTORY, 'orgn_social.dawg')


class EducationalOrganisationPipeline(CustomGrammemesPipeline):

    Grammemes = {
        'Orgn/Educational',
    }
    Dictionary = {
        'нии',
        'академия',
        'академия_наука',
        'обсерватория',
        'университет',
        'институт',
        'политех',
        'колледж',
        'техникум',
        'училище',
        'школа',
    }
    Path = os.path.join(DICTIONARY_DIRECTORY, 'orgn_educational.dawg')


class AbbreviationalOrganisationPipeline(CustomGrammemesPipeline):

    Grammemes = {
        'Orgn/Abbr',
    }
    Dictionary = {
        'ооо',
        'зао',
        'оао',
        'ао',
        'тоо',
        'фгуп',
        'пао',
        'уфпс',
        'нпо',
    }
    Path = os.path.join(DICTIONARY_DIRECTORY, 'orgn_abbr.dawg')

class PersonPositionPipeline(CustomGrammemesPipeline):

    Grammemes = {
        'Person/Position',
    }
    Dictionary = {
        'святой',

        'царь',
        'король',
        'царица',
        'император',
        'инператрица',
        'князь',
        'княгиня',
        'президент',
        'премьер-министр',
        'министр',
        'замминистр',
        'замиститель_министр',
        'глава',

        'актер',
        'актриса',
        'артист',
        'певец',
        'певица',
        'исполнитель',
        'солист',
        'режиссер',
        'сценарист',
        'писатель',
        'музыкант',
        'композитор',
        'корреспондент',
        'журналист',

        'судья',
        'юрист',
        'представитель',
        'директор',
    }
