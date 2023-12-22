import numpy as np
import pandas as pd
import glob
import time
import pandas as pd
import string
import random

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

def reshape_w2v(sentence):

  w2vtext = ''
  count = 0

  lexer_html = get_lexer_by_name('html')
  token_html = lexer_html.get_tokens_unprocessed(sentence)
  lexer_js = get_lexer_by_name('JavaScript')

  doubt_script = ''
  doubt_scripts = ['']
  js_flag = 0
  whitespace_flag = 0

  for idx, token_type, token_string in token_html:
    if token_type in Token.Text.Whitespace or (token_type in Token.Text and ' ' == token_string) :
      #純粋な空白かToken.Textで空白のとき
      # whitespace_flag = 1
      pass
      ##print('skip!! to {}:{}'.format(token_type,token_string))
    elif token_type in Token.Literal.String or token_type in Token.Text:
      if token_type in Token.Text.Whitespace :
        pass
      else:
        #if token_type in Token.Punctuation:
        token_string = re.sub('^"?','',token_string)
        token_string = re.sub('"?$','',token_string)
        ##print(token_string)
        #token_string = token_string.replace('attack_tag_must_remove','')

        doubt_save = token_string #""を取った時点ではこいつがjavascriptか単なる文字列かわからない。だから一旦保存

        token_js = lexer_js.get_tokens_unprocessed(token_string)

        js_flag = 1

        for idx2, token_type2,token_string2 in token_js :

          if js_flag != 0:
            doubt_script += token_string2
          # if whitespace_flag != 0:
          #   doubt_script += ' '

          if token_type2 in Token.Text.Whitespace:
            pass
          elif token_type2 in Token.Error:
            #print("error    js:{}".format(token_string2))
            token_string = '"'+doubt_save+'"'
            ##print(token_string)
            # whitespace_flag = 0

            w2vtext += token_string + ' '
            count += 1
            #print('---3 js:{}---'.format(token_type))
            #print(token_string)
            # whitespace_flag = 0
            break

          else:
            w2vtext += token_string2 + ' '
            count += 1
            ##print('---2 js:{}---'.format(token_type2))
            #print(token_string2)
            # whitespace_flag = 0

    else:
      w2vtext += token_string + ' '
      count += 1

      if doubt_script != '':
        doubt_scripts.append(doubt_script)
        doubt_script=''

      js_flag = 0
      ##print('---1{}---'.format(token_type))
      #print(token_string)

  w2vtext = re.sub('\s$','',w2vtext)
  #print(doubt_scripts)
  #print(w2vtext)

  return w2vtext,doubt_scripts

#分かち文字から<>ごと文章に置き換える関数

def divide_tag(sentence,doc_list):
  #sentence += ' a a a a'
  counter = 0
  tag_sentence = ''
  flag = 0

  ##print(sentence)

  sentence = sentence.split()
  for word in sentence:
    ##print(word)
    if word == '<':
      if len(tag_sentence) != 0:
        doc_list.append(tag_sentence)
        counter += 1
        tag_sentence = ''
      flag = 1

    if flag == 1:
      tag_sentence = tag_sentence + ' ' + word

      if word == '>':
        doc_list.append(tag_sentence)
        counter += 1
        flag = 0
        tag_sentence = ''

      continue

    if flag == 0:
      tag_sentence = tag_sentence + ' ' + word

  if len(tag_sentence) != 0:
    doc_list.append(tag_sentence)
    counter += 1

  return doc_list




