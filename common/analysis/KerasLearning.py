import tensorflow as tf
import pickle
import traceback

from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, Dropout, GlobalMaxPool1D
from tensorflow.keras.utils import to_categorical

from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from hdfs import InsecureClient

import config.config_database as Dcon
from common.utils import write_log
class KerasLearning():  
    def __init__(self):
        None

    def makeModel(self, x_data, y_data, path) :
        set_y_data = list(set(y_data))
        nb_classes = len(set(y_data))

        y_data = [list(set(set_y_data)).index(data) for data in y_data]
        y_data = to_categorical(y_data, nb_classes)

        max_word = 7000
        max_len = 500

        tok = Tokenizer(num_words = max_word)
        tok.fit_on_texts(x_data)

        sequences = tok.texts_to_sequences(x_data)
        write_log(sequences[0])

        sequences_matrix = sequence.pad_sequences(sequences, maxlen=max_len)

        x_train, x_test, y_train, y_test = train_test_split(sequences_matrix, y_data, test_size=0.2)
        write_log(x_train.shape)

        with tf.device('/device:GPU:0'):
            model = Sequential()
            
            model.add(Embedding(max_word, 64, input_length=max_len))
            model.add(LSTM(60, return_sequences=True))
            model.add(GlobalMaxPool1D())
            model.add(Dropout(0.2))
            model.add(Dense(50, activation='relu'))
            model.add(Dropout(0.5))
            model.add(Dense(nb_classes, activation='softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            checkpoint = ModelCheckpoint(filepath='./datas/' + path + '/keras_lstm.h5', monitor="val_loss", verbose=1, save_best_only=True)
            early_stopping = EarlyStopping(monitor='val_loss', patience=3)

        model.summary()

        hist = model.fit(x_train, y_train, batch_size=500, epochs=20, validation_split=0.2, callbacks=[checkpoint, early_stopping])
        write_log("정확도 : %.4f" % (model.evaluate(x_test, y_test)[1]))

        # saving
        with open('datas/' + path + '/tokenizer.pickle', 'wb') as handle:
            pickle.dump(tok, handle, protocol=pickle.HIGHEST_PROTOCOL)

        try :
            # HDFS 클라이언트와 연결합니다.
            client = InsecureClient(Dcon.HDFS_URL, user=Dcon.HDFS_USER)

            # HDFS의 디렉토리를 생성합니다.
            client.makedirs('data')

            # 파일을 업로드합니다.
            client.upload('data/' +  path + '/keras_lstm.h5', 'datas/' +  path + '/keras_lstm.h5', overwrite=True)

            # 파일을 업로드합니다.
            client.upload('data/' +  path + '/tokenizer.pickle', 'datas/' +  path + '/tokenizer.pickle', overwrite=True)
        except Exception as e:
            write_log(traceback.format_exc())