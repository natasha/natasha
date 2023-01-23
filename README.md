
<img src="https://github.com/natasha/natasha-logos/blob/master/natasha.svg">

![CI](https://github.com/natasha/yargy/actions/workflows/test.yml/badge.svg)

Natasha solves basic NLP tasks for Russian language: tokenization, sentence segmentation, word embedding, morphology tagging, lemmatization, phrase normalization, syntax parsing, NER tagging, fact extraction. Quality on every task is similar or better then current SOTAs for Russian language on news articles, see <a href="https://github.com/natasha/natasha#evaluation">evaluation section</a>. Natasha is not a research project, underlying technologies are built for production. We pay attention to model size, RAM usage and performance. Models run on CPU, use Numpy for inference.

Natasha integrates libraries from <a href="https://github.com/natasha">Natasha project</a> under one convenient API:

* <a href="https://github.com/natasha/razdel">Razdel</a> — token, sentence segmentation for Russian
* <a href="https://github.com/natasha/navec">Navec</a> — compact Russian embeddings
* <a href="https://github.com/natasha/slovnet">Slovnet</a> — modern deep-learning techniques for Russian NLP, compact models for Russian morphology, syntax, NER.
* <a href="https://github.com/natasha/yargy">Yargy</a> — rule-based fact extraction similar to Tomita parser.
* <a href="https://github.com/natasha/ipymarkup">Ipymarkup</a> — NLP visualizations for NER and syntax markups.

> ⚠ API may change, for realworld tasks consider using low level libraries from Natasha project.
> Models optimized for news articles, quality on other domain may be lower.
> To use old `NamesExtractor`, `AddressExtactor` downgrade `pip install natasha<1 yargy<0.13`

## Install

Natasha supports Python 3.7+ and PyPy3:

```bash
$ pip install natasha
```

## Usage

Import, initialize modules, build `Doc` object.

```python
>>> from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)


>>> segmenter = Segmenter()
>>> morph_vocab = MorphVocab()

>>> emb = NewsEmbedding()
>>> morph_tagger = NewsMorphTagger(emb)
>>> syntax_parser = NewsSyntaxParser(emb)
>>> ner_tagger = NewsNERTagger(emb)

>>> names_extractor = NamesExtractor(morph_vocab)

>>> text = 'Посол Израиля на Украине Йоэль Лион признался, что пришел в шок, узнав о решении властей Львовской области объявить 2019 год годом лидера запрещенной в России Организации украинских националистов (ОУН) Степана Бандеры. Свое заявление он разместил в Twitter. «Я не могу понять, как прославление тех, кто непосредственно принимал участие в ужасных антисемитских преступлениях, помогает бороться с антисемитизмом и ксенофобией. Украина не должна забывать о преступлениях, совершенных против украинских евреев, и никоим образом не отмечать их через почитание их исполнителей», — написал дипломат. 11 декабря Львовский областной совет принял решение провозгласить 2019 год в регионе годом Степана Бандеры в связи с празднованием 110-летия со дня рождения лидера ОУН (Бандера родился 1 января 1909 года). В июле аналогичное решение принял Житомирский областной совет. В начале месяца с предложением к президенту страны Петру Порошенко вернуть Бандере звание Героя Украины обратились депутаты Верховной Рады. Парламентарии уверены, что признание Бандеры национальным героем поможет в борьбе с подрывной деятельностью против Украины в информационном поле, а также остановит «распространение мифов, созданных российской пропагандой». Степан Бандера (1909-1959) был одним из лидеров Организации украинских националистов, выступающей за создание независимого государства на территориях с украиноязычным населением. В 2010 году в период президентства Виктора Ющенко Бандера был посмертно признан Героем Украины, однако впоследствии это решение было отменено судом. '
>>> doc = Doc(text)
```

### Segmentation

Split text into tokens and sentencies. Defines `tokens` and `sents` properties of `doc`. Uses <a href="https://github.com/natasha/razdel">Razdel</a> internally.

```python
>>> doc.segment(segmenter)
>>> print(doc.tokens[:5])
>>> print(doc.sents[:5])
[DocToken(stop=5, text='Посол'),
 DocToken(start=6, stop=13, text='Израиля'),
 DocToken(start=14, stop=16, text='на'),
 DocToken(start=17, stop=24, text='Украине'),
 DocToken(start=25, stop=30, text='Йоэль')]
[DocSent(stop=218, text='Посол Израиля на Украине Йоэль Лион признался, чт..., tokens=[...]),
 DocSent(start=219, stop=257, text='Свое заявление он разместил в Twitter.', tokens=[...]),
 DocSent(start=258, stop=424, text='«Я не могу понять, как прославление тех, кто непо..., tokens=[...]),
 DocSent(start=425, stop=592, text='Украина не должна забывать о преступлениях, совер..., tokens=[...]),
 DocSent(start=593, stop=798, text='11 декабря Львовский областной совет принял решен..., tokens=[...])]
```

### Morphology

For every token extract rich morphology tags. Depends on <a href="#Segmentation">segmentation</a> step. Defines `pos` and `feats` properties of `doc.tokens`. Uses <a href="https://github.com/natasha/slovnet#morphology">Slovnet morphology model</a> internally.

Call `morph.print()` to visualize morphology markup.

```python
>>> doc.tag_morph(morph_tagger)
>>> print(doc.tokens[:5])
>>> doc.sents[0].morph.print()
[DocToken(stop=5, text='Посол', pos='NOUN', feats=<Anim,Nom,Masc,Sing>),
 DocToken(start=6, stop=13, text='Израиля', pos='PROPN', feats=<Inan,Gen,Masc,Sing>),
 DocToken(start=14, stop=16, text='на', pos='ADP'),
 DocToken(start=17, stop=24, text='Украине', pos='PROPN', feats=<Inan,Loc,Fem,Sing>),
 DocToken(start=25, stop=30, text='Йоэль', pos='PROPN', feats=<Anim,Nom,Masc,Sing>)]
               Посол NOUN|Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing
             Израиля PROPN|Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing
                  на ADP
             Украине PROPN|Animacy=Inan|Case=Loc|Gender=Fem|Number=Sing
               Йоэль PROPN|Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing
                Лион PROPN|Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing
           признался VERB|Aspect=Perf|Gender=Masc|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Mid
                   , PUNCT
                 что SCONJ
...
```

### Lemmatization

Lemmatize every token. Depends on <a href="#Morphology">morphology</a> step. Defines `lemma` property of `doc.tokens`. Uses <a href="https://pymorphy2.readthedocs.io/en/stable/">Pymorphy</a> internally.

```python
>>> for token in doc.tokens:
>>>     token.lemmatize(morph_vocab)
    
>>> print(doc.tokens[:5])
>>> {_.text: _.lemma for _ in doc.tokens}
[DocToken(stop=5, text='Посол', pos='NOUN', feats=<Anim,Nom,Masc,Sing>, lemma='посол'),
 DocToken(start=6, stop=13, text='Израиля', pos='PROPN', feats=<Inan,Gen,Masc,Sing>, lemma='израиль'),
 DocToken(start=14, stop=16, text='на', pos='ADP', lemma='на'),
 DocToken(start=17, stop=24, text='Украине', pos='PROPN', feats=<Inan,Loc,Fem,Sing>, lemma='украина'),
 DocToken(start=25, stop=30, text='Йоэль', pos='PROPN', feats=<Anim,Nom,Masc,Sing>, lemma='йоэль')]
{'Посол': 'посол',
 'Израиля': 'израиль',
 'на': 'на',
 'Украине': 'украина',
 'Йоэль': 'йоэль',
 'Лион': 'лион',
 'признался': 'признаться',
 ',': ',',
 'что': 'что',
 'пришел': 'прийти',
 'в': 'в',
 'шок': 'шок',
 'узнав': 'узнать',
 'о': 'о',
...
```

### Syntax

For every sentence run syntax analyzer. Depends on <a href="#Segmentation">segmentation</a> step. Defines `id`, `head_id`, `rel` properties of `doc.tokens`. Uses <a href="https://github.com/natasha/slovnet#syntax">Slovnet syntax model</a> internally. 

Use `syntax.print()` to visualize syntax markup. Uses <a href="https://github.com/natasha/ipymarkup">Ipymarkup</a> internally.

```python
>>> doc.parse_syntax(syntax_parser)
>>> print(doc.tokens[:5])
>>> doc.sents[0].syntax.print()
[DocToken(stop=5, text='Посол', id='1_1', head_id='1_7', rel='nsubj', pos='NOUN', feats=<Anim,Nom,Masc,Sing>),
 DocToken(start=6, stop=13, text='Израиля', id='1_2', head_id='1_1', rel='nmod', pos='PROPN', feats=<Inan,Gen,Masc,Sing>),
 DocToken(start=14, stop=16, text='на', id='1_3', head_id='1_4', rel='case', pos='ADP'),
 DocToken(start=17, stop=24, text='Украине', id='1_4', head_id='1_1', rel='nmod', pos='PROPN', feats=<Inan,Loc,Fem,Sing>),
 DocToken(start=25, stop=30, text='Йоэль', id='1_5', head_id='1_1', rel='appos', pos='PROPN', feats=<Anim,Nom,Masc,Sing>)]
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
...
```

### NER

Extract standart named entities: names, locations, organizations. Depends on <a href="#Segmentation">segmentation</a> step. Defines `spans` property of `doc`. Uses <a href="https://github.com/natasha/slovnet#ner">Slovnet NER model</a> internally. 

Call `ner.print()` to visualize NER markup. Uses <a href="https://github.com/natasha/ipymarkup">Ipymarkup</a> internally.

```python
>>> doc.tag_ner(ner_tagger)
>>> print(doc.spans[:5])
>>> doc.ner.print()
[DocSpan(start=6, stop=13, type='LOC', text='Израиля', tokens=[...]),
 DocSpan(start=17, stop=24, type='LOC', text='Украине', tokens=[...]),
 DocSpan(start=25, stop=35, type='PER', text='Йоэль Лион', tokens=[...]),
 DocSpan(start=89, stop=106, type='LOC', text='Львовской области', tokens=[...]),
 DocSpan(start=152, stop=158, type='LOC', text='России', tokens=[...])]
Посол Израиля на Украине Йоэль Лион признался, что пришел в шок, узнав
      LOC────    LOC──── PER───────                                   
 о решении властей Львовской области объявить 2019 год годом лидера 
                   LOC──────────────                                
запрещенной в России Организации украинских националистов (ОУН) 
              LOC─── ORG─────────────────────────────────────── 
Степана Бандеры. Свое заявление он разместил в Twitter. «Я не могу 
PER────────────                                ORG────             
понять, как прославление тех, кто непосредственно принимал участие в 
ужасных антисемитских преступлениях, помогает бороться с 
антисемитизмом и ксенофобией. Украина не должна забывать о 
                              LOC────                      
преступлениях, совершенных против украинских евреев, и никоим образом 
не отмечать их через почитание их исполнителей», — написал дипломат. 
11 декабря Львовский областной совет принял решение провозгласить 2019
           ORG──────────────────────                                  
 год в регионе годом Степана Бандеры в связи с празднованием 110-летия
                     PER────────────                                  
 со дня рождения лидера ОУН (Бандера родился 1 января 1909 года). В 
                        ORG                                         
июле аналогичное решение принял Житомирский областной совет. В начале 
                                ORG────────────────────────           
месяца с предложением к президенту страны Петру Порошенко вернуть 
                                          PER────────────         
Бандере звание Героя Украины обратились депутаты Верховной Рады. 
PER────              LOC────                     ORG───────────  
Парламентарии уверены, что признание Бандеры национальным героем 
                                     PER────                     
поможет в борьбе с подрывной деятельностью против Украины в 
                                                  LOC────   
информационном поле, а также остановит «распространение мифов, 
созданных российской пропагандой». Степан Бандера (1909-1959) был 
                                   PER───────────                 
одним из лидеров Организации украинских националистов, выступающей за 
                 ORG─────────────────────────────────                 
создание независимого государства на территориях с украиноязычным 
населением. В 2010 году в период президентства Виктора Ющенко Бандера 
                                               PER─────────── PER──── 
был посмертно признан Героем Украины, однако впоследствии это решение 
                             LOC────                                  
было отменено судом. 
```

### Named entity normalization

For every NER span apply normalization procedure. Depends on <a href="#NER">NER</a>, <a href="#Morphology">morphology</a> and <a href="#Syntax">syntax</a> steps. Defines `normal` property of `doc.spans`.

One can not just lemmatize every token inside entity span, otherwise "Организации украинских националистов" would become "Организация украинские националисты". Natasha uses syntax dependencies to produce correct "Организация украинских националистов".

```python
>>> for span in doc.spans:
>>>    span.normalize(morph_vocab)
>>> print(doc.spans[:5])
>>> {_.text: _.normal for _ in doc.spans if _.text != _.normal}
[DocSpan(start=6, stop=13, type='LOC', text='Израиля', tokens=[...], normal='Израиль'),
 DocSpan(start=17, stop=24, type='LOC', text='Украине', tokens=[...], normal='Украина'),
 DocSpan(start=25, stop=35, type='PER', text='Йоэль Лион', tokens=[...], normal='Йоэль Лион'),
 DocSpan(start=89, stop=106, type='LOC', text='Львовской области', tokens=[...], normal='Львовская область'),
 DocSpan(start=152, stop=158, type='LOC', text='России', tokens=[...], normal='Россия')]
{'Израиля': 'Израиль',
 'Украине': 'Украина',
 'Львовской области': 'Львовская область',
 'России': 'Россия',
 'Организации украинских националистов (ОУН)': 'Организация украинских националистов (ОУН)',
 'Степана Бандеры': 'Степан Бандера',
 'Петру Порошенко': 'Петр Порошенко',
 'Бандере': 'Бандера',
 'Украины': 'Украина',
 'Верховной Рады': 'Верховная Рада',
 'Бандеры': 'Бандера',
 'Организации украинских националистов': 'Организация украинских националистов',
 'Виктора Ющенко': 'Виктор Ющенко'}
```

### Named entity parsing

Parse `PER` named entities into firstname, surname and patronymic. Depends on <a href="#NER">NER</a> step. Defines `fact` property of `doc.spans`. Uses <a href="https://github.com/natasha/yargy">Yargy-parser</a> internally.

Natasha also has built in extractors for <a href="https://nbviewer.jupyter.org/github/natasha/natasha/blob/master/docs.ipynb#DatesExtractor">dates</a>, <a href="https://nbviewer.jupyter.org/github/natasha/natasha/blob/master/docs.ipynb#MoneyExtractor">money</a>, <a href="https://nbviewer.jupyter.org/github/natasha/natasha/blob/master/docs.ipynb#AddrExtractor">address</a>.

```python
>>> for span in doc.spans:
>>>    if span.type == PER:
>>>        span.extract_fact(names_extractor)

>>> print(doc.spans[:5])
>>> {_.normal: _.fact.as_dict for _ in doc.spans if _.type == PER}
[DocSpan(start=6, stop=13, type='LOC', text='Израиля', tokens=[...], normal='Израиль'),
 DocSpan(start=17, stop=24, type='LOC', text='Украине', tokens=[...], normal='Украина'),
 DocSpan(start=25, stop=35, type='PER', text='Йоэль Лион', tokens=[...], normal='Йоэль Лион', fact=DocFact(slots=[...])),
 DocSpan(start=89, stop=106, type='LOC', text='Львовской области', tokens=[...], normal='Львовская область'),
 DocSpan(start=152, stop=158, type='LOC', text='России', tokens=[...], normal='Россия')]
{'Йоэль Лион': {'first': 'Йоэль', 'last': 'Лион'},
 'Степан Бандера': {'first': 'Степан', 'last': 'Бандера'},
 'Петр Порошенко': {'first': 'Петр', 'last': 'Порошенко'},
 'Бандера': {'last': 'Бандера'},
 'Виктор Ющенко': {'first': 'Виктор', 'last': 'Ющенко'}}
```

## Documentation

* <a href="http://nbviewer.jupyter.org/github/natasha/natasha/blob/master/docs.ipynb">Examples with description + reference</a>
* <a href="https://habr.com/ru/post/516098/#natasha">Natasha section in longread on Natasha project</a> (in Russian) 
* <a href="https://youtu.be/-7XT_U6hVvk?t=951">Natasha section of Datafest 2020 talk</a> (in Russian)

## Evaluation

* Segmentation — <a href="https://github.com/natasha/razdel#quality-performance">Razdel evalualtion section</a>
* Embedding — <a href="https://github.com/natasha/navec#evaluation">Navec evalualtion section</a>
* Morphology — <a href="https://github.com/natasha/slovnet#morphology-1">Slovnet Morph evaluation section</a>
* Syntax — <a href="https://github.com/natasha/slovnet#syntax-1">Slovnet Syntax evaluation section</a>
* NER — <a href="https://github.com/natasha/slovnet#ner-1">Slovnet NER evaluation section</a>

## Support

- Chat — https://t.me/natural_language_processing
- Issues — https://github.com/natasha/natasha/issues
- Commercial support — https://lab.alexkuk.ru

## Development

Dev env

```bash
python -m venv ~/.venvs/natasha-natasha
source ~/.venvs/natasha-natasha/bin/activate

pip install -r requirements/dev.txt
pip install -e .

python -m ipykernel install --user --name natasha-natasha
```

Test

```bash
make test
```

Docs

```bash
make exec-docs
```

Release

```bash
# Update setup.py version

git commit -am 'Up version'
git tag v1.5.0

git push
git push --tags

# Github Action builds dist and publishes to PyPi
```
