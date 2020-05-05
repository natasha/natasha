
<img src="https://github.com/natasha/natasha-logos/blob/master/natasha.svg">

![CI](https://github.com/natasha/natasha/workflows/CI/badge.svg) [![codecov](https://codecov.io/gh/natasha/natasha/branch/master/graph/badge.svg)](https://codecov.io/gh/natasha/natasha)

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

Natasha supports Python 3.5+ and PyPy3:

```bash
$ pip install natasha
```

## Usage

For more examples and explanation see [Natasha documentation](http://nbviewer.jupyter.org/github/natasha/natasha/blob/master/docs.ipynb).

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


#######
#
#  INIT
#
#####


>>> segmenter = Segmenter()
>>> morph_vocab = MorphVocab()

>>> emb = NewsEmbedding()
>>> morph_tagger = NewsMorphTagger(emb)
>>> syntax_parser = NewsSyntaxParser(emb)
>>> ner_tagger = NewsNERTagger(emb)

>>> names_extractor = NamesExtractor(morph_vocab)

>>> text = 'Посол Израиля на Украине Йоэль Лион признался, что пришел в шок, узнав о решении властей Львовской области объявить 2019 год годом лидера запрещенной в России Организации украинских националистов (ОУН) Степана Бандеры. Свое заявление он разместил в Twitter. «Я не могу понять, как прославление тех, кто непосредственно принимал участие в ужасных антисемитских преступлениях, помогает бороться с антисемитизмом и ксенофобией. Украина не должна забывать о преступлениях, совершенных против украинских евреев, и никоим образом не отмечать их через почитание их исполнителей», — написал дипломат. 11 декабря Львовский областной совет принял решение провозгласить 2019 год в регионе годом Степана Бандеры в связи с празднованием 110-летия со дня рождения лидера ОУН (Бандера родился 1 января 1909 года). В июле аналогичное решение принял Житомирский областной совет. В начале месяца с предложением к президенту страны Петру Порошенко вернуть Бандере звание Героя Украины обратились депутаты Верховной Рады. Парламентарии уверены, что признание Бандеры национальным героем поможет в борьбе с подрывной деятельностью против Украины в информационном поле, а также остановит «распространение мифов, созданных российской пропагандой». Степан Бандера (1909-1959) был одним из лидеров Организации украинских националистов, выступающей за создание независимого государства на территориях с украиноязычным населением. В 2010 году в период президентства Виктора Ющенко Бандера был посмертно признан Героем Украины, однако впоследствии это решение было отменено судом. '
>>> doc = Doc(text)


#######
#
#  SEGMENT
#
#####


>>> doc.segment(segmenter)
>>> display(doc.tokens[:5])
>>> display(doc.sents[:5])
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


#######
#
#   MORPH
#
#####


>>> doc.tag_morph(morph_tagger)
>>> display(doc.tokens[:5])
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


######
#
#  LEMMA
#
#######


>>> for token in doc.tokens:
>>>     token.lemmatize(morph_vocab)
    
>>> display(doc.tokens[:5])
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


#######
#
#  SYNTAX
#
######


>>> doc.parse_syntax(syntax_parser)
>>> display(doc.tokens[:5])
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


#######
#
#   NER
#
######


>>> doc.tag_ner(ner_tagger)
>>> display(doc.spans[:5])
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


#######
#
#   PHRASE NORM
#
#######


>>> for span in doc.spans:
>>>    span.normalize(morph_vocab)
>>> display(doc.spans[:5])
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


#######
#
#  FACT
#
######


>>> for span in doc.spans:
>>>    if span.type == PER:
>>>        span.extract_fact(names_extractor)
>>> {_.normal: _.fact for _ in doc.spans if _.type == PER}
{'Йоэль Лион': Name(
     first='Йоэль',
     last='Лион'
 ),
 'Степан Бандера': Name(
     first='Степан',
     last='Бандера'
 ),
 'Петр Порошенко': Name(
     first='Петр',
     last='Порошенко'
 ),
 'Бандера': Name(
     last='Бандера'
 ),
 'Виктор Ющенко': Name(
     first='Виктор',
     last='Ющенко'
 )}

```

## Evaluation

### Segmentation

Natasha uses <a href="https://github.com/natasha/razdel">Razdel</a> for text segmentation.

`errors` — number of errors aggregated over 4 datasets, see <a href="https://github.com/natasha/razdel#quality-performance">Razdel evalualtion section</a> for more info.

<!--- token --->
<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>errors</th>
      <th>time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>razdel.tokenize</th>
      <td>5439</td>
      <td>9.898350</td>
    </tr>
    <tr>
      <th>mystem</th>
      <td>12192</td>
      <td>17.210470</td>
    </tr>
    <tr>
      <th>spacy</th>
      <td>12288</td>
      <td>19.920618</td>
    </tr>
    <tr>
      <th>nltk.word_tokenize</th>
      <td>130119</td>
      <td>12.405366</td>
    </tr>
  </tbody>
</table>
<!--- token --->

<!--- sent --->
<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>errors</th>
      <th>time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>razdel.sentenize</th>
      <td>32106</td>
      <td>21.989045</td>
    </tr>
    <tr>
      <th>deeppavlov/rusenttokenize</th>
      <td>41722</td>
      <td>32.535322</td>
    </tr>
    <tr>
      <th>nltk.sent_tokenize</th>
      <td>60378</td>
      <td>29.916063</td>
    </tr>
  </tbody>
</table>
<!--- sent --->

### Embedding

Natasha uses <a href="https://github.com/natasha/navec">Navec pretrained embeddings</a>.

`precision` — Average precision over 4 datasets, see <a href="https://github.com/natasha/navec#evaluation">Navec evalualtion section</a> for more info.

<!--- emb1 --->
<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>type</th>
      <th>precision</th>
      <th>init, s</th>
      <th>disk, mb</th>
      <th>ram, mb</th>
      <th>vocab</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>hudlit_12B_500K_300d_100q</th>
      <td>navec</td>
      <td>0.825</td>
      <td>1.0</td>
      <td>50.6</td>
      <td>95.3</td>
      <td>500K</td>
    </tr>
    <tr>
      <th>news_1B_250K_300d_100q</th>
      <td>navec</td>
      <td>0.775</td>
      <td>0.5</td>
      <td>25.4</td>
      <td>47.7</td>
      <td>250K</td>
    </tr>
    <tr>
      <th>ruscorpora_upos_cbow_300_20_2019</th>
      <td>w2v</td>
      <td>0.777</td>
      <td>12.1</td>
      <td>220.6</td>
      <td>236.1</td>
      <td>189K</td>
    </tr>
    <tr>
      <th>ruwikiruscorpora_upos_skipgram_300_2_2019</th>
      <td>w2v</td>
      <td>0.776</td>
      <td>15.7</td>
      <td>290.0</td>
      <td>309.4</td>
      <td>248K</td>
    </tr>
    <tr>
      <th>tayga_upos_skipgram_300_2_2019</th>
      <td>w2v</td>
      <td>0.795</td>
      <td>15.7</td>
      <td>290.7</td>
      <td>310.9</td>
      <td>249K</td>
    </tr>
    <tr>
      <th>tayga_none_fasttextcbow_300_10_2019</th>
      <td>fasttext</td>
      <td>0.706</td>
      <td>11.3</td>
      <td>2741.9</td>
      <td>2746.9</td>
      <td>192K</td>
    </tr>
    <tr>
      <th>araneum_none_fasttextcbow_300_5_2018</th>
      <td>fasttext</td>
      <td>0.720</td>
      <td>7.8</td>
      <td>2752.1</td>
      <td>2754.7</td>
      <td>195K</td>
    </tr>
  </tbody>
</table>
<!--- emb1 --->

### Morphology

Natasha uses <a href="https://github.com/natasha/slovnet#morphology">Slovnet morphology tagger</a>.

`accuracy` — accuracy on news dataset, see <a href="https://github.com/natasha/slovnet#morphology-1">Slovnet evaluation section</a> for more.

<!--- morph1 --->
<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>accuracy</th>
      <th>init, s</th>
      <th>disk, mb</th>
      <th>ram, mb</th>
      <th>speed, sents/s</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>slovnet</th>
      <td>0.961</td>
      <td>1.0</td>
      <td>27</td>
      <td>115</td>
      <td>532.0</td>
    </tr>
    <tr>
      <th>deeppavlov_bert</th>
      <td>0.951</td>
      <td>20.0</td>
      <td>1393</td>
      <td>8704</td>
      <td>85.0 (gpu)</td>
    </tr>
    <tr>
      <th>deeppavlov</th>
      <td>0.940</td>
      <td>4.0</td>
      <td>32</td>
      <td>10240</td>
      <td>90.0 (gpu)</td>
    </tr>
    <tr>
      <th>spacy</th>
      <td>0.919</td>
      <td>10.9</td>
      <td>89</td>
      <td>579</td>
      <td>30.6</td>
    </tr>
    <tr>
      <th>udpipe</th>
      <td>0.918</td>
      <td>6.9</td>
      <td>45</td>
      <td>242</td>
      <td>56.2</td>
    </tr>
  </tbody>
</table>
<!--- morph1 --->

### Syntax

Natasha uses <a href="https://github.com/natasha/slovnet#syntax">Slovnet syntax parser</a>.

`uas`, `las` — accuracy on news dataset, see <a href="https://github.com/natasha/slovnet#syntax-1">Slovnet evaluation section</a> for more.

<!--- syntax1 --->
<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>uas</th>
      <th>las</th>
      <th>init, s</th>
      <th>disk, mb</th>
      <th>ram, mb</th>
      <th>speed, sents/s</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>slovnet</th>
      <td>0.907</td>
      <td>0.880</td>
      <td>1.0</td>
      <td>27</td>
      <td>125</td>
      <td>450.0</td>
    </tr>
    <tr>
      <th>deeppavlov_bert</th>
      <td>0.962</td>
      <td>0.910</td>
      <td>34.0</td>
      <td>1427</td>
      <td>8704</td>
      <td>75.0 (gpu)</td>
    </tr>
    <tr>
      <th>spacy</th>
      <td>0.876</td>
      <td>0.818</td>
      <td>10.9</td>
      <td>89</td>
      <td>579</td>
      <td>31.6</td>
    </tr>
    <tr>
      <th>udpipe</th>
      <td>0.873</td>
      <td>0.823</td>
      <td>6.9</td>
      <td>45</td>
      <td>242</td>
      <td>56.2</td>
    </tr>
  </tbody>
</table>
<!--- syntax1 --->

### NER

Natasha uses <a href="https://github.com/natasha/slovnet#ner">Slovnet NER tagger</a>.

`f1` — score aggregated over 4 datasets, see <a href="https://github.com/natasha/slovnet#ner-1">Slovnet evaluation section</a> for more.

<!--- ner1 --->
<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PER/LOC/ORG f1</th>
      <th>init, s</th>
      <th>disk, mb</th>
      <th>ram, mb</th>
      <th>speed, articles/s</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>slovnet</th>
      <td>0.97/0.91/0.85</td>
      <td>1.0</td>
      <td>27</td>
      <td>205</td>
      <td>25.3</td>
    </tr>
    <tr>
      <th>deeppavlov_bert</th>
      <td>0.98/0.92/0.86</td>
      <td>34.5</td>
      <td>2048</td>
      <td>6144</td>
      <td>13.1 (gpu)</td>
    </tr>
    <tr>
      <th>deeppavlov</th>
      <td>0.92/0.86/0.76</td>
      <td>5.9</td>
      <td>1024</td>
      <td>3072</td>
      <td>24.3 (gpu)</td>
    </tr>
    <tr>
      <th>pullenti</th>
      <td>0.92/0.82/0.64</td>
      <td>2.9</td>
      <td>16</td>
      <td>253</td>
      <td>6.0</td>
    </tr>
  </tbody>
</table>
<!--- ner1 --->

## Support

- Chat — https://telegram.me/natural_language_processing
- Issues — https://github.com/natasha/natasha/issues
- Commercial support — http://lab.alexkuk.ru/natasha

## Development

Tests:

```bash
make test
```

Package:

```bash
make version
git push
git push --tags

make clean package publish
```
