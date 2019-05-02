# -*- coding: utf-8 -*-
import codecs
import re
import string
import os
import pythaispell
from pythainlp.tokenize import tcc
from pythainlp.tokenize import syllable_tokenize as word_tokenize
import sklearn_crfsuite
from pythainlp.spell.pn import NorvigSpellChecker
try:
    from pythainlp.corpus.thaisyllable import get_data as syllable_dict
    from pythainlp.corpus import stopwords
    stopwords = stopwords.words('thai')
except:
    from pythainlp.corpus.common import thai_syllables,thai_stopwords
    stopwords = list(thai_stopwords())
    syllable_dict = thai_syllables

templates_file = os.path.join(os.path.dirname(pythaispell.__file__),"sp.model")
invalidChars = set(string.punctuation.replace("_", ""))
dict_s=list(set(syllable_dict()))
def c(word):
    for i in list('กขฃคฆงจชซญฎฏฐฑฒณดตถทธนบปพฟภมยรลวศษสฬอ'):
        if i in word:
            return True
    return False
def n(word):
    for i in list('ฅฉผฟฌหฮ'):
        if i in word:
            return True
    return False
def v(word):
    for i in list('ะาำิีืึุู'):
        if i in word:
            return True
    return False
def w(word):
    for i in list('เแโใไ'):
        if i in word:
            return True
    return False
def is_special_characters(w):
    if any(char in invalidChars for char in w):
        return True
    else:
        return False
def is_numthai(w):
    return w in list("๑๒๓๔๕๖๗๘๙๐")
def lenbytcc(w):
    return tcc.segment(w)
def in_dict(word):
    return word in dict_s
def has_silencer(word):
    for i in list('์ๆฯ.'):
        if i in word:
            return True
    return False
def has_tonemarks(word):
    t=False
    for i in ['่','้','็','๊','๋']:
        if i in word:
            t=True
    return t
def isThai(chr):
 cVal = ord(chr)
 if(cVal >= 3584 and cVal <= 3711):
  return True
 return False
def isThaiWord(word):
 t=True
 for i in word:
  l=isThai(i)
  if l!=True and i!='.':
   t=False
   break
 return t

def is_stopword(word):
    return word in stopwords
def is_s(word):
    if word == " " or word =="\t" or word=="" or word=="\r\n" or word=="\n":
        return True
    else:
        return False

def lennum(word,num):
    if len(word)==num:
        return True
    return False
def _doc2features(doc, i):
    word = doc[i][0]
    # Features from current word
    features={
        'word.word': word,
        'word.stopword': is_stopword(word),
        'word.isthai':isThaiWord(word),
        'word.isnumthai':is_numthai(word),
        'word.isspace':word.isspace(),
        'word.tonemarks':has_tonemarks(word),
        'word.in_dict':in_dict(word),
        'word.silencer':has_silencer(word),
        'word.isdigit': word.isdigit(),
        'word.lentcc':lenbytcc(word),
        'word.c':c(word),
        'word.n':n(word),
        'word.v':v(word),
        'word.w':w(word),
        'word.is_special_characters':is_special_characters(word)
    }
    if i > 0:
        prevword = doc[i-1][0]
        features['word.prevword'] = prevword
        features['word.previsspace']=prevword.isspace()
        features['word.previsthai']=isThaiWord(prevword)
        features['word.prevstopword']=is_stopword(prevword)
        features['word.prevtonemarks']=has_tonemarks(prevword)
        features['word.previn_dict']=in_dict(prevword)
        features['word.previn_isnumthai']=is_numthai(prevword)
        features['word.prevsilencer']=has_silencer(prevword)
        features['word.prevwordisdigit'] = prevword.isdigit()
        features['word.prevlentcc'] = lenbytcc(prevword)
        features['word.prev_c'] = c(prevword)
        features['word.prev_n'] = n(prevword)
        features['word.prev_w'] = w(prevword)
        features['word.prev_v'] = v(prevword)
        features['word.prev_is_special_characters'] =is_special_characters(prevword)
    else:
        features['BOS'] = True # Special "Beginning of Sequence" tag
    # Features from next word
    if i < len(doc)-1:
        nextword = doc[i+1][0]
        features['word.nextword'] = nextword
        features['word.next_isspace']=nextword.isspace()
        features['word.next_isthai']=isThaiWord(nextword)
        features['word.next_tonemarks']=has_tonemarks(nextword)
        features['word.next_stopword']=is_stopword(nextword)
        features['word.next_in_dict']=in_dict(nextword)
        features['word.next_in_isnumthai']=is_numthai(nextword)
        features['word.next_silencer']=has_silencer(nextword)
        features['word.next_wordisdigit'] = nextword.isdigit()
        features['word.next_lentcc']=lenbytcc(nextword)
        features['word.next_c']=c(nextword)
        features['word.next_n']=n(nextword)
        features['word.next_w']=w(nextword)
        features['word.next_v']=v(nextword)
        features['word.next_is_special_characters']=is_special_characters(nextword)
    else:
        features['EOS'] = True # Special "End of Sequence" tag

    return features

def _extract_features(doc):
    return [_doc2features(doc, i) for i in range(len(doc))]

crf = sklearn_crfsuite.CRF(
    algorithm='pa',
    #c1=0.1,
    #c2=0.1,
    max_iterations=450,#500,
    all_possible_transitions=True,
    model_filename=templates_file
)
check=NorvigSpellChecker()
checking=""

def spell(text,autocorrect=False,worddict=None):
    global check,checking
    word_cut=word_tokenize(text)
    if worddict=="thai2fit" and checking=="":
        from pythainlp.word_vector import get_model
        words = get_model().index2word
        w_rank = {}
        for i,word in enumerate(words):
            w_rank[word] = i
        word=w_rank.items()
        check=NorvigSpellChecker(custom_dict=word)
        checking="thai2fit"
    elif checking=="thai2fit" and worddict!=None:
        pass
    else:
        checking=""
        check=NorvigSpellChecker()
    #print(word_cut)
    X_test = _extract_features([(i,) for i in word_cut])
    #print(X_test)
    y_=crf.predict_single(X_test)
    x= [(word_cut[i],data) for i,data in enumerate(y_)]
    output=""
    temp=''
    #print(x)
    for i,b in enumerate(x):
        if i==len(x)-1 and 'B' in b[1] and temp=='B':
            output+="</คำผิด><คำผิด>"+b[0]+"</คำผิด>"
            temp='B'
        elif i==len(x)-1 and 'B' in b[1]:
            output+="<คำผิด>"+b[0]+"</คำผิด>"
            temp='B'
        elif 'B-' in b[1] and temp=='B':
            output+="</คำผิด><คำผิด>"+b[0]
            temp='B'
        elif 'B-' in b[1]:
            output+="<คำผิด>"+b[0]
            temp='B'
        elif 'O' in b[1] and temp=='B':
            output+="</คำผิด>"+b[0]
            temp='O'
        elif i==len(x)-1 and 'I' in b[1] and temp=='B':
            output+=b[0]+"</คำผิด>"
            temp='O'
        else:
            output+=b[0]
    if autocorrect:
        f="(<คำผิด>)(.*)(</คำผิด>)"
        output=output.replace("<คำผิด>","|---|<คำผิด>|---|").replace("</คำผิด>","|---|</คำผิด>|---|")
        listall=output.split("|---|")
        i=0
        output=""
        ii=len(listall)
        while i<ii:
            if listall[i]=="<คำผิด>":
                output+=check.correct(listall[i+1])
                i+=3
            else:
                output+=listall[i]
                i+=1
    return output
