# 기존: from config import __init__ 또는 유사한 import문을 사용하는 경우
import config.config as cfg  # config.py를 직접 import

# 그리고 JSON을 사용할 때는 다음과 같이 참조:
news_categories = cfg.NAVER_NEWS_CATEGORY_JSON
news_sub_categories = cfg.NAVER_NEWS_SUB_CATEGORY_JSON
news_press = cfg.NAVER_NEWS_PRESS_JSON
