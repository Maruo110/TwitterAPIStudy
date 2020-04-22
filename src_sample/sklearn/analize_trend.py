# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import numpy as np

#わかち書き関数
def wakachi(text):
    from janome.tokenizer import Tokenizer
    t = Tokenizer()
    tokens = t.tokenize(text)
    docs=[]
    for token in tokens:
        docs.append(token.surface)
    return docs

#文書ベクトル化関数
def vecs_array(documents):
    from sklearn.feature_extraction.text import TfidfVectorizer

    docs = np.array(documents)
    vectorizer = TfidfVectorizer(analyzer=wakachi,binary=True,use_idf=False)
    vecs = vectorizer.fit_transform(docs)
    return vecs.toarray()

if __name__ == '__main__':
    from sklearn.metrics.pairwise import cosine_similarity
    """
    docs = [
    "私は犬が好きです。",
    "私は犬が嫌いです。",
    "私は犬のことがとても好きです。"]
    """

    docs = [
    "湘南エリアなどの海岸封鎖を 地元自治体が県に要望 新型コロナ  ",
    "《新型コロナ》茨城県内キャンプ場　活況一転　相次ぎ休業 ",
    "神奈川県の湘南鎌倉エリアや三浦半島の海沿いに多くの人が訪れているとして、地元の１１の自治体が黒岩知事に対し海岸エリアの封鎖や利用制限、周辺の道路の通行止めなどの措置を求める要望書を提出。違法駐車が増えているとして、駐車の取り締ま りの徹底も求めている。"]

    #類似度行列作成
    cs_array = np.round(cosine_similarity(vecs_array(docs), vecs_array(docs)),3)
    print(cs_array)
