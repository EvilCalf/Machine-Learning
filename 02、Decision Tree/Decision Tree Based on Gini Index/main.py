import pandas as pd
import numpy as np
import random

data_file_encode = "utf-8"
with open(
    r"D:\MyProject\Machine Learning\data\watermelon_2.csv", mode="r", encoding=data_file_encode
) as data_file:
    DataSet = pd.read_csv(data_file)

import DT as decision_tree

# 划分训练集和测试集
index = DataSet.shape[0] - 1
index_train = np.arange(index)
rand_train = np.random.choice(
    index_train, size=random.randint(int((index + 1) / 2), index), replace=False
)

DataSet_train = DataSet.iloc[rand_train]
DataSet_test = DataSet.drop(rand_train)

# generate a full tree
root = decision_tree.TreeGenerate(DataSet_train)
decision_tree.DrawPNG(
    root,
    "Decision Tree/Decision Tree Based on Gini Index/Decision Tree Based on Gini Index.png",
)
print("accuracy of full tree: %.3f" % decision_tree.PredictAccuracy(root, DataSet_test))

# pre-purning 预剪枝
root = decision_tree.PrePurn(DataSet_train, DataSet_test)
decision_tree.DrawPNG(
    root, "Decision Tree/Decision Tree Based on Gini Index/decision_tree_pre.png"
)
print(
    "accuracy of pre-purning tree: %.3f"
    % decision_tree.PredictAccuracy(root, DataSet_test)
)

# # post-puring 后剪枝
root = decision_tree.TreeGenerate(DataSet_train)
decision_tree.PostPurn(root, DataSet_test)
decision_tree.DrawPNG(
    root, "Decision Tree/Decision Tree Based on Gini Index/decision_tree_post.png"
)
print(
    "accuracy of post-purning tree: %.3f"
    % decision_tree.PredictAccuracy(root, DataSet_test)
)

# print the accuracy
# k-folds cross prediction k折交叉验证法
accuracy_scores = []
n = len(DataSet.index)
k = 5
for i in range(k):
    m = int(n / k)
    test = []
    for j in range(i * m, i * m + m):
        test.append(j)

    DataSet_train = DataSet.drop(test)
    DataSet_test = DataSet.iloc[test]
    root = decision_tree.TreeGenerate(DataSet_train)  # generate the tree
    decision_tree.PostPurn(root, DataSet_test)  # post-purning

    # test the accuracy
    pred_true = 0
    for i in DataSet_test.index:
        label = decision_tree.Predict(root, DataSet[DataSet.index == i])
        if label == DataSet_test[DataSet_test.columns[-1]][i]:
            pred_true += 1

    accuracy = pred_true / len(DataSet_test.index)
    accuracy_scores.append(accuracy)

# print the prediction accuracy result
accuracy_sum = 0
print("accuracy: ", end="")
for i in range(k):
    print("%.3f  " % accuracy_scores[i], end="")
    accuracy_sum += accuracy_scores[i]
print("\naverage accuracy: %.3f" % (accuracy_sum / k))
