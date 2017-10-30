
# coding: utf-8

# In[4]:

from natasha.grammars.pipelines import CommercialOrganisationPipeline
from natasha.grammars.pipelines import AbbreviationalOrganisationPipeline
from yargy.pipeline import CustomGrammemesPipeline

new_dictionary_com = {
        "авиакомпания",
        "госкомпания",
        "инвесткомпания",
        "медиакомпания",
        "оффшор-компания",
        "радиокомпания",
        "телекомпания",
        "телерадиокомпания",
        "траст-компания",
        "фактор-компания",
        "холдинг-компания",
        "энергокомпания",
        "компания-производитель",
        "компания-изготовитель",
        "компания-заказчик",
        "компания-исполнитель",
        "компания-посредник",
        "группа_управляющий_компания",
        "агрофирма",
        "турфирма",
        "юрфирма",
        "фирма-производитель",
        "фирма-изготовитель",
        "фирма-заказчик",
        "фирма-исполнитель",
        "фирма-посредник",
        "авиапредприятие",
        "агропредприятие",
        "госпредприятие",
        "нацпредприятие",
        "промпредприятие",
        "энергопредприятие",
        "авиакорпорация",
        "госкорпорация",
        "профорганизация",
        "стартап",
        "нотариальный_контора",
        "букмекерский_контора",
        "авиазавод",
        "автозавод",
        "винзавод",
        "подстанция",
        "гидроэлектростанция"
}

new_dictionary_abbr = {
    'ик',
    'нк',
    'хк',
    'ип',
    'чп',
    'ичп',
    'гпф',
    'нпф',
    'бф',
    'спао',
    'сро',
}
new_dictionary_com.update(CommercialOrganisationPipeline.Dictionary)
new_dictionary_abbr.update(AbbreviationalOrganisationPipeline.Dictionary)

class NewCommercialOrganisationPipeline(CustomGrammemesPipeline):
    Grammemes = {
        'Orgn/Commercial',
    }
    Dictionary = new_dictionary_com
    
class NewAbbreviationalOrganisationPipeline(CustomGrammemesPipeline):
    Grammemes = {
        'Orgn/Abbr',
    }
    Dictionary = new_dictionary_abbr

