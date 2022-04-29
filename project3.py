from dis import dis
import math
import random as rd
from turtle import update
import pandas as pd


DATA = pd.read_csv('Mall_Customers.csv')
COLS = DATA.columns[1:]


def compareList(a,b):
    if len(a) != len(b):
        return False

    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


def isExistList(a,b):
    for i in range(len(b)):
        if compareList(a,b[i]):
            return True
    return False


#data preprocessing
def normalize():
    #numeric columns
    numeric_cols = COLS[1:]
    DATA[numeric_cols]= DATA[numeric_cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    #String column 0 if Male else 1
    string_col = COLS[0]
    DATA[string_col]= DATA[string_col].apply(lambda x: 0 if (x=="Male") else 1 )
    

#euclid distance 
def euclidDist(a,b):
    if type(a) == 'int':
        a=[a]
        b=[b]
    
    result = 0
    for i in range(len(a)):
        result+= math.pow((a[i]-b[i]),2)
    
    return math.sqrt(result)


def dataToRows():
    rows=DATA.values.tolist()

    for i in range(len(rows)):
        rows[i] = rows[i][1:]

    return rows


def clustering(rows, centers):
    group_matrix = []

    #clustering
    for i in range(len(rows)):
        if isExistList(rows[i],centers):
            continue

        min_val = 999999
        min_idx = -1
        for j in range(len(centers)):
            dist = euclidDist(rows[i],centers[j])
            if dist < min_val:
                min_val = dist
                min_idx = j

        group_matrix.append(min_idx)
    
    return group_matrix


def updateCenters(rows, groups, k):
    new_centers = []

    for i in range(k):
        count = 0
        temp =[0] * len(rows[0])

        for j in range(len(groups)):

            if groups[j] == i:
                count += 1
                for k in range(len(rows[j])):
                    temp[k] += rows[j][k]

        if (count != 0):
            for c in range(len(temp)):
                temp[c] /= count

        new_centers.append(temp)
    
    return new_centers


def kMean(k):
    rows  = dataToRows()

    if k > len(rows):
        return False

    #random choice
    centers_idx = rd.sample(range(0,len(rows)),k)
    centers = []

    for i in range(len(centers_idx)):
        centers.append(rows[centers_idx[i]])
    
    cluster_mtrix = []

    while True:
        old_cluster_mtrix = cluster_mtrix

        #clustering
        cluster_mtrix = clustering(rows, centers)

        #stop condition
        if compareList(cluster_mtrix,old_cluster_mtrix):
            break

        #update center
        centers = updateCenters(rows, cluster_mtrix, k)

    #distributing to clusters
    result = {}
    for i in range(k):
        result[i] = []

    for i in range(len(cluster_mtrix)):
        result[cluster_mtrix[i]].append(i)
    
    return result

        

normalize()
clusters = kMean(3)
print(clusters)


