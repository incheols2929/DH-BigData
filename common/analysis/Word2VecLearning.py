import gensim
from gensim.models import Word2Vec
import config.config_database as Dcon
import traceback
import os

from hdfs import InsecureClient
from common.utils import write_log
from config.config import MODEL_PATH


class Word2VecLearning():
    def __init__(self):
        self.model_path = MODEL_PATH
        self.vector_size = 100
        self.window = 5
        self.min_count = 1
        self.workers = 4
        self.sg = 0

    def makeModel(self, data, path):
        try:
            if not data:  # 데이터가 비어있으면 처리하지 않음
                write_log('입력 데이터가 비어있어 처리를 건너뜁니다.')
                return

            # 모델 로드 또는 새로 생성
            model = self._load_or_create_model()

            # 증분 학습 수행
            self._incremental_training(model, data)

            # 모델 저장
            self._save_model(model)

            # 두 개의 인자를 하나의 문자열로 합쳐서 전달
            write_log(f'모델 벡터 크기==> {model.wv.vectors.shape}')
            write_log(f'학습된 단어 수==> {len(model.wv.index_to_key)}')

        except Exception as e:
            write_log('모델 학습 중 오류 발생:')
            write_log(traceback.format_exc())
            raise e

    def _load_or_create_model(self):
        """모델을 로드하거나 새로 생성"""
        try:
            if os.path.exists(self.model_path):
                write_log('기존 모델을 로드합니다...')
                return Word2Vec.load(self.model_path)
            else:
                write_log('새로운 모델을 생성합니다...')
                return Word2Vec(vector_size=self.vector_size,
                                window=self.window,
                                min_count=self.min_count,
                                workers=self.workers,
                                sg=self.sg)
        except Exception as e:
            write_log('모델 로드/생성 중 오류:')
            write_log(traceback.format_exc())
            raise e

    def _incremental_training(self, model, data):
        """증분 학습 수행"""
        try:
            if not data:
                write_log('학습할 데이터가 없습니다.')
                return

            # 디버깅을 위한 데이터 상세 정보 출력
            write_log(f'입력 데이터 타입: {type(data)}')
            write_log(f'전체 데이터 길이: {len(data)}')
            if isinstance(data, list):
                write_log(f'첫 번째 항목 샘플: {data[0] if data else "없음"}')

            # 데이터 유효성 검사 및 필터링
            valid_sentences = [sentence for sentence in data if isinstance(sentence, list) and len(sentence) > 0]
            write_log(f'유효한 문장 수: {len(valid_sentences)}')

            if not valid_sentences:
                write_log('유효한 문장이 없습니다.')
                return

            write_log('어휘 사전을 업데이트합니다...')
            # 현재 어휘 크기 출력
            write_log(f'업데이트 전 어휘 사전 크기: {len(model.wv.key_to_index)}')

            model.build_vocab(valid_sentences, update=True)

            write_log(f'업데이트 후 어휘 사전 크기: {len(model.wv.key_to_index)}')

            epochs = 5
            write_log(f'모델 학습을 시작합니다... (epochs: {epochs})')

            model.train(valid_sentences,
                        total_examples=len(valid_sentences),
                        epochs=epochs)

            write_log(f'학습 완료: {len(model.wv.key_to_index)} 단어')

        except Exception as e:
            write_log('증분 학습 중 오류:')
            write_log(traceback.format_exc())
            raise e

    def _save_model(self, model):
        """모델 저장"""
        try:
            # 모델 저장 디렉토리 확인 및 생성
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

            write_log('모델을 저장합니다...')
            model.save(self.model_path)
            write_log(f'모델이 {self.model_path}에 저장되었습니다.')

        except Exception as e:
            write_log('모델 저장 중 오류:')
            write_log(traceback.format_exc())
            raise e

