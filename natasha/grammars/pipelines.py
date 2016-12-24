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
        'общество',
        'объединение',
        'министерство',
        'правительство',
        'руководство',
        'администрация',
        'кабинет_министр',
        'правительство',
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
