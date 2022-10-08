import pandas as pd
import numpy as np
import kss

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # fd = pd.read_csv('review_dataset.csv')
    # print(fd)
    # fd['content'] = fd['content'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    # content = fd['content']
    # print(content.shape)
    # idx = 0
    # file = open('Test.txt', 'w', encoding='utf8')
    # file.write("id\tdocument\tlabel\n")
    # for data in content :
    #     print(data)
    #     text_list = kss.split_sentences(data)
    #     for text in text_list :
    #         idx = idx + 1
    #         file.write("%d\t%s\t%d\n" %(idx, text, 0))
    #     print(text_list)
    #     if idx > 5000 :
    #         print("Finish")
    #         break
    # file.close()
    fd = pd.read_csv('pos_neg_genie_review_dataset.txt', header = 0, delimiter = '\t', quoting=3)
    print(fd)
