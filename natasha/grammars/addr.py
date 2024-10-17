
from yargy import (
    rule, empty, forward,
    or_, and_, not_
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, lte, gte, gram, type, tag,
    length_eq,
    in_, in_caseless, dictionary,
    normalized, caseless,
    is_title
)
from yargy.pipelines import morph_pipeline
from yargy.tokenizer import QUOTES

Index = fact(
    'Index',
    ['value']
)
Unparsedint = fact(
    'Unparsedint',
    ['value']
)
Unparsedvarchar = fact(
    'Unparsedvarchar',
    ['value']
)

Country = fact(
    'Country',
    ['name']
)
Region = fact(
    'Region',
    ['name', 'type']
)
Raion = fact(
    'Raion',
    ['name', 'type']
)
Settlement = fact(
    'Settlement',
    ['name', 'type']
)
Sodrugestvo = fact(
    'Sodrugestvo',
    ['name', 'type']
)
Street = fact(
    'Street',
    ['name', 'type']
)
Building = fact(
    'Building',
    ['number', 'type']
)
Room = fact(
    'Room',
    ['number', 'type']
)
AddrPart = fact(
    'AddrPart',
    ['value']
)


def value(key):
    @property
    def field(self):
        return getattr(self, key)
    return field


class Index(Index):
    type = 'индекс'

class Unparsedint(Unparsedint):
    type = 'int'

class Unparsedvarchar(Unparsedvarchar):
    type = 'varchar'

class Country(Country):
    type = 'страна'
    value = value('name')


class Region(Region):
    value = value('name')


class Raion(Raion):
    value = value('name')


class Settlement(Settlement):
    value = value('name')

class Sodrugestvo(Settlement):
    value = value('name')

class Street(Settlement):
    value = value('name')


class Building(Building):
    value = value('number')


class Room(Room):
    value = value('number')


class AddrPart(AddrPart):
    @property
    def obj(self):
        from natasha import obj

        part = self.value
        return obj.AddrPart(part.value, part.type)


DASH = eq('-')
DOT = eq('.')

ADJF = gram('ADJF')
NOUN = gram('NOUN')
INT = type('INT')
TITLE = is_title()

ANUM = rule(
    INT,
    DASH.optional(),
    in_caseless({
        'я', 'й', 'е',
        'ое', 'ая', 'ий', 'ой'
    })
)


#########
#
#  STRANA
#
##########


# TODO
COUNTRY_VALUE = dictionary({
    'россия',
    'украина',
})

ABBR_COUNTRY_VALUE = in_caseless({
    'рф'
})
COUNTRY = or_(
    COUNTRY_VALUE,
    ABBR_COUNTRY_VALUE,
).interpretation(
    Country.name
).interpretation(
    Country
)


#############
#
#  FED OKRUGA
#
############


FED_OKRUG_NAME = or_(
    rule(
        dictionary({
            'дальневосточный',
            'приволжский',
            'сибирский',
            'уральский',
            'центральный',
            'южный',
        })
    ),
    rule(
        caseless('северо'),
        DASH.optional(),
        dictionary({
            'западный',
            'кавказский'
        })
    )
).interpretation(
    Region.name
)

FED_OKRUG_WORDS = or_(
    rule(
        normalized('федеральный'),
        normalized('округ')
    ),
    rule(caseless('фо'))
).interpretation(
    Region.type.const('Федеральная территория')
)

FED_OKRUG = rule(
    FED_OKRUG_WORDS,
    FED_OKRUG_NAME
).interpretation(
    Region
)


#########
#
#   RESPUBLIKA
#
############


RESPUBLIKA_WORDS = or_(
    rule(caseless('респ'), DOT.optional()),
    rule(normalized('республика'))
).interpretation(
    Region.type.const('Республика')
)

RESPUBLIKA_ADJF = or_(
    rule(
        dictionary({
            'удмуртский',
            'чеченский',
            'чувашский',
        })
    ),
    rule(
        caseless('карачаево'),
        DASH.optional(),
        normalized('черкесский')
    ),
    rule(
        caseless('кабардино'),
        DASH.optional(),
        normalized('балкарский')
    )
).interpretation(
    Region.name
)

RESPUBLIKA_NAME = or_(
    rule(
        dictionary({
            'адыгея',
            'алтай',
            'башкортостан',
            'бурятия',
            'дагестан',
            'ингушетия',
            'калмыкия',
            'карелия',
            'коми',
            'крым',
            'мордовия',
            'татарстан',
            'тыва',
            'удмуртия',
            'хакасия',
            'саха',
            'якутия',
        })
    ),
    rule(caseless('марий'), caseless('эл')),
    rule(
        normalized('северный'), normalized('осетия'),
        rule('-', normalized('алания')).optional()
    )
).interpretation(
    Region.name
)

RESPUBLIKA_ABBR = in_caseless({
    'кбр',
    'кчр',
    'рт',  # Татарстан
}).interpretation(
    Region.name  # TODO type
)

RESPUBLIKA = or_(
    rule(RESPUBLIKA_ADJF, RESPUBLIKA_WORDS),
    rule(RESPUBLIKA_WORDS, RESPUBLIKA_NAME),
    rule(RESPUBLIKA_ABBR)
).interpretation(
    Region
)


##########
#
#   KRAI
#
########


KRAI_WORDS = normalized('край').interpretation(
    Region.type.const('Край')
)

KRAI_NAME = dictionary({
    'алтайский',
    'забайкальский',
    'камчатский',
    'краснодарский',
    'красноярский',
    'пермский',
    'приморский',
    'ставропольский',
    'хабаровский',
}).interpretation(
    Region.name
)

KRAI = rule(
    KRAI_NAME, KRAI_WORDS
).interpretation(
    Region
)


############
#
#    OBLAST
#
############


OBLAST_WORDS = or_(
    rule(normalized('область')),
    rule(
        caseless('обл'),
        DOT.optional()
    )
).interpretation(
    Region.type.const('Область')
)

OBLAST_NAME = dictionary({
    'амурский',
    'архангельский',
    'астраханский',
    'белгородский',
    'брянский',
    'владимирский',
    'волгоградский',
    'вологодский',
    'воронежский',
    'горьковский',
    'ивановский',
    'ивановский',
    'иркутский',
    'калининградский',
    'калужский',
    'камчатский',
    'кемеровский',
    'кировский',
    'костромской',
    'курганский',
    'курский',
    'ленинградский',
    'липецкий',
    'магаданский',
    'московский',
    'мурманский',
    'нижегородский',
    'новгородский',
    'новосибирский',
    'омский',
    'оренбургский',
    'орловский',
    'пензенский',
    'пермский',
    'псковский',
    'ростовский',
    'рязанский',
    'самарский',
    'саратовский',
    'сахалинский',
    'свердловский',
    'смоленский',
    'тамбовский',
    'тверской',
    'томский',
    'тульский',
    'тюменский',
    'ульяновский',
    'челябинский',
    'читинский',
    'ярославский',
}).interpretation(
    Region.name
)

OBLAST = or_(
    rule(
        OBLAST_NAME,
        OBLAST_WORDS
    ),
    rule(
        OBLAST_WORDS,
        OBLAST_NAME
    ),
).interpretation(
    Region
)


##########
#
#    AUTO OKRUG
#
#############


AUTO_OKRUG_NAME = or_(
    rule(
        dictionary({
            'чукотский',
            'эвенкийский',
            'корякский',
            'ненецкий',
            'таймырский',
            'агинский',
            'бурятский',
        })
    ),
    rule(caseless('коми'), '-', normalized('пермяцкий')),
    rule(caseless('долгано'), '-', normalized('ненецкий')),
    rule(caseless('ямало'), '-', normalized('ненецкий')),
).interpretation(
    Region.name
)

AUTO_OKRUG_WORDS = or_(
    rule(
        normalized('автономный'),
        normalized('округ')
    ),
    rule(caseless('ао'))
).interpretation(
    Region.type.const('Автономный округ')
)

HANTI = rule(
    caseless('ханты'), '-', normalized('мансийский')
).interpretation(
    Region.name
)

BURAT = rule(
    caseless('усть'), '-', normalized('ордынский'),
    normalized('бурятский')
).interpretation(
    Region.name
)

AUTO_OKRUG = or_(
    rule(AUTO_OKRUG_NAME, AUTO_OKRUG_WORDS),
    or_(
        rule(
            HANTI,
            AUTO_OKRUG_WORDS,
            '-', normalized('югра')
        ),
        rule(
            caseless('хмао'),
        ).interpretation(Region.name),
        rule(
            caseless('хмао'),
            '-', caseless('югра')
        ).interpretation(Region.name),
    ),
    rule(
        BURAT,
        AUTO_OKRUG_WORDS
    )
).interpretation(
    Region
)



##########
#
#  RAION
#
###########


RAION_WORDS = or_(
    rule(
        #русские и английские буквы
        in_caseless({'р', 'p'}), '-', in_caseless({'он', 'н', 'oн'}), 
        DOT.optional()
    ),
    rule(
        caseless('мн'),
        DOT.optional()
    ),
    rule(
        normalized('район'),
        DOT.optional()
    ),
).interpretation(
    Raion.type.const('Район')
)

RAION_SIMPLE_NAME = and_(
    ADJF,
    TITLE
)

RAION_MODIFIERS = rule(
    in_caseless({
        'усть',
        'северо',
        'александрово',
        'гаврилово',
    }),
    DASH.optional(),
    TITLE
)

RAION_COMPLEX_NAME = rule(
    RAION_MODIFIERS,
    RAION_SIMPLE_NAME
)

RAION_NAME = or_(
    rule(RAION_SIMPLE_NAME),
    RAION_COMPLEX_NAME
).interpretation(
    Raion.name
)

RAION = or_(
    rule(
        RAION_WORDS,
        RAION_NAME
    ),
    rule(
        RAION_NAME,
        RAION_WORDS
    ),
).interpretation(
    Raion
)

##############
#
#    GOR OKRUG
#
##############

GOR_OKRUG_WORDS = or_(
    rule(caseless('городской'), caseless('округ')),
    rule(
        in_caseless({'ггородской', 'городской'}), 
        in_caseless({'округ', 'лкруг'})
    ),
    rule(caseless('г'), '.', caseless('о'), '.'), 
    rule(caseless('г'), '.', caseless('о'), ','), 
).interpretation(
    Raion.type.const('Городской округ')
)
GOROD_SIMPLE = dictionary({
    'москва',
    'новосибирск',
    'екатеринбург',
    'казань',
    'самара',
    'омск',
    'челябинск',
    'уфа',
    'волгоград',
    'пермь',
    'красноярск',
    'воронеж',
    'саратов',
    'краснодар',
    'тольятти',
    'барнаул',
    'ижевск',
    'ульяновск',
    'владивосток',
    'ярославль',
    'иркутск',
    'тюмень',
    'махачкала',
    'хабаровск',
    'оренбург',
    'новокузнецк',
    'кемерово',
    'рязань',
    'томск',
    'астрахань',
    'пенза',
    'липецк',
    'тула',
    'киров',
    'чебоксары',
    'калининград',
    'брянск',
    'курск',
    'иваново',
    'магнитогорск',
    'тверь',
    'ставрополь',
    'симферополь',
    'белгород',
    'архангельск',
    'владимир',
    'севастополь',
    'сочи',
    'курган',
    'смоленск',
    'калуга',
    'чита',
    'орёл',
    'волжский',
    'череповец',
    'владикавказ',
    'мурманск',
    'сургут',
    'вологда',
    'саранск',
    'тамбов',
    'стерлитамак',
    'грозный',
    'якутск',
    'кострома',
    'петрозаводск',
    'таганрог',
    'нижневартовск',
    'братск',
    'новороссийск',
    'дзержинск',
    'шахта',
    'нальчик',
    'орск',
    'сыктывкар',
    'нижнекамск',
    'ангарск',
    'балашиха',
    'благовещенск',
    'прокопьевск',
    'химки',
    'псков',
    'бийск',
    'энгельс',
    'рыбинск',
    'балаково',
    'северодвинск',
    'армавир',
    'подольск',
    'королёв',
    'сызрань',
    'норильск',
    'златоуст',
    'мытищи',
    'люберцы',
    'волгодонск',
    'новочеркасск',
    'абакан',
    'находка',
    'уссурийск',
    'березники',
    'салават',
    'электросталь',
    'миасс',
    'первоуральск',
    'рубцовск',
    'альметьевск',
    'ковровый',
    'коломна',
    'керчь',
    'майкоп',
    'пятигорск',
    'одинцово',
    'копейск',
    'хасавюрт',
    'новомосковск',
    'кисловодск',
    'серпухов',
    'новочебоксарск',
    'нефтеюганск',
    'димитровград',
    'нефтекамск',
    'черкесск',
    'дербент',
    'камышин',
    'невинномысск',
    'красногорск',
    'мур',
    'батайск',
    'новошахтинск',
    'ноябрьск',
    'кызыл',
    'октябрьский',
    'ачинск',
    'северск',
    'новокуйбышевск',
    'елец',
    'евпатория',
    'арзамас',
    'обнинск',
    'каспийск',
    'элиста',
    'пушкино',
    'жуковский',
    'междуреченск',
    'сарапул',
    'ессентуки',
    'воткинск',
    'ногинск',
    'тобольск',
    'ухта',
    'серов',
    'бердск',
    'мичуринск',
    'киселёвск',
    'новотроицк',
    'зеленодольск',
    'соликамск',
    'раменский',
    'домодедово',
    'магадан',
    'глазов',
    'железногорск',
    'канск',
    'назрань',
    'гатчина',
    'саров',
    'новоуральск',
    'воскресенск',
    'долгопрудный',
    'бугульма',
    'кузнецк',
    'губкин',
    'кинешма',
    'ейск',
    'реутов',
    'железногорск',
    'чайковский',
    'азов',
    'бузулук',
    'озёрск',
    'балашов',
    'юрга',
    'кропоткин',
    'клин',
    'заостровское',
    'талажское',
})
GOR_OKRUG_SIMPLE = or_(
    rule(caseless('город'), GOROD_SIMPLE),
    rule(caseless('г'), '.', GOROD_SIMPLE),
)

GOR_OKRUG_NAME = GOR_OKRUG_SIMPLE.interpretation(
    Raion.name
)

GOR_OKRUG = or_(
    rule(
        GOR_OKRUG_WORDS,
        GOR_OKRUG_NAME
    ),
).interpretation(
    Raion
)


##############
#
#    MUN_OBRAZ
#
##############

MUN_OBRAZ_WORDS = or_(
    rule(caseless('муниципальное'), caseless('образование')),
    rule(caseless('мо'))
).interpretation(
    Raion.type.const('Муниципальное образование')
)
MUN_OBRAZ_SIMPLE = or_(
    rule(caseless('город'), GOROD_SIMPLE),
    rule(GOROD_SIMPLE)
)

MUN_OBRAZ_NAME = MUN_OBRAZ_SIMPLE.interpretation(
    Raion.name
)

MUN_OBRAZ = or_(
    rule(
        MUN_OBRAZ_WORDS,
        MUN_OBRAZ_NAME
    ),
).interpretation(
    Raion
)
###########
#
#   GOROD
#
###########


# Top 200 Russia cities, cover 75% of population

COMPLEX = morph_pipeline([
    'санкт-петербург',
    'нижний новгород',
    'н.новгород',
    'ростов-на-дону',
    'набережные челны',
    'улан-удэ',
    'нижний тагил',
    'комсомольск-на-амуре',
    'йошкар-ола',
    'старый оскол',
    'великий новгород',
    'южно-сахалинск',
    'петропавловск-камчатский',
    'каменск-уральский',
    'орехово-зуево',
    'сергиев посад',
    'новый уренгой',
    'ленинск-кузнецкий',
    'великие луки',
    'каменск-шахтинский',
    'усть-илимск',
    'усолье-сибирский',
    'кирово-чепецк',
])

SIMPLE = dictionary({
    'москва',
    'новосибирск',
    'екатеринбург',
    'казань',
    'самара',
    'омск',
    'челябинск',
    'уфа',
    'волгоград',
    'пермь',
    'красноярск',
    'воронеж',
    'саратов',
    'краснодар',
    'тольятти',
    'барнаул',
    'ижевск',
    'ульяновск',
    'владивосток',
    'ярославль',
    'иркутск',
    'тюмень',
    'махачкала',
    'хабаровск',
    'оренбург',
    'новокузнецк',
    'кемерово',
    'рязань',
    'томск',
    'астрахань',
    'пенза',
    'липецк',
    'тула',
    'киров',
    'чебоксары',
    'калининград',
    'брянск',
    'курск',
    'иваново',
    'магнитогорск',
    'тверь',
    'ставрополь',
    'симферополь',
    'белгород',
    'архангельск',
    'владимир',
    'севастополь',
    'сочи',
    'курган',
    'смоленск',
    'калуга',
    'чита',
    'орёл',
    'волжский',
    'череповец',
    'владикавказ',
    'мурманск',
    'сургут',
    'вологда',
    'саранск',
    'тамбов',
    'стерлитамак',
    'грозный',
    'якутск',
    'кострома',
    'петрозаводск',
    'таганрог',
    'нижневартовск',
    'братск',
    'новороссийск',
    'дзержинск',
    'шахта',
    'нальчик',
    'орск',
    'сыктывкар',
    'нижнекамск',
    'ангарск',
    'балашиха',
    'благовещенск',
    'прокопьевск',
    'химки',
    'псков',
    'бийск',
    'энгельс',
    'рыбинск',
    'балаково',
    'северодвинск',
    'армавир',
    'подольск',
    'королёв',
    'сызрань',
    'норильск',
    'златоуст',
    'мытищи',
    'люберцы',
    'волгодонск',
    'новочеркасск',
    'абакан',
    'находка',
    'уссурийск',
    'березники',
    'салават',
    'электросталь',
    'миасс',
    'первоуральск',
    'рубцовск',
    'альметьевск',
    'ковровый',
    'коломна',
    'керчь',
    'майкоп',
    'пятигорск',
    'одинцово',
    'копейск',
    'хасавюрт',
    'новомосковск',
    'кисловодск',
    'серпухов',
    'новочебоксарск',
    'нефтеюганск',
    'димитровград',
    'нефтекамск',
    'черкесск',
    'дербент',
    'камышин',
    'невинномысск',
    'красногорск',
    'мур',
    'батайск',
    'новошахтинск',
    'ноябрьск',
    'кызыл',
    'октябрьский',
    'ачинск',
    'северск',
    'новокуйбышевск',
    'елец',
    'евпатория',
    'арзамас',
    'обнинск',
    'каспийск',
    'элиста',
    'пушкино',
    'жуковский',
    'междуреченск',
    'сарапул',
    'ессентуки',
    'воткинск',
    'ногинск',
    'тобольск',
    'ухта',
    'серов',
    'бердск',
    'мичуринск',
    'киселёвск',
    'новотроицк',
    'зеленодольск',
    'соликамск',
    'раменский',
    'домодедово',
    'магадан',
    'глазов',
    'железногорск',
    'канск',
    'назрань',
    'гатчина',
    'саров',
    'новоуральск',
    'воскресенск',
    'долгопрудный',
    'бугульма',
    'кузнецк',
    'губкин',
    'кинешма',
    'ейск',
    'реутов',
    'железногорск',
    'чайковский',
    'азов',
    'бузулук',
    'озёрск',
    'балашов',
    'юрга',
    'кропоткин',
    'клин',
})

GOROD_ABBR = in_caseless({
    'спб',
    'мск',
    'нск'   # Новосибирск
})

GOROD_NAME = or_(
    rule(SIMPLE),
    COMPLEX,
    rule(GOROD_ABBR)
).interpretation(
    Settlement.name
)

SIMPLE = and_(
    TITLE,
    or_(
        NOUN,
        ADJF  # Железнодорожный, Юбилейный
    )
)

COMPLEX = or_(
    rule(
        SIMPLE,
        DASH.optional(),
        SIMPLE
    ),
    rule(
        TITLE,
        DASH.optional(),
        caseless('на'),
        DASH.optional(),
        TITLE
    )
)

NAME = or_(
    rule(SIMPLE),
    COMPLEX
)

MAYBE_GOROD_NAME = or_(
    NAME,
    rule(NAME, '-', INT)
).interpretation(
    Settlement.name
)

GOROD_WORDS = or_(
    rule(normalized('город')),
    rule(
        in_caseless({'г', 'гор'}),
        DOT.optional()
    )
).interpretation(
    Settlement.type.const('Город')
)

GOROD = or_(
    rule(GOROD_WORDS, MAYBE_GOROD_NAME),
    rule(
        GOROD_WORDS.optional(),
        GOROD_NAME
    ),
    rule(
        GOROD_NAME,
        GOROD_WORDS.optional()
    )
).interpretation(
    Settlement
)


##########
#
#  SETTLEMENT NAME
#
##########


ADJS = gram('ADJS')
SIMPLE = and_(
    or_(
        NOUN,  # Александровка, Заречье, Горки
        ADJS,  # Кузнецово
        ADJF,  # Никольское, Новая, Марьино
    ),
    TITLE
)

COMPLEX = rule(
    SIMPLE,
    DASH.optional(),
    SIMPLE
)

NAME = or_(
    rule(SIMPLE),
    COMPLEX
)

SETTLEMENT_NAME = or_(
    NAME,
    rule(NAME, '-', INT),
    rule(NAME, ANUM)
)

###########
#
#   OKRUG
#
#############


OKRUG_WORDS = or_(
    rule(
        in_caseless({'ок', 'окр'}),
        DOT.optional()
    ),
    rule(normalized('округ'))
).interpretation(
    Settlement.type.const('Округ')
)

OKRUG_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

OKRUG = or_(
    rule(
        OKRUG_WORDS,
        OKRUG_NAME
    ),
    rule(
        OKRUG_NAME,
        OKRUG_WORDS
    ),
).interpretation(
    Settlement
)

###########
#
#   SELO
#
#############


SELO_WORDS = or_(
    rule(
        caseless('с'),
        DOT.optional()
    ),
    rule(normalized('село'))
).interpretation(
    Settlement.type.const('Село')
)

SELO_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

SELO = rule(
    SELO_WORDS,
    SELO_NAME
).interpretation(
    Settlement
)

###########
#
#   STANCIYA
#
#############


STANCIYA_WORDS = or_(
    rule(
        in_caseless({'ст'}),
        DOT
        #нельзя убирать точку, иначе попадает Садовое товарищество
    ),
    rule(normalized('станция'))
).interpretation(
    Settlement.type.const('Станция')
)

STANCIYA_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

STANCIYA = rule(
    STANCIYA_WORDS,
    STANCIYA_NAME
).interpretation(
    Settlement
)

###########
#
#   DEREVNYA
#
#############


DEREVNYA_WORDS = or_(
    rule(
        in_caseless({'д', 'дер', 'дерев', 'деревн'}),
        DOT.optional()
    ),
    rule(normalized('деревня'))
).interpretation(
    Settlement.type.const('Деревня')
)

DEREVNYA_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

DEREVNYA = rule(
    DEREVNYA_WORDS,
    DEREVNYA_NAME
).interpretation(
    Settlement
)


###########
#
#   POSELOK
#
#############


POSELOK_WORDS = or_(
    rule(
        in_caseless({'п', 'пос'}),
        DOT.optional()
    ),
    rule(normalized('посёлок')),
    rule(
        caseless('р'),
        DOT.optional(),
        caseless('п'),
        DOT.optional()
    ),
    rule(
        normalized('рабочий'),
        normalized('посёлок')
    ),
    rule(
        caseless('пгт'),
        DOT.optional()
    ),
    rule(
        caseless('п'), DOT, caseless('г'), DOT, caseless('т'),
        DOT.optional()
    ),
    rule(
        normalized('посёлок'),
        normalized('городского'),
        normalized('типа'),
    ),
).interpretation(
    Settlement.type.const('Поселок')
)

POSELOK_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

POSELOK = rule(
    POSELOK_WORDS,
    POSELOK_NAME
).interpretation(
    Settlement
)


###########
#
#   OSTROV
#
#############


OSTROV_WORDS = or_(
    rule(
        in_caseless({'остр', 'остров', 'ос-ов'}),
        DOT.optional()
    ),
).interpretation(
    Settlement.type.const('Остров')
)

OSTROV_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

OSTROV = or_(
    rule(
        OSTROV_WORDS,
        OSTROV_NAME
    ),
    rule(
        OSTROV_NAME,
        OSTROV_WORDS
    )
).interpretation(
    Settlement
)


###########
#
#   AIRPORT
#
#############


AIRPORT_WORDS = or_(
    rule(
        caseless('аэропорт'),
        DOT.optional()
    ),
).interpretation(
    Settlement.type.const('Аэропорт')
)

AIRPORT_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

AIRPORT = or_(
    rule(
        AIRPORT_WORDS,
        AIRPORT_NAME
    ),
    rule(
        AIRPORT_NAME,
        AIRPORT_WORDS
    )
).interpretation(
    Settlement
)


###########
#
#   TERRITORY
#
#############


TERRITORY_WORDS = or_(
    rule(
        caseless('тер'),
        DOT.optional()
    ),
).interpretation(
    Settlement.type.const('Территория')
)

TERRITORY_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

TERRITORY = or_(
    rule(
        TERRITORY_WORDS,
        TERRITORY_NAME
    ),
    rule(
        TERRITORY_NAME,
        TERRITORY_WORDS
    )
).interpretation(
    Settlement
)
##############
#
#   ADDR PERSON
#
############


ABBR = and_(
    length_eq(1),
    is_title()
)

PART = and_(
    TITLE,
    or_(
        gram('Name'),
        gram('Surn')
    )
)

MAYBE_FIO = or_(
    rule(TITLE, PART),
    rule(PART, TITLE),
    rule(ABBR, '.', TITLE),
    rule(ABBR, '.', ABBR, '.', TITLE),
    rule(TITLE, ABBR, '.', ABBR, '.')
)

POSITION_WORDS_ = or_(
    rule(
        dictionary({
            'мичман',
            'геолог',
            'подводник',
            'краевед',
            'снайпер',
            'штурман',
            'бригадир',
            'учитель',
            'политрук',
            'военком',
            'ветеран',
            'историк',
            'пулемётчик',
            'авиаконструктор',
            'адмирал',
            'академик',
            'актер',
            'актриса',
            'архитектор',
            'атаман',
            'врач',
            'воевода',
            'генерал',
            'губернатор',
            'хирург',
            'декабрист',
            'разведчик',
            'граф',
            'десантник',
            'конструктор',
            'скульптор',
            'писатель',
            'поэт',
            'капитан',
            'князь',
            'комиссар',
            'композитор',
            'космонавт',
            'купец',
            'лейтенант',
            'лётчик',
            'майор',
            'маршал',
            'матрос',
            'подполковник',
            'полковник',
            'профессор',
            'сержант',
            'старшина',
            'танкист',
            'художник',
            'герой',
            'княгиня',
            'строитель',
            'дружинник',
            'диктор',
            'прапорщик',
            'артиллерист',
            'графиня',
            'большевик',
            'патриарх',
            'сварщик',
            'офицер',
            'рыбак',
            'брат',
        })
    ),
    rule(normalized('генерал'), normalized('армия')),
    rule(normalized('герой'), normalized('россия')),
    rule(
        normalized('герой'),
        normalized('российский'), normalized('федерация')),
    rule(
        normalized('герой'),
        normalized('советский'), normalized('союз')
    ),
)

ABBR_POSITION_WORDS = rule(
    in_caseless({
        'адм',
        'ак',
        'акад',
    }),
    DOT.optional()
)

POSITION_WORDS = or_(
    POSITION_WORDS_,
    ABBR_POSITION_WORDS
)

MAYBE_PERSON = or_(
    MAYBE_FIO,
    rule(POSITION_WORDS, MAYBE_FIO),
    rule(POSITION_WORDS, TITLE)
)


###########
#
#   IMENI
#
##########


IMENI_WORDS = or_(
    rule(
        caseless('им'),
        DOT.optional()
    ),
    rule(caseless('имени'))
)

IMENI = or_(
    rule(
        IMENI_WORDS.optional(),
        MAYBE_PERSON
    ),
    rule(
        IMENI_WORDS,
        TITLE
    )
)

##########
#
#   LET
#
##########


LET_WORDS = or_(
    rule(caseless('лет')),
    rule(
        DASH.optional(),
        caseless('летия')
    )
)

LET_NAME = in_caseless({
    'влксм',
    'ссср',
    'алтая',
    'башкирии',
    'бурятии',
    'дагестана',
    'калмыкии',
    'колхоза',
    'комсомола',
    'космонавтики',
    'москвы',
    'октября',
    'пионерии',
    'победы',
    'великой победы',
    'приморья',
    'района',
    'совхоза',
    'совхозу',
    'татарстана',
    'тувы',
    'удмуртии',
    'улуса',
    'хакасии',
    'целины',
    'чувашии',
    'якутии',
})

LET = rule(
    INT,
    LET_WORDS,
    LET_NAME
)


##########
#
#    ADDR DATE
#
#############


MONTH_WORDS = dictionary({
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
})

DAY = and_(
    INT,
    gte(1),
    lte(31)
)

YEAR = and_(
    INT,
    gte(1),
    lte(2100)
)

YEAR_WORDS = normalized('год')

DATE = or_(
    rule(DAY, MONTH_WORDS),
    rule(YEAR, YEAR_WORDS)
)


#########
#
#   MODIFIER
#
############


MODIFIER_WORDS_ = rule(
    dictionary({
        'большой',
        'малый',
        'средний',

        'верхний',
        'центральный',
        'нижний',
        'северный',
        'дальний',

        'первый',
        'второй',

        'старый',
        'новый',

        'красный',
        'лесной',
        'тихий',
    }),
    DASH.optional()
)

ABBR_MODIFIER_WORDS = rule(
    in_caseless({
        'б', 'м', 'н'
    }),
    DOT.optional()
)

SHORT_MODIFIER_WORDS = rule(
    in_caseless({
        'больше',
        'мало',
        'средне',

        'верх',
        'верхне',
        'центрально',
        'нижне',
        'северо',
        'дальне',
        'восточно',
        'западно',

        'перво',
        'второ',

        'старо',
        'ново',

        'красно',
        'тихо',
        'горно',
    }),
    DASH.optional()
)

MODIFIER_WORDS = or_(
    MODIFIER_WORDS_,
    ABBR_MODIFIER_WORDS,
    SHORT_MODIFIER_WORDS,
)


##########
#
#   ADDR NAME
#
##########


ROD = gram('gent')

SIMPLE = and_(
    or_(
        ADJF,  # Школьная
        and_(NOUN, ROD),  # Ленина, Победы
    ),
    TITLE
)
COMPLEX = or_(
    rule(
        and_(ADJF, TITLE),
        NOUN
    ),
    rule(
        TITLE,
        DASH.optional(),
        TITLE
    ),
)

# TODO
# Исключения - список дурацких улиц, которые ни в какую не хотят парситься.
# Пример - "Тимме" - по отладке, должна матчиться SIMPLE, но в данном случае
# возникают морфологические проблемы
# туда же - зеленец - оно не склоняемое
# Импульс - название СНТ - если спислк СНТ будет расти - придется делать справочник снт
# Вымпел - гск
# снт масленица, сот малинка
# киз Лето, Исакогорка
EXCEPTION = dictionary({
    'арбат',
    'варварка',
    'тимме',
    'зеленец',
    'импульс',
    'вымпел',
    'лето',
    'масленица',
    'исакогорка',
    '1 рабочий',
    'рабочий',
    'сигнал',
    'московский',
    'самойло',
    'малинка',
    'ельник',
    'локомотив',
    'лотос',
    'катунинец',
    'виченка',
    'автомобилист',
    'кедр',
    'клдк',
    'суфтина',
    'кедрова',
    'жосу',
    'черемушки',
    'брусовица',
    'ручеек',
    'набережная',
    'ваганиха',
    'дружба',
    'нива',
    'целлюлозник',
    'истра',
    'монолит',
    'труд',
    'риф',
    'ельник',
    'исток',
    'октябрь',
    'вперед',
    'мечта',
    'экология',
    'сосновка',
    'заря',
    'бочага',
    'сирена',
    'черная курья',
    'север',
    'арс',
    'собор',
    'спутник',
    'парус',
    'эфир',
    'соломбалец',
    'силикат',
    'волна',
    
})
# Продолжение списка исключений.
# Пример - "Северодвинская ветка 2", она же "2-ой км Сверодвинской ветки"
# Если после "Северодвинская ветка" идет 2 - значит это название улицы
# Иначе - номер дома.
NUMBER_AFTER_STREET = or_(
    rule(normalized('северодвинская'), normalized('ветка'), eq('2')), 
    rule(eq('2'), normalized('северодвинской'), normalized('ветки')),  
    rule(eq('второй'), normalized('северодвинской'), normalized('ветки')),  
    rule(eq('4'), caseless('-й'), normalized('кузнечихинский'), normalized('промузел')),  
    rule(caseless('четвертый').optional(), normalized('кузнечихинский'), normalized('промузел')), 
    rule(eq('1'), caseless('-й'), normalized('кузнечихинский'), normalized('промузел')),  
    rule(caseless('первый'), normalized('кузнечихинский'), normalized('промузел')),  
)

MAYBE_NAME = or_(
    rule(SIMPLE),
    COMPLEX,
    rule(EXCEPTION)
)

NAME = or_(
    MAYBE_NAME,
    LET,
    DATE,
    IMENI
)

NAME = rule(
    MODIFIER_WORDS.optional(),
    NAME
)

ADDR_CRF = tag('I').repeatable()

NAME = or_(
    NAME,
    ANUM,
    rule(NAME, ANUM),
    rule(ANUM, NAME),
    rule(INT, DASH.optional(), NAME),
    rule(NAME, DASH, INT),
    ADDR_CRF
)

ADDR_NAME = NAME

########
#
#    GSK
#
#########


GSK_WORDS = or_(
    rule(
        caseless('гск'),
        DOT.optional()
    ),
    rule(
        caseless('пгк'),
        DOT.optional()
    ),
    rule(
        caseless('гк'),
        DOT.optional()
    ),
).interpretation(
    Sodrugestvo.type.const('Гаражно-строительный кооп.')
)
GSK_NAME = ADDR_NAME.interpretation(
    Sodrugestvo.name
)

GSK = or_(
    rule(GSK_WORDS, GSK_NAME),
    rule(GSK_NAME, GSK_WORDS)
).interpretation(
    Sodrugestvo
)


########
#
#    SNT
#
#########


SNT_WORDS = or_(
    rule(
        in_caseless({'снт', 'сот', 'ст', 'сонт', 'тсж'}),
        DOT.optional()
    ),
    rule(
        caseless('садоводческое'),
        caseless('товарищество'),
    ),
    rule(
        caseless('садоводческое'),
        caseless('некоммерческое'),
        caseless('товарищество'),
    ),
).interpretation(
    Sodrugestvo.type.const('Садовое товарищество')
)
SNT_NAME = ADDR_NAME.interpretation(
    Sodrugestvo.name
)

SNT = or_(
    rule(SNT_WORDS, SNT_NAME),
    rule(SNT_NAME, rule(caseless('тер'), DOT.optional()),SNT_WORDS),
    rule(SNT_NAME, SNT_WORDS)
).interpretation(
    Sodrugestvo
)

########
#
#    KIZ
#
#########


KIZ_WORDS = or_(
    rule(caseless('киз')),
    rule(
        caseless('тер.'),
        DOT.optional(),
        caseless('киз'),
    ),
    rule(
        caseless('тер'),
        caseless('киз'),
    ),
).interpretation(
    Sodrugestvo.type.const('Киз')
)
KIZ_NAME = ADDR_NAME.interpretation(
    Sodrugestvo.name
)

KIZ = or_(
    rule(KIZ_WORDS, KIZ_NAME),
    rule(KIZ_NAME, KIZ_WORDS)
).interpretation(
    Sodrugestvo
)


########
#
#    TIZ
#
#########


TIZ_WORDS = or_(
    rule(caseless('тиз')),
    rule(
        caseless('тер.'),
        DOT.optional(),
        caseless('тиз'),
    ),
    rule(
        caseless('тер'),
        caseless('тиз'),
    ),
).interpretation(
    Sodrugestvo.type.const('Тиз')
)
TIZ_NAME = ADDR_NAME.interpretation(
    Sodrugestvo.name
)

TIZ = or_(
    rule(TIZ_WORDS, TIZ_NAME),
    rule(TIZ_NAME, TIZ_WORDS)
).interpretation(
    Sodrugestvo
)
########
#
#    STREET
#
#########


STREET_WORDS = or_(
        rule(normalized('улица')),
        rule(
            caseless('ул'),
            DOT.optional()
        )
).interpretation(   
    Street.type.const('Улица')
)
STREET_NAME = or_(
    rule(INT, ADDR_NAME).interpretation(Street.name),
    ADDR_NAME.interpretation(Street.name),
    INT.interpretation(Street.name),
)

STREET = or_(
    rule(STREET_WORDS, STREET_NAME),
    rule(STREET_NAME, STREET_WORDS)
).interpretation(
    Street
)


########
#
#    KVARTAL
#
#########


KVARTAL_WORDS = or_(
        rule(normalized('квартал')),
        rule(
            caseless('кв-л'),
            DOT.optional()
        ),
        rule(
            caseless('кв'),
            '-',
            caseless('л'),
            DOT.optional()
        ),
        rule(
            caseless('кв'),
            caseless('-'),
            caseless('л'),
            DOT.optional()
        )
).interpretation(
    Street.type.const('Квартал')
)
KVARTAL_NAME = rule(INT.optional(), ADDR_NAME).interpretation(
    Street.name
)

KVARTAL = or_(
    rule(KVARTAL_WORDS, KVARTAL_NAME),
    rule(KVARTAL_NAME, KVARTAL_WORDS)
).interpretation(
    Street
)
########
#
#    KILOMETR
#
#########


KILOMETR_WORDS = or_(
    rule(normalized('километр')),
    rule(
        caseless('км'),
        DOT.optional()
    ),
).interpretation(
    Street.type.const('Километр')
)

KILOMETR_NAME_with_INT = NUMBER_AFTER_STREET.interpretation(
    Street.name
)
KILOMETR_NAME = ADDR_NAME.interpretation(
    Street.name
)

KILOMETR = or_(
    rule(KILOMETR_WORDS, KILOMETR_NAME_with_INT),
    rule(KILOMETR_WORDS, KILOMETR_NAME),
    rule(KILOMETR_NAME, KILOMETR_WORDS),
).interpretation(
    Street
)

########
#
#    LINIA
#
#########


LINIA_WORDS = or_(
    rule(
        normalized('линия'),
        DOT.optional()
    ),
    rule(
        in_caseless({'л','лин', 'линия'}),
        DOT.optional()
    ),
).interpretation(
    Street.type.const('Линия')
)

LINIA_NAME = or_(
    ADDR_NAME.interpretation(Street.name),
    INT.interpretation(Street.name),
)

LINIA = or_(
    rule(LINIA_WORDS, LINIA_NAME),
    rule(LINIA_NAME, LINIA_WORDS),
).interpretation(
    Street
)

##########
#
#    PROSPEKT
#
##########


PROSPEKT_WORDS = or_(
    rule(
        in_caseless({'пр','просп','пркт','пр-кт','пр-т'}),
        DOT.optional()
    ),
    rule(
        caseless('пр'),
        '-',
        in_caseless({'кт','т'}),
        DOT.optional()
    ),
    rule(
        caseless('пр'),
        DOT.optional(),
        in_caseless({'кт','т'}),
        DOT.optional()
    ),
    rule(
        caseless('пр'),
        DOT.optional()
    ),
    rule(normalized('проспект'))
).interpretation(
    Street.type.const('Проспект')
)

PROSPEKT_NAME = ADDR_NAME.interpretation(
    Street.name
)

PROSPEKT = or_(
    rule(PROSPEKT_WORDS, PROSPEKT_NAME),
    rule(PROSPEKT_NAME, PROSPEKT_WORDS)
).interpretation(
    Street
)


############
#
#    PROEZD
#
#############


PROEZD_WORDS = or_(
    rule(
        in_caseless({'пр-езд','пр-зд', 'пр-д', 'прз'}), 
        DOT.optional()
    ),
    rule(
        normalized('проезд'),
        DOT.optional()
    ),
).interpretation(
    Street.type.const('Проезд')
)

PROEZD_NAME = or_(
    ADDR_NAME.interpretation(Street.name),
    INT.interpretation(Street.name),
)

PROEZD_NAME_with_INT = NUMBER_AFTER_STREET.interpretation(
    Street.name
)

PROEZD = or_(
    rule(PROEZD_WORDS, PROEZD_NAME_with_INT),
    rule(PROEZD_NAME, PROEZD_WORDS),
    rule(PROEZD_WORDS, PROEZD_NAME)
).interpretation(
    Street
)


###########
#
#   PEREULOK
#
##############


PEREULOK_WORDS = or_(
    rule(
        caseless('п'),
        DOT.optional()
    ),
    rule(
        caseless('пер'),
        DOT.optional()
    ),
    rule(normalized('переулок'))
).interpretation(
    Street.type.const('Переулок')
)

PEREULOK_NAME = ADDR_NAME.interpretation(
    Street.name
)

PEREULOK = or_(
    rule(PEREULOK_WORDS, PEREULOK_NAME),
    rule(PEREULOK_NAME, PEREULOK_WORDS)
).interpretation(
    Street
)


########
#
#  PLOSHAD
#
##########


PLOSHAD_WORDS = or_(
    rule(
        in_caseless({'пл', 'площ', 'площад', 'площадъ'}),
        DOT.optional()
    ),
    rule(normalized('площадь'))
).interpretation(
    Street.type.const('Площадь')
)

PLOSHAD_NAME = ADDR_NAME.interpretation(
    Street.name
)

PLOSHAD = or_(
    rule(PLOSHAD_WORDS, PLOSHAD_NAME),
    rule(PLOSHAD_NAME, PLOSHAD_WORDS)
).interpretation(
    Street
)


############
#
#   SHOSSE
#
###########


# TODO
# Покровское 17 км.
# Сергеляхское 13 км
# Сергеляхское 14 км.


SHOSSE_WORDS = or_(
    rule(
        in_caseless({'ш', 'шосе', 'шос', 'шосс', 'шосэ', 'шоссэ'}),
        DOT.optional()
    ),
    rule(normalized('шоссе'))
).interpretation(
    Street.type.const('Шоссе')
)

SHOSSE_NAME = ADDR_NAME.interpretation(
    Street.name
)

SHOSSE = or_(
    rule(SHOSSE_WORDS, SHOSSE_NAME),
    rule(SHOSSE_NAME, SHOSSE_WORDS)
).interpretation(
    Street
)


########
#
#  NABEREG
#
##########


NABEREG_WORDS = or_(
    rule(
        in_caseless({'наб', 'н', 'набер', 'набереж', 'набережн'}),
        DOT.optional()
    ),
    rule(normalized('набережная'))
).interpretation(
    Street.type.const('Набережная')
)

NABEREG_NAME = ADDR_NAME.interpretation(
    Street.name
)

NABEREG = or_(
    rule(NABEREG_WORDS, NABEREG_NAME),
    rule(NABEREG_NAME, NABEREG_WORDS)
).interpretation(
    Street
)


########
#
#  BULVAR
#
##########


BULVAR_WORDS = or_(
    rule(
        caseless('б'),
        '-',
        caseless('р')
    ),
    rule(
        caseless('б'),
        DOT.optional()
    ),
    rule(
        caseless('бул'),
        DOT.optional()
    ),
    rule(normalized('бульвар')),
    rule(normalized('бульвара'))
).interpretation(
    Street.type.const('Бульвар')
)

BULVAR_NAME = ADDR_NAME.interpretation(
    Street.name
)

BULVAR = or_(
    rule(BULVAR_WORDS, BULVAR_NAME),
    rule(BULVAR_NAME, BULVAR_WORDS)
).interpretation(
    Street
)


##############
#
#   ADDR VALUE
#
#############

LETTER = in_caseless(set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяф'))

QUOTE = in_(QUOTES)

LETTER = or_(
    rule(LETTER),
    rule(QUOTE, LETTER, QUOTE)
)

VALUE = rule(
    INT,
    LETTER.optional()
)

SEP = in_(r'/\-')

VALUE = or_(
    rule(VALUE),
    rule(VALUE, SEP, VALUE),
    rule(VALUE, SEP, LETTER)
)

ADDR_VALUE = rule(
    eq('№').optional(),
    VALUE
)

############
#
#    GARAG
#
#############

GARAG_WORDS = or_(
    rule(
        normalized('гараж'),
        DOT.optional()
    ),
).interpretation(
    Building.type.const('Гараж')
)


GARAG_VALUE = or_(
    INT.interpretation(Building.number)
).interpretation(
    Building.number
)

GARAG = or_(
    rule(
        GARAG_WORDS,
        GARAG_VALUE
    ),
).interpretation(
    Building
)

############
#
#    DOM
#
#############

UNPARSED_INT = and_(
    INT
).interpretation(
    Unparsedint.value
).interpretation(
    Unparsedint
)

DOM_WORDS = or_(
    rule(
        normalized('дом'),
        DOT.optional()
    ),
    rule(
        caseless('д'),
        DOT.optional()
    ),
).interpretation(
    Building.type.const('Дом')
)


DOM_VALUE = or_(
    INT.interpretation(Building.number)
).interpretation(
    Building.number
)

DOM = or_(
    rule(
        DOM_WORDS,
        DOM_VALUE
    ),
).interpretation(
    Building
)


###########
#
#  KORPUS
#
##########


KORPUS_WORDS = or_(
    rule(
        in_caseless({'корп', 'копр', 'кор', 'корс', 'корус', 'корпс'}),
        DOT.optional()
    ),
    rule(normalized('корпус')),
    rule(normalized('корпусы')),
    rule(normalized('корпусу')),
    rule(
        caseless('к'),
        DOT.optional()
    ),
    rule(
        caseless('/'),
        DOT.optional()
    ),
).interpretation(
    Building.type.const('Корпус')
)

KORPUS_VALUE = or_(
    ADDR_VALUE.interpretation(Building.number),
    LETTER.interpretation(Building.number)
)

KORPUS = or_(
    rule( 
        KORPUS_WORDS,
        KORPUS_VALUE
    )
).interpretation(
    Building
)




###########
#
#  STROENIE
#
##########


STROENIE_WORDS = or_(
    rule(
        in_caseless({'с', 'ст', 'стр_', 'стр', 'строй', 'строен'}),
        DOT.optional()
    ),
    rule(
        normalized('строение'),
        DOT.optional()
    ),
    rule(
        normalized('строения'),
        DOT.optional()
    ),
    rule(
        normalized('строению'),
        DOT.optional()
    )
).interpretation(
    Building.type.const('Строение')
)

STROENIE_VALUE = or_(
    ADDR_VALUE.interpretation(Building.number),
    LETTER.interpretation(Building.number)
)

STROENIE = rule(
    STROENIE_WORDS,
    STROENIE_VALUE
).interpretation(
    Building
)


###########
#
#  LITERA
#
##########


LITERA_WORDS = or_(
    rule(
        in_caseless({'лит', 'литер', 'литеру'}),
        DOT.optional()
    ),
    rule(normalized('литера'))
).interpretation(
    Building.type.const('Литера')
)

LITERA_VALUE = or_(
    ADDR_VALUE.interpretation(Building.number),
    LETTER.interpretation(Building.number)
)

LITERA = rule(
    LITERA_WORDS,
    LITERA_VALUE
).interpretation(
    Building
)

###########
#
#  MASHINOMESTO
#
##########


MASHINOMESTO_WORDS = or_(
    rule(
        in_caseless({'машино-место', 'м-место'}),
        DOT.optional()
    ),
    rule(
        caseless('машино'),
        '-',
        caseless('место'),
    ),
    rule(
        caseless('парковочное'),
        caseless('место'),
    ),
    rule(normalized('машино-место'))
).interpretation(
    Building.type.const('Машино-место')
)

MASHINOMESTO_VALUE = or_(
    ADDR_VALUE.interpretation(Building.number),
    LETTER.interpretation(Building.number)
)

MASHINOMESTO = rule(
    MASHINOMESTO_WORDS,
    MASHINOMESTO_VALUE
).interpretation(
    Building
)
###########
#
#  ETAZH
#
##########


ETAZH_WORDS = or_(
    rule(
        in_caseless({'эт'}),
        DOT.optional()
    ),
    rule(normalized('этаж'))
).interpretation(
    Building.type.const('Этаж')
)

ETAZH_VALUE = or_(
    ADDR_VALUE.interpretation(Building.number),
    LETTER.interpretation(Building.number)
)

ETAZH = or_(
    rule(
    ETAZH_WORDS,
    ETAZH_VALUE
    ),
    rule(
    ETAZH_VALUE,
    ETAZH_WORDS
    ),
).interpretation(
    Building
)


###########
#
#   HRANILISHCHE
#
#############


HRANILISHCHE_WORDS = or_(
    rule(
        caseless('хран'),
        DOT.optional()
    ),
    rule(normalized('хранилище')),
).interpretation(
    Room.type.const('Хранилище')
)

HRANILISHCHE_VALUE = or_(
    ADDR_VALUE.interpretation(Room.number),
    LETTER.interpretation(Room.number)
)

HRANILISHCHE = rule(
    HRANILISHCHE_WORDS,
    HRANILISHCHE_VALUE
).interpretation(
    Room
)

###########
#
#   SEKCIYA
#
#############


SEKCIYA_WORDS = or_(
    rule(
        caseless('секция'),
        DOT.optional()
    ),
    rule(normalized('секция')),
).interpretation(
    Room.type.const('Секция')
)

SEKCIYA_VALUE = or_(
    ADDR_VALUE.interpretation(Room.number),
    LETTER.interpretation(Room.number)
)

SEKCIYA = rule(
    SEKCIYA_WORDS,
    SEKCIYA_VALUE
).interpretation(
    Room
)
###########
#
#   OFIS
#
#############


OFIS_WORDS = or_(
    rule(
        caseless('оф'),
        DOT.optional()
    ),
    rule(normalized('офис')),
    rule(normalized('офисы'))
).interpretation(
    Room.type.const('Офис')
)

OFIS_VALUE = or_(
    ADDR_VALUE.interpretation(Room.number),
    LETTER.interpretation(Room.number)
)

OFIS = rule(
    OFIS_WORDS,
    OFIS_VALUE
).interpretation(
    Room
)


###########
#
#   BLOK
#
#############


BLOK_WORDS = or_(
    rule(
        caseless('бл'),
        DOT.optional()
    ),
    rule(
        normalized('блок'),
        DOT.optional()
    )
).interpretation(
    Room.type.const('Блок')
)

BLOK_VALUE = or_(
    ADDR_VALUE.interpretation(Room.number),
    INT.interpretation(Room.number)
)

BLOK = rule(
    BLOK_WORDS,
    BLOK_VALUE
).interpretation(
    Room
)


###########
#
#   BOKS
#
#############


BOKS_WORDS = or_(
    rule(caseless('гаражный'), caseless('бокс')),
    rule(
        in_caseless({'бокс'}),
        DOT.optional()
    )
).interpretation(
    Room.type.const('Бокс')
)

BOKS_VALUE = or_(
    ADDR_VALUE.interpretation(Room.number),
    LETTER.interpretation(Room.number)
)

BOKS = rule(
    BOKS_WORDS,
    BOKS_VALUE
).interpretation(
    Room
)

###########
#
#   KVARTIRA
#
#############


KVARTIRA_WORDS = or_(
    rule(
        caseless('кв'),
        DOT.optional()
    ),
    rule(normalized('квартира'))
).interpretation(
    Room.type.const('Квартира')
)

KVARTIRA_VALUE = or_(
    ADDR_VALUE.interpretation(Room.number),
    LETTER.interpretation(Room.number)
)

KVARTIRA = rule(
    KVARTIRA_WORDS,
    KVARTIRA_VALUE
).interpretation(
    Room
)


###########
#
#   KOMNATA
#
#############


KOMNATA_WORDS = or_(
    rule(
        in_caseless({'ком', 'комн', 'комна', 'комата','омната','комнат'}),
        DOT.optional()
    ),
    rule(normalized('комната')),
    rule(normalized('комнаты'))
).interpretation(
    Room.type.const('Комната')
)

KOMNATA_VALUE = or_(
    ADDR_VALUE.interpretation(Room.number),
    LETTER.interpretation(Room.number)
)

KOMNATA = rule(
    KOMNATA_WORDS,
    KOMNATA_VALUE
).interpretation(
    Room
)


###########
#
#   POMESHENIE
#
#############


POMESHENIE_WORDS = or_(
    rule(normalized('помещение'), caseless('ОПС')),
    rule(normalized('жилое'), normalized('помещение')),
    rule(normalized('нежилое'), normalized('помещение')),
    rule(
        in_caseless({'пом', 'помещ', 'помеще', 'помещен', 'помещени'}),
        DOT.optional()
    ),
    rule(normalized('помещение')),
    rule(normalized('помещения')),
    rule(normalized('ячейка'))
).interpretation(
    Room.type.const('Помещение')
)

POMESHENIE_VALUE = or_(
    ADDR_VALUE.interpretation(Room.number),
    LETTER.interpretation(Room.number)
)

POMESHENIE = rule(
    POMESHENIE_WORDS,
    POMESHENIE_VALUE
).interpretation(
    Room
)

###########
#
#   UCHASTOK
#
#############


UCHASTOK_WORDS = or_(
    rule(
        in_caseless({'уч', 'уч-к'}), 
        DOT.optional()
    ),
    rule(
        caseless('уч'), 
        '-',
        caseless('к'), 
        DOT.optional()
    ),
    rule(
        normalized('участок')
    )
).interpretation(
    Room.type.const('Участок')
)

UCHASTOK_VALUE = or_(
    ADDR_VALUE.interpretation(Room.number),
    LETTER.interpretation(Room.number)
)

UCHASTOK = or_(
    rule(
        UCHASTOK_WORDS,
        UCHASTOK_VALUE
    ),
    rule(
        UCHASTOK_WORDS,
        UCHASTOK_VALUE
    ),
).interpretation(
    Room
)

###########
#
#   INDEX
#
#############

INDEX = and_(
    INT,
    gte(100000),
    lte(999999)
).interpretation(
    Index.value
).interpretation(
    Index
)

###########
#
#   UNPARSED
#
#############


UNPARSED_INT = and_(
    INT
).interpretation(
    Unparsedint.value
).interpretation(
    Unparsedint
)

UNPARSED_VARCHAR = and_(
    not_(INT),
    not_(
        in_(r',')
    ),
    not_(
        in_(r'\"')
    ),
    not_(
        in_(r'\№')
    )
).interpretation(
    Unparsedvarchar.value
).interpretation(
    Unparsedvarchar
)



#############
#
#   ADDR PART
#
############


ADDR_PART = or_(
    INDEX,
    COUNTRY,
    FED_OKRUG,

    RESPUBLIKA,
    KRAI,
    OBLAST,
    AUTO_OKRUG,

    RAION,
    GOR_OKRUG,
    MUN_OBRAZ,

    GOROD,
    OKRUG,
    STANCIYA,
    DEREVNYA,
    SELO,
    POSELOK,
    OSTROV,
    AIRPORT,
    TERRITORY,

    GSK,
    SNT,
    KIZ,
    TIZ,

    STREET,
    KVARTAL,
    KILOMETR,
    LINIA,
    PROEZD,
    PROSPEKT,
    PEREULOK,
    PLOSHAD,
    SHOSSE,
    NABEREG,
    BULVAR,

    GARAG,
    DOM,
    KORPUS,
    STROENIE,
    LITERA,
    MASHINOMESTO,

    ETAZH,

    SEKCIYA,
    HRANILISHCHE,
    OFIS,
    BLOK,
    BOKS,
    KVARTIRA,
    KOMNATA,
    POMESHENIE,

    UCHASTOK,

    UNPARSED_INT,
    UNPARSED_VARCHAR
).interpretation(
    AddrPart.value
).interpretation(
    AddrPart
)
