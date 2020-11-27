import jieba
jieba.enable_parallel(4)
import os
from os import path
from wordcloud import WordCloud

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
# d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
stopwords_path = './stopwords_cn_en.txt'
font_path = './font/simsun.ttc'
userdict_list = ['招募', '美区', '时间', '收留','近战','找到','陪练','接收']


# The function for processing text with Jieba
def jieba_processing_txt(text):
    for word in userdict_list:
        jieba.add_word(word)

    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)

    with open(stopwords_path, encoding='utf-8') as f_stop:
        f_stop_text = f_stop.read()
        f_stop_seg_list = f_stop_text.splitlines()

    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ' '.join(mywordlist)


# Read the whole text.
text = open('nga_thread.csv').read()

wc = WordCloud(font_path=font_path, max_words=2000, max_font_size=40)

# Generate a word cloud image
wordcloud = wc.generate(jieba_processing_txt(text))

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")


# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()