
import re

from natasha import PER, Doc


TEXT = 'Посол Израиля на Украине Йоэль Лион признался, что пришел в шок, узнав о решении властей Львовской области объявить 2019 год годом лидера запрещенной в России Организации украинских националистов (ОУН) Степана Бандеры. Свое заявление он разместил в Twitter. 11 декабря Львовский областной совет принял решение провозгласить 2019 год в регионе годом Степана Бандеры в связи с празднованием 110-летия со дня рождения лидера ОУН (Бандера родился 1 января 1909 года).'


def strip(markup):
    markup = markup.lstrip('\n')
    return re.sub(r'\s+\n', '\n', markup)


NER = strip('''
Посол Израиля на Украине Йоэль Лион признался, что пришел в шок, узнав
      LOC────    LOC──── PER───────
 о решении властей Львовской области объявить 2019 год годом лидера
                   LOC──────────────
запрещенной в России Организации украинских националистов (ОУН)
              LOC─── ORG───────────────────────────────────────
Степана Бандеры. Свое заявление он разместил в Twitter. 11 декабря
PER────────────                                ORG────
Львовский областной совет принял решение провозгласить 2019 год в
ORG──────────────────────
регионе годом Степана Бандеры в связи с празднованием 110-летия со дня
              PER────────────
 рождения лидера ОУН (Бандера родился 1 января 1909 года).
                 ORG
''')

MORPH = strip('''
               Посол NOUN|Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing
             Израиля PROPN|Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing
                  на ADP
             Украине PROPN|Animacy=Inan|Case=Loc|Gender=Fem|Number=Sing
               Йоэль PROPN|Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing
                Лион PROPN|Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing
           признался VERB|Aspect=Perf|Gender=Masc|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Mid
                   , PUNCT
                 что SCONJ
              пришел VERB|Aspect=Perf|Gender=Masc|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Act
                   в ADP
                 шок NOUN|Animacy=Inan|Case=Acc|Gender=Masc|Number=Sing
                   , PUNCT
               узнав VERB|Aspect=Perf|Tense=Past|VerbForm=Conv|Voice=Act
                   о ADP
             решении NOUN|Animacy=Inan|Case=Loc|Gender=Neut|Number=Sing
             властей NOUN|Animacy=Inan|Case=Gen|Gender=Fem|Number=Plur
           Львовской ADJ|Case=Gen|Degree=Pos|Gender=Fem|Number=Sing
             области NOUN|Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing
            объявить VERB|Aspect=Perf|VerbForm=Inf|Voice=Act
                2019 ADJ
                 год NOUN|Animacy=Inan|Case=Acc|Gender=Masc|Number=Sing
               годом NOUN|Animacy=Inan|Case=Ins|Gender=Masc|Number=Sing
              лидера NOUN|Animacy=Anim|Case=Gen|Gender=Masc|Number=Sing
         запрещенной VERB|Aspect=Perf|Case=Gen|Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part|Voice=Pass
                   в ADP
              России PROPN|Animacy=Inan|Case=Loc|Gender=Fem|Number=Sing
         Организации PROPN|Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing
          украинских ADJ|Case=Gen|Degree=Pos|Number=Plur
       националистов NOUN|Animacy=Anim|Case=Gen|Gender=Masc|Number=Plur
                   ( PUNCT
                 ОУН PROPN|Animacy=Inan|Case=Nom|Gender=Fem|Number=Sing
                   ) PUNCT
             Степана PROPN|Animacy=Anim|Case=Gen|Gender=Masc|Number=Sing
             Бандеры PROPN|Animacy=Anim|Case=Gen|Gender=Masc|Number=Sing
                   . PUNCT
''')

SYNTAX = strip('''
        ┌──► Посол         nsubj
        │    Израиля
        │ ┌► на            case
        │ └─ Украине
        │ ┌─ Йоэль
        │ └► Лион          flat:name
┌─────┌─└─── признался
│     │ ┌──► ,             punct
│     │ │ ┌► что           mark
│     └►└─└─ пришел        ccomp
│     │   ┌► в             case
│     └──►└─ шок           obl
│         ┌► ,             punct
│ ┌────►┌─└─ узнав         advcl
│ │     │ ┌► о             case
│ │ ┌───└►└─ решении       obl
│ │ │ ┌─└──► властей       nmod
│ │ │ │   ┌► Львовской     amod
│ │ │ └──►└─ области       nmod
│ └─└►┌─┌─── объявить      nmod
│     │ │ ┌► 2019          amod
│     │ └►└─ год           obj
│     └──►┌─ годом         obl
│   ┌─────└► лидера        nmod
│   │ ┌►┌─── запрещенной   acl
│   │ │ │ ┌► в             case
│   │ │ └►└─ России        obl
│ ┌─└►└─┌─── Организации   nmod
│ │     │ ┌► украинских    amod
│ │   ┌─└►└─ националистов nmod
│ │   │   ┌► (             punct
│ │   └►┌─└─ ОУН           parataxis
│ │     └──► )             punct
│ └──────►┌─ Степана       appos
│         └► Бандеры       flat:name
└──────────► .             punct
''')

LEMMAS = {
    '110-летия': '110-летие',
    'Бандеры': 'бандера',
    'Израиля': 'израиль',
    'Львовской': 'львовский',
    'Организации': 'организация',
    'России': 'россия',
    'Свое': 'свой',
    'Степана': 'степан',
    'Украине': 'украина',
    'властей': 'власть',
    'года': 'год',
    'годом': 'год',
    'декабря': 'декабрь',
    'дня': 'день',
    'запрещенной': 'запретить',
    'лидера': 'лидер',
    'националистов': 'националист',
    'области': 'область',
    'празднованием': 'празднование',
    'признался': 'признаться',
    'принял': 'принять',
    'пришел': 'прийти',
    'разместил': 'разместить',
    'регионе': 'регион',
    'решении': 'решение',
    'родился': 'родиться',
    'рождения': 'рождение',
    'связи': 'связь',
    'со': 'с',
    'узнав': 'узнать',
    'украинских': 'украинский',
    'января': 'январь'
}

NORMALS = {
    'Twitter': 'Twitter',
    'Израиля': 'Израиль',
    'Йоэль Лион': 'Йоэль Лион',
    'Львовский областной совет': 'Львовский областной совет',
    'Львовской области': 'Львовская область',
    'ОУН': 'ОУН',
    'Организации украинских националистов (ОУН)': 'Организация украинских '
    'националистов (ОУН)',
    'России': 'Россия',
    'Степана Бандеры': 'Степан Бандера',
    'Украине': 'Украина'
}

FACTS = {
    'Йоэль Лион': {'first': 'Йоэль', 'last': 'Лион'},
    'Степан Бандера': {'first': 'Степан', 'last': 'Бандера'}
}


def test_doc(segmenter, morph_vocab,
             morph_tagger, syntax_parser, ner_tagger,
             names_extractor, capsys):
    doc = Doc(TEXT)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        span.normalize(morph_vocab)
        if span.type == PER:
            span.extract_fact(names_extractor)

    for token in doc.tokens:
        token.lemmatize(morph_vocab)

    doc.ner.print()
    assert strip(capsys.readouterr().out) == NER

    sent = doc.sents[0]

    sent.morph.print()
    assert strip(capsys.readouterr().out) == MORPH

    sent.syntax.print()
    assert strip(capsys.readouterr().out) == SYNTAX

    lemmas = {
        _.text: _.lemma
        for _ in doc.tokens
        if _.text.lower() != _.lemma
    }
    assert lemmas == LEMMAS

    normals = {
        _.text: _.normal
        for _ in doc.spans
    }
    assert normals == NORMALS

    facts = {
        _.normal: _.fact.as_dict
        for _ in doc.spans
        if _.fact
    }
    assert facts == FACTS
