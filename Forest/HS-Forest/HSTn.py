# !/usr/bin/env python
# -*-coding:utf-8-*-

from numpy.random import rand, randint


class treeNode:
    def __init__(self):
        self.size = 0
        self.left = None
        self.right = None
        self.height = 0
        self.splitIndex = -1
        self.splitValue = 0
        self.external = False

class HS_Forest(object):

    def __init__(self):
        self.__hlimit = -1
        self.__treeNum = -1
        self.__attr = -1
        self.__trees = list()

    def setup(self, attr, treeNum = 25, hlimit = 6):
        self.__attr = attr
        self.__hlimit = hlimit
        self.__treeNum = treeNum

    def build(self):
        assert (self.__attr > 1), 'attributes number is too less'
        assert (self.__hlimit > 0), "tree height limit is too less"
        assert (self.__treeNum >= 1), 'tree nums is too less'

        mins = list()
        maxs = list()
        for i in range(self.__attr):
            sq = rand()
            mins.append(sq - 2*max(sq, 1-sq))
            maxs.append(sq + 2*max(sq, 1-sq))

        i = 0
        while (i < self.__treeNum):
            tree = self.__buildTree(mins, maxs, 0)
            self.__trees.append(tree)
            i+=1

    def initModel(self, data):
        for tree in self.__trees:
            for item in data:
                self.__updateMass(item, tree, False)

    def __buildTree(self, mins, maxs, curH):
        if curH == self.__hlimit:
            node = treeNode()
            node.external = True
            return node
        node = treeNode()
        node.splitIndex = randint(self.__attr)
        node.splitValue = (mins[node.splitIndex] + maxs[node.splitIndex]) / 2
        maxs[node.splitIndex] = node.splitValue
        node.left = self.__buildTree(mins, maxs, curH+1)
        mins[node.splitIndex] = node.splitValue
        node.right = self.__buildTree(mins, maxs, curH+1)
        return node

    def __updateMass(self, x, node, referenceWindow):
        if node is None:
            return
        node.size += 1
        if node.height < self.__hlimit:
            if x[node.splitIndex] < node.splitValue:
                self.__updateMass(x, node.left, referenceWindow)
            else:
                self.__updateMass(x, node.right, referenceWindow)

    def evaluate(self, data, hlimit = 8):
        scores = list()
        for item in data:
            score = 0
            for tree in self.__trees:
                # score += self.__score(tree, item, 0, hlimit)
                score += self.__score(tree, item, 0, hlimit) * 1.0 / tree.size
            scores.append( 1-2 ** (-1.0*score/self.__treeNum))
            # scores.append(score)
        return scores

    def __score(self, node, instance, curH, hlimit):
        if node.external is True or curH >= hlimit:
            return node.size * (2**curH)
        else:
            if instance[node.splitIndex] < node.splitValue:
                return self.__score(node.left, instance, curH+1, hlimit)
            else:
                return self.__score(node.right, instance, curH+1, hlimit)
