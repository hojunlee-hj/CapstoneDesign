import pandas as pd
import numpy as np
import kss

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fd = pd.read_csv('appstore_review_test_3420.csv')
    print(fd)
    fd['review'] = fd['review'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
    content = fd['review']
    print(content.shape)
    idx = 0
    file = open('Test.csv', 'w', encoding='utf8')
    file.write("id\tdocument\tlabel\tlabel2\n")
    for data in content:
        print(data)
        text_list = kss.split_sentences(data)
        for text in text_list:
            idx = idx + 1
            file.write("%d\t%s\t%d\t%d\n" % (idx, text, 0, 0))
        print(text_list)

    fd2 = pd.read_csv('review_dataset.csv')
    print(fd2)
    fd2['content'] = fd2['content'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    content2 = fd2['content']
    print(content2.shape)
    file = open('Test.csv', 'a', encoding='utf8')
    for data in content2 :
        print(data)
        text_list = kss.split_sentences(data)
        for text in text_list :
            idx = idx + 1
            file.write("%d\t%s\t%d\t%d\n" %(idx, text, 0, 0))
        print(text_list)

    print("Finish");
    file.close()
    # fd = pd.read_csv('pos_neg_genie_review_dataset.txt', header = 0, delimiter = '\t', quoting=3)
    # print(fd)
