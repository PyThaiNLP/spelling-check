import codecs
import re
import string
from pythainlp.tokenize import tcc
from pythainlp.tokenize import syllable_tokenize as word_tokenize
from pythainlp.corpus.thaisyllable import get_data as syllable_dict
from pythainlp.corpus import stopwords
import sklearn_crfsuite
stopwords = stopwords.words('thai')
invalidChars = set(string.punctuation.replace("_", ""))
dict_s=list(set(syllable_dict()))
def is_special_characters(w):
    if any(char in invalidChars for char in w):
        return True
    else:
        return False
def is_numthai(w):
    return w in list("๑๒๓๔๕๖๗๘๙๐")
def lenbytcc(w):
    return tcc.tcc(w, sep="|=/=|").count('|=/=|')
def in_dict(word):
    return word in dict_s
def has_silencer(word):
    return '์' in word
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
def doc2features(doc, i):
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
        'word.isdigit()': word.isdigit(),
        'word.lentcc':lenbytcc(word),
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
        features['word.prev_is_special_characters'] =is_special_characters(prevword)
    else:
        features['BOS'] = True # Special "Beginning of Sequence" tag
    """if i < len(doc)-1 and i+2< len(doc)-1:
        nextword = doc[i+2][0]
        features['word.next2word'] = nextword
        features['word.next2isspace']=nextword.isspace()
        features['word.next2isthai']=isThaiWord(nextword)
        features['word.next2tonemarks']=has_tonemarks(nextword)
        features['word.next2stopword']=is_stopword(nextword)
        features['word.next2in_dict']=in_dict(nextword)
        features['word.next2in_isnumthai']=is_numthai(nextword)
        features['word.next2silencer']=has_silencer(nextword)
        features['word.next2wordisdigit'] = nextword.isdigit()
        features['word.next2lentcc']=lenbytcc(nextword)
        features['word.next2_is_special_characters']=is_special_characters(nextword)"""
    # Features from next word
    if i < len(doc)-1:
        nextword = doc[i+1][0]
        features['word.nextword'] = nextword
        features['word.nextisspace']=nextword.isspace()
        features['word.nextisthai']=isThaiWord(nextword)
        features['word.nexttonemarks']=has_tonemarks(nextword)
        features['word.nextstopword']=is_stopword(nextword)
        features['word.nextin_dict']=in_dict(nextword)
        features['word.nextin_isnumthai']=is_numthai(nextword)
        features['word.nextsilencer']=has_silencer(nextword)
        features['word.nextwordisdigit'] = nextword.isdigit()
        features['word.nextlentcc']=lenbytcc(nextword)
        features['word.next_is_special_characters']=is_special_characters(nextword)
    else:
        features['EOS'] = True # Special "End of Sequence" tag

    return features

def extract_features(doc):
    return [doc2features(doc, i) for i in range(len(doc))]

def get_labels(doc):
    return [tag for (token,tag) in doc]

crf = sklearn_crfsuite.CRF(
    algorithm='pa',
    #c1=0.1,
    #c2=0.1,
    max_iterations=450,#500,
    all_possible_transitions=True,
    model_filename="sp.model"
)

def get(text):
    word_cut=word_tokenize(text)
    #print(word_cut)
    X_test = extract_features([(i,) for i in word_cut])
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
    return output
