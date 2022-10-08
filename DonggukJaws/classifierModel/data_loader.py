import pandas as pd

class DataSet :
    def __init__(self, train_dir, test_dir, genie_dir):
        self.train = pd.read_csv(train_dir, delimiter = '\t', quoting=3)
        self.test = pd.read_csv(test_dir, delimiter = '\t', quoting=3)
        self.genie = pd.read_csv(genie_dir, header = 0, delimiter = '\t', quoting=3)
        self.dataAppend()
        self.checkDataset()

    def checkDataset(self):
        print("DataSet Check : ", len(self.train), len(self.test), len(self.genie))

    def dataAppend(self):
        self.train = self.train.append(self.genie[:3500], ignore_index=True)
        self.test = self.test.append(self.genie[3500:], ignore_index=True)


if __name__ == '__main__' :
    data = DataSet('../data/ratings_train.txt', '../data/ratings_test.txt', '../data/pos_neg_genie_review_dataset.txt')

