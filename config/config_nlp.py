# -----------------------------------------
# teanaps.nlp.Processing
# -----------------------------------------
STOPWORD_PATH = "file/corpus/stopword.txt"
STOPWORD_ORG_PATH = "file/corpus/stopword_org.txt"
CNOUN_PATH = "file/corpus/cnoun.txt"
CNOUN_ORG_PATH = "file/corpus/cnoun_org.txt"
SYNONYM_PATH = "file/corpus/synonym.txt"
SYNONYM_ORG_PATH = "file/corpus/synonym_org.txt"

# -----------------------------------------
# teanaps.nlp.MorphologicalAnalyzer
# -----------------------------------------
# Select Part of Speech Tagger
#POS_TAGGER = "mecab"
POS_TAGGER = "mecab-ko"
# POS_TAGGER = "kkma"
# POS_TAGGER = "okt"
POS_TAG_MAP = {
    "NNG": "NNG", "NNB": "NNB", "NNP": "NNP", "NP": "NP", "NR": "NR", 
    "VV": "VV", "VX": "VX", "VA": "VA", "VCN": "VCN", "VCP": "VCP",
    "MM": "MM", "MAG": "MAG","MAJ": "MAJ", "IC": "IC", 
    "DT": "DT", "EX": "EX", "IN": "IN", "MD": "MD", "PDT": "PDT", "RP": "RP", "TO": "TO",
    "WDT": "WDT", "WP": "WP", "WP$": "WP$", "WRB": "WRB",
    "JKB": "JKB", "JKC": "JKC","JKG": "JKG", "JKO": "JKO", "JKQ": "JKQ", "JKS": "JKS", "JKV": "JKV", 
    "JC": "JC", "JX": "JX", 
    "EC": "EC", "EP": "EP", "EF": "EF", "ETN": "ETN", "ETM": "ETM", 
    "XPN": "XPN", "XSN": "XSN", "XSV": "XSV", "XSA": "XSA", 
    "XR": "XR", "SE": "SW", "SF": "SW", "SH": "OL", "SL": "OL", "SN": "SN", 
    "SS": "SW", "SW": "SW", "SP": "SW", "UN": "UN", "SO": "SW", 
    # For MeCab
    "NNBC": "NNB", "NN": "NNG", "NNS": "NNG", "NNPS": "NNP", "PRP": "NP", "PRP$": "NP", 
    "JJ": "VA", "JJR": "VA", "JJS": "VA", "VB": "VV", "VBG": "VV", "VBN": "VV", "VBZ": "VV", 
    "RB": "MAG", "RBS": "MAG", "RBR": "MAG",
    "UH": "IC", "CC": "JC", "FW": "OL", "CD": "SN",
    "SSO": "SW", "SSC": "SW", "SC": "SW", "SY": "SW", "LS": "SW",
    "UNKNOWN": "UN", "UNT": "UN", "UNA": "UN", "NA": "UN", "E": "UN",
    # For KKMA
    "NNM": "NNB", "VXV": "VX", "VXA": "VX", "VXN": "VX", "MDT": "MM", "MDN": "MM", "MAC": "MAJ",
    "JKM": "JKB", "EPH": "EP", "EPT": "EP", "EPP": "EP", "ECE": "EC", "ECD": "EC", "ECS": "EC",
    "EFN": "EF", "EFQ": "EF", "EFO": "EF", "EFA": "EF", "EFI": "EF", "EFR": "EF", "ETD": "ETM",
    "XPV": "XPN", "OH": "OL", "SL": "OL", "OL": "OL", "ON": "SN", "UV": "UN", "UE": "UN", 
    # For Okt
    "Noun": "NNG", "Adjective": "VA", "Verb": "VV", "Determiner": "MM", "Adverb": "MAG",
    "Conjunction": "MAJ", "Exclamation": "IC", "Josa": "JC", "PreEomi": "EP", "Eomi": "EC",
    "Suffix": "XPN", "Unknown": "UN", "Punctuation": "SW", "Alpha": "OL", "Number": "SN",
    "Foreign": "OL", "Modifier": "MM", "Hashtag": "SW", "KoreanParticle": "SW", "ScreenName": "SW",
    "Email": "SW", "VerbPrefix": "XPN", "URL": "SW", "CashTag": "SW"
}
LEMMATIZER_POS_MAP = {'J': 'a', 'N': 'n', 'R': 'r', 'V': 'v'}
SYMBOLS_POS_MAP = {
    "...": "SW", ".": "SW", "?": "SW", "!": "SW",
    "-": "SW", ",": "SW", "·": "SW", ";": "SW", ":": "SW", "/": "SW",
    "'": "SW", "\"": "SW", "(": "SW", ")": "SW", "<": "SW", ">": "SW",     
}

TAG_CLASSES = ['VV', 'VA', 'NNG+XS', 'NNG+VC', 'XR', 'NNG', 'NNP','VA', 'VV+EC', 'XSV+EP', 'XSV+EF', 'XSV+EC', 'VV+ETM', 'MAG', 'MAJ', 'NP', 'NNBC', 'IC', 'XR', 'VA+EC']
SKIP_WORD_LIST = [
    "/", "무단전재", "무단 전재", "무단복제", "재배포 금지", "저작권자", "레이어 닫기", "영상취재", "사진영상부", "뉴스1", "특파원", "인턴기자", "한국일보", "앵커", "기자", "편집자",
    "경향신문", "헤럴드경제", "뉴스1코리아", "이데일리", "동아일보", "파이낸셜뉴스", "뉴시스", "매일경제", "글로벌 미디어", "한경닷컴", "한국경제", "한경", "연합뉴스", "동아일보"
]