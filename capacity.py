#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 23:30:34
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import math
import operator as op


class Node(object):
    def __init__(self, selectedElements, total):
        super(Node, self).__init__()

        assert (
            selectedElements >= 1 and
            selectedElements <= total), selectedElements

        self._selectedElements = selectedElements  # i.e., bi, [1, ai]
        self._sumOfChildren = 1  # the sum of value of all the children nodes
        self.k = 0  # i.e., layer. For root node, this value is 0
        self._numberOfArrange = nPr(total, selectedElements)

    def __str__(self):
        return '(%d, %d, %d)' % (
            self.numberOfArrange, self.sumOfChildren, self._selectedElements)

    @property
    def value(self):
        return self.numberOfArrange * (
            self.sumOfChildren ** self._selectedElements)

    @property
    def numberOfArrange(self):
        return self._numberOfArrange

    @property
    def sumOfChildren(self):
        return self._sumOfChildren

    @sumOfChildren.setter
    def sumOfChildren(self, value):
        self._sumOfChildren = value


class Layer(object):
    def __init__(self, num):
        super(Layer, self).__init__()

        self._numberOfNodes = num

        self._nodes = []
        self._sumOfNodes = 0

        for i in xrange(num):
            node = Node(i + 1, num)
            self._nodes.append(node)

    def __iter__(self):
        return iter(self._nodes)

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, index):
        return self._nodes[index]

    def __str__(self):
        ret = []
        for node in self:
            ret.append(str(node))
        return ', '.join(ret)

    @property
    def sumOfNodes(self):
        ret = 0
        for node in self:
            ret += node.value
        return ret  # nodes' value, current layer


class Tree(object):
    def __init__(self, base):
        super(Tree, self).__init__()

        assert isinstance(base, list), base

        self._layers = []

        self.addLayer(1)  # root layer

        for x in base:
            self.addLayer(x)  # each layer

        # Calculate value for each layer
        for i in xrange(len(self) - 2, -1, -1):
            lowLayer = self._layers[i + 1]
            highLayer = self._layers[i]

            # Update each node in high loyer
            for node in highLayer:
                node.sumOfChildren = lowLayer.sumOfNodes

    def __iter__(self):
        return iter(self._layers)

    def __len__(self):
        return len(self._layers)

    def __getitem__(self, index):
        return self._layers[index]

    def __str__(self):
        ret = []
        for layer in self:
            ret.append(str(layer))
        return '\n'.join(ret)

    def addLayer(self, num):
        self._layers.append(Layer(num))


# k-hierarchy
def Cn(A, i):
    if i == len(A) - 1:
        return sum([nPr(A[i], bi) for bi in xrange(1, A[i] + 1)])

    return sum(
        [nPr(A[i], bi) * (Cn(A, i + 1) ** bi) for bi in xrange(1, A[i] + 1)])


def calTotal(A):
    return Cn(A, 0) + 1  # 1 for empty


def unrank(base, aRank):
    '''rank -> tree'''
    pass


def rank(base, aTree):
    '''tree -> rank'''
    pass


def inner(aList):
    f = math.factorial
    ret = reduce(op.mul, [f(ai) for ai in aList])

    if len(aList) == 1:
        return ret

    return ret * nCr(aList[-1] - 1, aList[-2] - 1)


def nCarrierRider(aList, n):
    '''R: rider, n: hierarchy'''
    assert n >= 1, n
    assert len(aList) >= 1, aList

    if n == 1:
        return inner(aList)

    ret = 0
    for i in xrange(1, aList[0] + 1):
        ret += nCarrierRider([i] + aList, n - 1)

    return ret


def kHierarchy2(aList, R):
    if len(aList) == 0:
        return 0

    if len(aList) == 1:
        return nPr(aList[0], R)

    # n >= 2
    ret = 0
    for i in xrange(1, min(R, aList[0]) + 1):
        ret += (
            nPr(aList[0], i) * kHierarchy2(aList[1:], R) * nCr(R - 1, i - 1))

    return ret


# Permutation
def unrankPermutation(n, aRank, aList=None):
    '''rank -> permutation'''
    # Init
    ret = aList or range(n)

    if n <= 0:
        return ret

    # Swap
    ret[n - 1], ret[aRank % n] = ret[aRank % n], ret[n - 1]

    # Recursive call
    return unrankPermutation(n - 1, int(math.floor(aRank / n)), ret)


def rankPermutation(n, aList1, aList2=None):
    '''permutation -> rank'''
    if n == 1:
        return 0

    # Init: list 2
    if aList2 is None:
        aList2 = list(aList1)
        for i in xrange(n):
            aList2[aList1[i]] = i

    s = aList1[n - 1]

    # Swap: list 1
    aList1[n - 1], aList1[aList2[n - 1]] = aList1[aList2[n - 1]], aList1[n - 1]

    # Swap: list 2
    aList2[s], aList2[n - 1] = aList2[n - 1], aList2[s]

    return s + n * rankPermutation(n - 1, aList1, aList2)


# Permutation 2
def unrankPermutation2(n, aRank, aList=None):
    '''rank -> permutation'''
    # Init
    ret = aList or range(n)

    if n <= 0:
        return ret

    s = int(math.floor(aRank / math.factorial(n - 1)))

    # Swap
    ret[n - 1], ret[s] = ret[s], ret[n - 1]

    # Recursive call
    return unrankPermutation2(n - 1, aRank % math.factorial(n - 1), ret)


def rankPermutation2(n, aList1, aList2=None):
    '''permutation -> rank'''
    if n == 1:
        return 0

    # Init: list 2
    if aList2 is None:
        aList2 = list(aList1)
        for i in xrange(n):
            aList2[aList1[i]] = i

    s = aList1[n - 1]

    # Swap: list 1
    aList1[n - 1], aList1[aList2[n - 1]] = aList1[aList2[n - 1]], aList1[n - 1]

    # Swap: list 2
    aList2[s], aList2[n - 1] = aList2[n - 1], aList2[s]

    return s * math.factorial(n - 1) + rankPermutation2(n - 1, aList1, aList2)


# Combination
def unrankCombination(n, k, aRank):
    '''rank -> combination'''
    assert aRank >= 0 and aRank <= nCr(n, k) - 1, aRank  # [0, nCr(n, k) - 1]

    # Init
    x = 1
    ret = [0] * k  # combination

    for i in xrange(1, k + 1):
        while nCr(n - x, k - i) <= aRank:
            aRank -= nCr(n - x, k - i)
            x += 1
        ret[i - 1] = x - 1
        x += 1

    return ret


def rankCombination(n, k, aList):
    '''combination -> rank'''
    # Init
    ret = 0  # rank
    tList = list(aList)
    tList.insert(0, -1)  # t0 <- 0

    for i in xrange(1, k + 1):
        if tList[i - 1] + 1 <= tList[i] - 1:
            for j in xrange(tList[i - 1] + 2, tList[i] + 1):
                ret += nCr(n - j, k - i)

    return ret


# Integer partition
def unrankIntegerPartition(m, n, aRank):
    '''rank -> integer partition list'''
    # Init
    P = enumPartition(m, n)
    ret = [0] * n

    while m > 0:
        if aRank < P[m - 1][n - 1]:
            ret[n - 1] += 1
            m -= 1
            n -= 1
        else:
            for i in xrange(n):
                ret[i] += 1
            aRank -= P[m - 1][n - 1]
            m -= n

    return ret


def rankIntegerPartition(m, n, aList):
    '''integer partition list -> rank'''
    assert len(aList) == n, aList
    assert sum(aList) == m, aList

    # Init
    P = enumPartition(m, n)
    tList = list(aList)  # copy
    ret = 0  # rank

    while m > 0:
        if tList[n - 1] == 1:
            m -= 1
            n -= 1
        else:
            for i in xrange(n):
                tList[i] -= 1
            ret += P[m - 1][n - 1]
            m -= n

    return ret


def enumPartition(m, n):
    # Init
    P = [[0 for i in xrange(n + 1)] for j in xrange(m + 1)]
    P[0][0] = 1

    for i in xrange(1, m + 1):
        for j in xrange(1, min(i, n) + 1):
            if i < 2 * j:
                P[i][j] = P[i - 1][j - 1]
            else:
                P[i][j] = P[i - 1][j - 1] + P[i - j][j]

    return P


# Set partition
def unrankSetPartition(m, n, aRank):
    '''rank -> set partition list'''
    from sympy.combinatorics.partitions import Partition
    from sympy.combinatorics.partitions import RGS_unrank
    rgs = RGS_unrank(aRank, m)
    setPartition = Partition.from_rgs(rgs, range(m))
    return setPartition.partition


def rankSetPartition(m, n, aList):
    '''set partition list -> rank'''
    from sympy.combinatorics.partitions import Partition
    setPartition = Partition(*aList)
    return setPartition.rank


def enumSetPartition(m, n):
    '''m <= n'''
    S = [[0 for i in xrange(n + 1)] for j in xrange(m + 1)]
    S[0][0] = 1

    for i in xrange(1, m + 1):
        for j in xrange(1, min(i, n) + 1):
            S[i][j] = j * S[i - 1][j] + S[i - 1][j - 1]

    return S


def nCr(n, k):
    f = math.factorial
    return f(n) / f(k) / f(n - k)


def nPr(n, k):
    f = math.factorial
    return f(n) / f(n - k)


def update(aBase, aNum):
    assert len(aBase) == len(aNum)

    i = len(aNum) - 1

    aNum[i] += 1

    while aNum[i] > aBase[i]:
        aNum[i] = aNum[i] - aBase[i]

        if i - 1 < 0:
            break

        aNum[i - 1] += 1
        i -= 1


def main(A):
    N = len(A)
    B = N * [1]

    total = 0
    while True:
        current = 1

        for i in xrange(N):
            current *= nPr(A[i], B[i])

        update(A, B)

        total += current

        if B == N * [1]:
            break

    return total


def T9(R):
    ret = 0
    for i in xrange(1, R + 1):
        ret += T9Outer(R, i)
    return ret


def T9Outer(R, i):
    f = math.factorial
    return f(i) * f(R) * nCr(R - 1, i - 1)


def T5(R):
    ret = 0
    f = math.factorial
    S = enumSetPartition(R, R)
    for i in xrange(1, R + 1):
        ret += (f(i) * S[R][i])
    return ret


def T5Outter(R, i):
    f = math.factorial
    S = enumSetPartition(R, R)
    return f(i) * S[R][i]


def getNumberOfCarrier9(A, R):
    I = 0
    Val = 0

    while A >= 0:
        I += 1
        Val = A
        A -= T9Outer(R, I)

    return I, Val


def splitVal9(Val, R, I):
    f = math.factorial
    U = Val % (f(R) * f(I))
    V = int(math.floor(Val / (f(R) * f(I))))
    U1 = U % f(R)
    U2 = int(math.floor(U / f(R)))

    return U1, U2, V


if __name__ == '__main__':
    print unrankSetPartition(4, 3, 0)
    print unrankSetPartition(4, 3, 1)
    print unrankSetPartition(4, 3, 2)
    print unrankSetPartition(4, 3, 3)
    print unrankSetPartition(4, 3, 4)
    print unrankSetPartition(4, 3, 5)

    print unrankSetPartition(4, 3, 6)

    print enumSetPartition(20, 10)[20][10]
