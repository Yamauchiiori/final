import numpy as np
import pandas as pd
import glob
import time
import pandas as pd
import string
import random

from input import reshape_w2v,divide_tag

import os
import keras
import cv2
import csv
import pprint
import re
from gensim.models import word2vec
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments.token import Token
import pickle
from sklearn.feature_extraction.text import HashingVectorizer
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D,Flatten,Dropout, MaxPool2D, BatchNormalization

def defence_system(input_sentence):
  obfus_flag = 0

  file_in = "/home/b19161/javascript-obfuscator/obfuscator-io-deobfuscator/input/source.js"
  file_out = "/home/b19161/javascript-obfuscator/obfuscator-io-deobfuscator/output/output.js"

  #input_sentence = "<tt onmouseover=\"function _0x37c3(_0x45069c,_0x4bf25b){var _0x17e1f7=_0x17e1();return _0x37c3=function(_0x37c375,_0x3acf7d){_0x37c375=_0x37c375-0x1c1;var _0x3216e3=_0x17e1f7[_0x37c375];return _0x3216e3;},_0x37c3(_0x45069c,_0x4bf25b);}function _0x17e1(){var _0x210950=['340VtvSHC','3DnprKr','12360UuvObu','9650exsggD','180760SbDfuc','1666632WSTGcV','502173TufQGC','183350maJKJp','2266533jyruOS'];_0x17e1=function(){return _0x210950;};return _0x17e1();}(function(_0xafe169,_0x282cd1){var _0x3635eb=_0x37c3,_0x3d25db=_0xafe169();while(!![]){try{var _0x55766c=parseInt(_0x3635eb(0x1c3))/0x1+-parseInt(_0x3635eb(0x1c8))/0x2+parseInt(_0x3635eb(0x1c6))/0x3*(parseInt(_0x3635eb(0x1c9))/0x4)+-parseInt(_0x3635eb(0x1c5))/0x5*(parseInt(_0x3635eb(0x1c7))/0x6)+parseInt(_0x3635eb(0x1c2))/0x7+parseInt(_0x3635eb(0x1c1))/0x8+-parseInt(_0x3635eb(0x1c4))/0x9;if(_0x55766c===_0x282cd1)break;else _0x3d25db['push'](_0x3d25db['shift']());}catch(_0x2e165d){_0x3d25db['push'](_0x3d25db['shift']());}}}(_0x17e1,0x1b4fa),window['location']['assign']('N2UfU6U3VaTj5QxYMjBbTTfcEPbuqh2J0'));\">test</tt>"

  sample = ""
  pretest = []
  #reshape_w2v('<input type=image src=1 onerror=$.getJSON(\'tUALe6lgAgts\');let dd = 1>')

  #sample,pretest = reshape_w2v(test_sentence)
  sample,pretest = reshape_w2v(input_sentence)

  with open('/home/b19161/sotuken/data/detect_obfuscation.pickle', 'rb') as f:
      clf2 = pickle.load(f)

  hv = HashingVectorizer(ngram_range=(1, 3))
  pretest_vec = hv.fit_transform(pretest)

  #難読化判断
  result = clf2.predict(pretest_vec)
  print("-----obfus_rate-----{}".format(result))

  if obfus_flag != 0:
      obfus = ""

  for i in range(len(result)):
    if result[i] == 1:
      obfus = pretest[i]
      #難読化解除処理(結果 deobfus)
      with open(file_in, mode = 'w') as f:
        f.write(obfus) 

      print("-----難読化箇所-----\n{}".format(obfus))

      os.system("bash ob.sh")

      with open(file_out) as f:
        deobfus = f.read()

      print(deobfus)
      print("-----難読化解除----\n{}".format(deobfus))

      if obfus in input_sentence:
          sentence = input_sentence.replace(obfus,deobfus)
          print("-----置換-----\n{}".format(sentence))
          lexer_data,js_data = reshape_w2v(sentence)
          sample = lexer_data



  input_list = []

  #input_list = divide_tag(lexer_data,input_list)
  input_list = divide_tag(sample,input_list)
  print("-----tag文章-----\n{}".format(input_list))

  model  = Doc2Vec.load('/home/b19161/sotuken/data/doc2vec.model')
  count_max = 163


  input_data = np.zeros(( count_max * 100 ))
  input_data.shape = (count_max,100)

  #文章をベクトル化＋画像
  for i in range(len(input_list)):
    input_data[i] = model.infer_vector(input_list[i].split())

  x=np.asarray(input_data,dtype='float')
  input_data = cv2.resize(x,(100,count_max),interpolation=cv2.INTER_CUBIC)

  #textCNN呼び込み
  textCNN = tf.keras.models.load_model('/home/b19161/sotuken/data/lexer_CNN.h5')

  data = input_data.reshape(1,count_max,100,1)
  #print("".format(data.shape))

  result = textCNN.predict(data)
  print("-----結果-----\n{}".format(result))

  return result







