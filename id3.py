import sys
import csv
import math
import random

class Dtree(object):
    def __init__(self):
        self.data = list()
        self.left = None
        self.right = None
        self.ID = 0
        self.entropy = None
        self.index = None
        self.attribute = None
        self.attributevalue = None
        self.parent = None
        self.ones = None
        self.zeros = None
        self.classoutput = None
    identity = 0

#function to calculate the entropy of the class
def entropy(data,self,wd):
    ones = 0
    zeros = 0
    count = 0
    for i in range(1,len(data)):
        count = count +1
        dt = int(data[i][wd])
        if dt == 0:
            zeros = zeros + 1
        elif dt == 1:
            ones = ones + 1
    self.ones = ones
    self.zeros = zeros
    if ones != 0:
        pos = -(float(ones/count)*math.log(float(ones/count),2))
    else:
        pos = 0
    if zeros != 0:
        neg = -(float(zeros/count)*math.log(float(zeros/count),2))
    else:
        neg = 0
    self.entropy = pos + neg

#function to perform ID3 Algorithm and choose the attribute
def findattr(self,wdt):
    index = -1
    data = self.data
    entro = self.entropy
    bestinfogain = 0.0
    for i in range(0,wdt):
        one = 0
        zeros = 0
        classonepos = 0
        classoneneg = 0
        classzeropos = 0
        classzeroneg = 0
        for j in range(1,len(data)):
            ot = int(data[j][i])
            if ot == 0:
                zeros = zeros + 1
                templabel = int(data[j][wdt])
                if templabel == 0:
                    classzeroneg = classzeroneg + 1
                else:
                    classzeropos = classzeropos + 1
            else:
                one = one + 1
                templabel = int(data[j][wdt])
                if templabel == 0:
                    classoneneg = classoneneg + 1
                else:
                    classonepos = classonepos + 1
        classztot = classzeropos + classzeroneg
        classotot = classonepos + classoneneg
        if classzeroneg != 0:
            p1 = -(float(classzeroneg/classztot)*math.log(float(classzeroneg/classztot),2))
        else:
            p1 = 0
        if classzeropos != 0:
            p2 = -(float(classzeropos/classztot)*math.log(float(classzeropos/classztot),2))
        else:
            p2 = 0
        if classoneneg != 0:
            p3 = -(float(classoneneg/classotot)*math.log(float(classoneneg/classotot),2))
        else:
            p3 = 0
        if classonepos != 0:
            p4 = -(float(classonepos/classotot)*math.log(float(classonepos/classotot),2))
        else:
            p4 = 0
        tot = one + zeros
        childentropy = float(float(zeros / tot) * (p1 + p2)) + float(float(one / tot) * (p3 + p4))
        infogain = entro - childentropy
        if infogain > bestinfogain:
            bestinfogain = infogain
            index = i
    return index

#function to create the tree
def createtree(Node,wd,par):
    Dtree.identity = Dtree.identity + 1
    wd = wd - 1
    Node.ID = Dtree.identity
    Node.parent = par
    entropy(Node.data,Node,wd)
    if Node.entropy != 0 and wd > 0:
        attrindex = findattrrandom(wd)
        Node.index = attrindex
        Node.attribute = Node.data[0][attrindex]
        tempattr = Node.attribute
        temp = Node.data
        for i in range(1,len(Node.data)):
            x = int(Node.data[i][attrindex])
            if x == 0:
                if Node.left is None:
                    Node.left = Dtree()
                    Node.left.data.append(temp[0])
                Node.left.attributevalue = 0
                Node.left.data.append(temp[i])
            else:
                if Node.right is None:
                    Node.right = Dtree()
                    Node.right.data.append(temp[0])
                Node.right.attributevalue = 1
                Node.right.data.append(temp[i])
        if Node.left is not None:
            tmplst = list(zip(*Node.left.data))
            tmplst.pop(attrindex)
            Node.left.data = list(zip(*tmplst))
            createtree(Node.left,wd,tempattr)
        if Node.right is not None:
            tmplst1 = list(zip(*Node.right.data))
            tmplst1.pop(attrindex)
            Node.right.data = list(zip(*tmplst1))
            createtree(Node.right,wd,tempattr)
    else:
        if Node.zeros < Node.ones:
            Node.classoutput = 1
        else:
            Node.classoutput = 0

#function to print the constructed tree
def printtree(node,dis):
    s = dis
    if node.parent is not None:
        op = s+str(node.parent)+"="+str(node.attributevalue)+":"
        op = op[1:]
        print(op, end="")
    if node.attribute is None:
        print(node.classoutput)
    else:
        print()

    if node.left is not None:
        s = s + "|"
        printtree(node.left, s)
    if node.right is not None:
        s = s + "|"
        printtree(node.right,s)

#function to calculate the total number of nodes
def total_nodes(Node):
    if Node is None:
        return 0
    else:
        return total_nodes(Node.left)+total_nodes(Node.right)+1

#function to calculate the number of leaf nodes
def leaf_nodes(Node):
    if Node is None:
        return 0
    if Node.classoutput is not None:
        return 1
    else:
        return leaf_nodes(Node.left)+leaf_nodes(Node.right)

# function to calculate the depth
def depth(self):
    if self.left is None and self.right is None:
        return 1
    return max(depth(self.left), depth(self.right)) + 1

#function to test the data with the constructed tree
def testtree(data,Node,width):
    compare = data[width]
    while Node.classoutput is None:
        if data[Node.index] == "0":
            data.pop(Node.index)
            if Node.left is not None:
                Node = Node.left
            else:
                break
        elif data[Node.index] == "1":
            data.pop(Node.index)
            if Node.right is not None:
                Node = Node.right
            else:
                break
        if Node is None:
            break
    if compare == str(Node.classoutput):
        out = 1
    else:
        out = 0
    return out

#function to call the comparision function for testing data
def treecompare(Node, wdth, tr_test):
    crct = 0
    output = 0
    for i in range (1,len(tr_test)):
        chk = tr_test[i]
        output = testtree(chk, Node, wdth - 1)
        if output == 1:
            crct = crct + 1
    return crct

train_data_path = str(sys.argv[1])
test_data_path = str(sys.argv[2])
valid_data_path = str(sys.argv[3])

#Reads the csv files and stores the data in a list
reader_train = csv.reader(open(train_data_path))
reader_valid = csv.reader(open(valid_data_path))
reader_test = csv.reader(open(test_data_path))
tr_train = list()
tr_test = list()
tr_valid = list()
for i in reader_train:
    tr_train.append(i)
for i in reader_valid:
    tr_valid.append(i)
for i in reader_test:
    tr_test.append(i)

attributenum_train = int(len(tr_train[0])-1)
attributenum_test = int(len(tr_test[0])-1)
attributenum_valid = int(len(tr_valid[0])-1)
totalinstances_train = len(tr_train)
totalinstances_test =  len(tr_test)
totalinstances_valid = len(tr_valid)

#Object is created and tree is constructed
Node = Dtree()
Node.data = tr_train
width = int(len(tr_train[0]))
createtree(Node,width,None)

print("Constructed Tree")
print("----------------------------------")

printtree(Node,"")
print("")

print("Accuracy")
print("---------------------------------")

totalnodes = total_nodes(Node)
leafnodes = leaf_nodes(Node)
crct = treecompare(Node,width,tr_train)
Accuracy = float(crct/(totalinstances_train-1))*100
dpth = depth(Node)

print("Number of training instances="+str(totalinstances_train-1))
print("Number of training attributes="+str(attributenum_train))
print("Total number of nodes in the tree="+str(totalnodes))
print("Number of leaf nodes in the tree="+str(leafnodes))
print("Accuracy of the model on the training dataset="+str(Accuracy))
print("Depth of the node="+dpth)
print("")

crct = treecompare(Node,width,tr_valid)
Accuracy = float(crct/(totalinstances_valid-1))*100

print("Number of validation instances="+str(totalinstances_valid-1))
print("Number of validation attributes="+str(attributenum_valid))
print("Accuracy of the model on the validation dataset before pruning="+str(Accuracy))
print("")

crct = treecompare(Node,width,tr_test)
Accuracy = float(crct/(totalinstances_test-1))*100

print("Number of testing instances="+str(totalinstances_test-1))
print("Number of testing attributes="+str(len(tr_test[0])-1))
print("Accuracy of the model on the testing dataset="+str(Accuracy))
print("")
