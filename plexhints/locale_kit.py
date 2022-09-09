# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
from typing import Optional


class CountryCodes:
    def __init__(self):
        pass

    AF = "Afghanistan"
    AL = "Albania"
    DZ = "Algeria"
    AS = "American Samoa"
    AD = "Andorra"
    AO = "Angola"
    AI = "Anguilla"
    AQ = "Antarctica"
    AG = "Antigua and Barbuda"
    AR = "Argentina"
    AM = "Armenia"
    AW = "Aruba"
    AU = "Australia"
    AT = "Austria"
    AZ = "Azerbaijan"
    BS = "Bahamas"
    BH = "Bahrain"
    BD = "Bangladesh"
    BB = "Barbados"
    BY = "Belarus"
    BE = "Belgium"
    BZ = "Belize"
    BJ = "Benin"
    BM = "Bermuda"
    BT = "Bhutan"
    BO = "Bolivia"
    BA = "Bosnia and Herzegovina"
    BW = "Botswana"
    BV = "Bouvet Island"
    BR = "Brazil"
    BQ = "British Antarctic Territory"
    IO = "British Indian Ocean Territory"
    VG = "British Virgin Islands"
    BN = "Brunei"
    BG = "Bulgaria"
    BF = "Burkina Faso"
    BI = "Burundi"
    KH = "Cambodia"
    CM = "Cameroon"
    CA = "Canada"
    CT = "Canton and Enderbury Islands"
    CV = "Cape Verde"
    KY = "Cayman Islands"
    CF = "Central African Republic"
    TD = "Chad"
    CL = "Chile"
    CN = "China"
    CX = "Christmas Island"
    CC = "Cocos [Keeling] Islands"
    CO = "Colombia"
    KM = "Comoros"
    CG = "Congo - Brazzaville"
    CD = "Congo - Kinshasa"
    CK = "Cook Islands"
    CR = "Costa Rica"
    HR = "Croatia"
    CU = "Cuba"
    CY = "Cyprus"
    CZ = "Czech Republic"
    CI = "Cote d'Ivoire"
    DK = "Denmark"
    DJ = "Djibouti"
    DM = "Dominica"
    DO = "Dominican Republic"
    NQ = "Dronning Maud Land"
    DD = "East Germany"
    EC = "Ecuador"
    EG = "Egypt"
    SV = "El Salvador"
    GQ = "Equatorial Guinea"
    ER = "Eritrea"
    EE = "Estonia"
    ET = "Ethiopia"
    FK = "Falkland Islands"
    FO = "Faroe Islands"
    FJ = "Fiji"
    FI = "Finland"
    FR = "France"
    GF = "French Guiana"
    PF = "French Polynesia"
    TF = "French Southern Territories"
    FQ = "French Southern and Antarctic Territories"
    GA = "Gabon"
    GM = "Gambia"
    GE = "Georgia"
    DE = "Germany"
    GH = "Ghana"
    GI = "Gibraltar"
    GR = "Greece"
    GL = "Greenland"
    GD = "Grenada"
    GP = "Guadeloupe"
    GU = "Guam"
    GT = "Guatemala"
    GG = "Guernsey"
    GN = "Guinea"
    GW = "Guinea-Bissau"
    GY = "Guyana"
    HT = "Haiti"
    HM = "Heard Island and McDonald Islands"
    HN = "Honduras"
    HK = "Hong Kong SAR China"
    HU = "Hungary"
    IS = "Iceland"
    IN = "India"
    ID = "Indonesia"
    IR = "Iran"
    IQ = "Iraq"
    IE = "Ireland"
    IM = "Isle of Man"
    IL = "Israel"
    IT = "Italy"
    JM = "Jamaica"
    JP = "Japan"
    JE = "Jersey"
    JT = "Johnston Island"
    JO = "Jordan"
    KZ = "Kazakhstan"
    KE = "Kenya"
    KI = "Kiribati"
    KW = "Kuwait"
    KG = "Kyrgyzstan"
    LA = "Laos"
    LV = "Latvia"
    LB = "Lebanon"
    LS = "Lesotho"
    LR = "Liberia"
    LY = "Libya"
    LI = "Liechtenstein"
    LT = "Lithuania"
    LU = "Luxembourg"
    MO = "Macau SAR China"
    MK = "Macedonia"
    MG = "Madagascar"
    MW = "Malawi"
    MY = "Malaysia"
    MV = "Maldives"
    ML = "Mali"
    MT = "Malta"
    MH = "Marshall Islands"
    MQ = "Martinique"
    MR = "Mauritania"
    MU = "Mauritius"
    YT = "Mayotte"
    FX = "Metropolitan France"
    MX = "Mexico"
    FM = "Micronesia"
    MI = "Midway Islands"
    MD = "Moldova"
    MC = "Monaco"
    MN = "Mongolia"
    ME = "Montenegro"
    MS = "Montserrat"
    MA = "Morocco"
    MZ = "Mozambique"
    MM = "Myanmar [Burma]"
    NA = "Namibia"
    NR = "Nauru"
    NP = "Nepal"
    NL = "Netherlands"
    AN = "Netherlands Antilles"
    NT = "Neutral Zone"
    NC = "New Caledonia"
    NZ = "New Zealand"
    NI = "Nicaragua"
    NE = "Niger"
    NG = "Nigeria"
    NU = "Niue"
    NF = "Norfolk Island"
    KP = "North Korea"
    VD = "North Vietnam"
    MP = "Northern Mariana Islands"
    NO = "Norway"
    OM = "Oman"
    PC = "Pacific Islands Trust Territory"
    PK = "Pakistan"
    PW = "Palau"
    PS = "Palestinian Territories"
    PA = "Panama"
    PZ = "Panama Canal Zone"
    PG = "Papua New Guinea"
    PY = "Paraguay"
    YD = "People's Democratic Republic of Yemen"
    PE = "Peru"
    PH = "Philippines"
    PN = "Pitcairn Islands"
    PL = "Poland"
    PT = "Portugal"
    PR = "Puerto Rico"
    QA = "Qatar"
    RO = "Romania"
    RU = "Russia"
    RW = "Rwanda"
    RE = "Reunion"
    BL = "Saint Barthelemy"
    SH = "Saint Helena"
    KN = "Saint Kitts and Nevis"
    LC = "Saint Lucia"
    MF = "Saint Martin"
    PM = "Saint Pierre and Miquelon"
    VC = "Saint Vincent and the Grenadines"
    WS = "Samoa"
    SM = "San Marino"
    SA = "Saudi Arabia"
    SN = "Senegal"
    RS = "Serbia"
    CS = "Serbia and Montenegro"
    SC = "Seychelles"
    SL = "Sierra Leone"
    SG = "Singapore"
    SK = "Slovakia"
    SI = "Slovenia"
    SB = "Solomon Islands"
    SO = "Somalia"
    ZA = "South Africa"
    GS = "South Georgia and the South Sandwich Islands"
    KR = "South Korea"
    ES = "Spain"
    LK = "Sri Lanka"
    SD = "Sudan"
    SR = "Suriname"
    SJ = "Svalbard and Jan Mayen"
    SZ = "Swaziland"
    SE = "Sweden"
    CH = "Switzerland"
    SY = "Syria"
    ST = "Sao Tome and Principe"
    TW = "Taiwan"
    TJ = "Tajikistan"
    TZ = "Tanzania"
    TH = "Thailand"
    TL = "Timor-Leste"
    TG = "Togo"
    TK = "Tokelau"
    TO = "Tonga"
    TT = "Trinidad and Tobago"
    TN = "Tunisia"
    TR = "Turkey"
    TM = "Turkmenistan"
    TC = "Turks and Caicos Islands"
    TV = "Tuvalu"
    UM = "U.S. Minor Outlying Islands"
    PU = "U.S. Miscellaneous Pacific Islands"
    VI = "U.S. Virgin Islands"
    UG = "Uganda"
    UA = "Ukraine"
    SU = "Union of Soviet Socialist Republics"
    AE = "United Arab Emirates"
    GB = "United Kingdom"
    US = "United States"
    ZZ = "Unknown or Invalid Region"
    UY = "Uruguay"
    UZ = "Uzbekistan"
    VU = "Vanuatu"
    VA = "Vatican City"
    VE = "Venezuela"
    VN = "Vietnam"
    WK = "Wake Island"
    WF = "Wallis and Futuna"
    EH = "Western Sahara"
    YE = "Yemen"
    ZM = "Zambia"
    ZW = "Zimbabwe"
    AX = "Aland Islnds"


class Language:
    def __init__(self):
        pass

    Unknown = 'xx'
    Afar = 'aa'
    Abkhazian = 'ab'
    Afrikaans = 'af'
    Akan = 'ak'
    Albanian = 'sq'
    Amharic = 'am'
    Arabic = 'ar'
    Aragonese = 'an'
    Armenian = 'hy'
    Assamese = 'as'
    Avaric = 'av'
    Avestan = 'ae'
    Aymara = 'ay'
    Azerbaijani = 'az'
    Bashkir = 'ba'
    Bambara = 'bm'
    Basque = 'eu'
    Belarusian = 'be'
    Bengali = 'bn'
    Bihari = 'bh'
    Bislama = 'bi'
    Bosnian = 'bs'
    Breton = 'br'
    Bulgarian = 'bg'
    Burmese = 'my'
    Catalan = 'ca'
    Chamorro = 'ch'
    Chechen = 'ce'
    Chinese = 'zh'
    ChurchSlavic = 'cu'
    Chuvash = 'cv'
    Cornish = 'kw'
    Corsican = 'co'
    Cree = 'cr'
    Czech = 'cs'
    Danish = 'da'
    Divehi = 'dv'
    Dutch = 'nl'
    Dzongkha = 'dz'
    English = 'en'
    Esperanto = 'eo'
    Estonian = 'et'
    Ewe = 'ee'
    Faroese = 'fo'
    Fijian = 'fj'
    Finnish = 'fi'
    French = 'fr'
    Frisian = 'fy'
    Fulah = 'ff'
    Georgian = 'ka'
    German = 'de'
    Gaelic = 'gd'
    Irish = 'ga'
    Galician = 'gl'
    Manx = 'gv'
    Greek = 'el'
    Guarani = 'gn'
    Gujarati = 'gu'
    Haitian = 'ht'
    Hausa = 'ha'
    Hebrew = 'he'
    Herero = 'hz'
    Hindi = 'hi'
    HiriMotu = 'ho'
    Croatian = 'hr'
    Hungarian = 'hu'
    Igbo = 'ig'
    Icelandic = 'is'
    Ido = 'io'
    SichuanYi = 'ii'
    Inuktitut = 'iu'
    Interlingue = 'ie'
    Interlingua = 'ia'
    Indonesian = 'id'
    Inupiaq = 'ik'
    Italian = 'it'
    Javanese = 'jv'
    Japanese = 'ja'
    Kalaallisut = 'kl'
    Kannada = 'kn'
    Kashmiri = 'ks'
    Kanuri = 'kr'
    Kazakh = 'kk'
    Khmer = 'km'
    Kikuyu = 'ki'
    Kinyarwanda = 'rw'
    Kirghiz = 'ky'
    Komi = 'kv'
    Kongo = 'kg'
    Korean = 'ko'
    Kuanyama = 'kj'
    Kurdish = 'ku'
    Lao = 'lo'
    Latin = 'la'
    Latvian = 'lv'
    Limburgan = 'li'
    Lingala = 'ln'
    Lithuanian = 'lt'
    Luxembourgish = 'lb'
    LubaKatanga = 'lu'
    Ganda = 'lg'
    Macedonian = 'mk'
    Marshallese = 'mh'
    Malayalam = 'ml'
    Maori = 'mi'
    Marathi = 'mr'
    Malay = 'ms'
    Malagasy = 'mg'
    Maltese = 'mt'
    Moldavian = 'mo'
    Mongolian = 'mn'
    Nauru = 'na'
    Navajo = 'nv'
    SouthNdebele = 'nr'
    NorthNdebele = 'nd'
    Ndonga = 'ng'
    Nepali = 'ne'
    NorwegianNynorsk = 'nn'
    NorwegianBokmal = 'nb'
    Norwegian = 'no'
    Chichewa = 'ny'
    Occitan = 'oc'
    Ojibwa = 'oj'
    Oriya = 'or'
    Oromo = 'om'
    Ossetian = 'os'
    Panjabi = 'pa'
    Persian = 'fa'
    Pali = 'pi'
    Polish = 'pl'
    Portuguese = 'pt'
    Pushto = 'ps'
    Quechua = 'qu'
    RaetoRomance = 'rm'
    Romanian = 'ro'
    Rundi = 'rn'
    Russian = 'ru'
    Sango = 'sg'
    Sanskrit = 'sa'
    Serbian = 'sr'
    Sinhalese = 'si'
    Slovak = 'sk'
    Slovenian = 'sl'
    Sami = 'se'
    Samoan = 'sm'
    Shona = 'sn'
    Sindhi = 'sd'
    Somali = 'so'
    Sotho = 'st'
    Spanish = 'es'
    Sardinian = 'sc'
    Swati = 'ss'
    Sundanese = 'su'
    Swahili = 'sw'
    Swedish = 'sv'
    Tahitian = 'ty'
    Tamil = 'ta'
    Tatar = 'tt'
    Telugu = 'te'
    Tajik = 'tg'
    Tagalog = 'tl'
    Thai = 'th'
    Tibetan = 'bo'
    Tigrinya = 'ti'
    Tonga = 'to'
    Tswana = 'tn'
    Tsonga = 'ts'
    Turkmen = 'tk'
    Turkish = 'tr'
    Twi = 'tw'
    Uighur = 'ug'
    Ukrainian = 'uk'
    Urdu = 'ur'
    Uzbek = 'uz'
    Venda = 've'
    Vietnamese = 'vi'
    Volapuk = 'vo'
    Welsh = 'cy'
    Walloon = 'wa'
    Wolof = 'wo'
    Xhosa = 'xh'
    Yiddish = 'yi'
    Yoruba = 'yo'
    Zhuang = 'za'
    Zulu = 'zu'
    Brazilian = 'pb'
    NoLanguage = 'xn'


class _LocaleKit:

    def __init__(self):
        self.Language = Language
        self.CountryCodes = CountryCodes

        # todo - set the default locale in a better way
        self._default_locale = 'en-us'

    @property
    def DefaultLocale(self):
        # type: () -> str
        """
        Returns the default locale currently in use by the plug-in, e.g. ``en-us``.
        """
        return self._default_locale

    @DefaultLocale.setter
    def DefaultLocale(self, value):
        # type: (str) -> None
        self._default_locale = value

    @property
    def Geolocation(self):
        # type: () -> str
        """
        Returns the user's country, obtained via IP-based geolocation, e.g. ``US``.
        """
        # todo
        return 'US'

    @property
    def CurrentLocale(self):
        # type: () -> Optional[str]
        """
        Returns the locale of the user currently making a request to the plug-in, or *None* if no locale was provided.
        """
        # todo
        return

    def LocalString(self, key):
        # type: (str) -> str
        """
        Retrieves the localized version of a string with the given key. Strings from the user's
        current locale are given the highest priority, followed by strings from the default locale.

        See `String files` for more information on providing localized versions of strings.
        """
        # todo
        return ''

    def LocalStringWithFormat(self, key, *args):
        # type: (str, *any) -> str
        """
        Retrieves the localized version of a string with the given key, and formats it using the
        given arguments.
        """
        # todo
        return ''


Locale = _LocaleKit()
