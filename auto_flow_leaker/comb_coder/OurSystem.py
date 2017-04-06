#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-14 16:52:36
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import math
from copy import deepcopy


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def nCr(n, k):
    if k > n:
        return 0

    if n == 0 or k == 0:
        return 1

    f = math.factorial
    return f(n) / f(k) / f(n - k)


def nPr(n, k):
    f = math.factorial
    return f(n) / f(n - k)


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
    return unrankPermutation(n - 1, aRank // n, ret)


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

    s = aRank // math.factorial(n - 1)

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


# Set partition
# reference: https://books.google.com.hk/books?id=Ib80AAAAQBAJ&pg=RA2-PR49&lpg=RA2-PR49&dq=rank+unranked+set+partition&source=bl&ots=YqRodZKNMg&sig=T2P6MFSvr0nNgHDoRyVLnet1u2E&hl=en&sa=X&redir_esc=y#v=onepage&q=rank%20unranked%20set%20partition&f=false
def unrankSetPartition(m, n, aRank, aList=None):
    '''rank -> set partition list'''
    assert m >= 0, m
    assert n >= 0 and n <= m, n

    # Init
    ret = aList or range(m)
    assert len(ret) == m, (m, ret)

    if aRank == 0:
        return [[ret[i]] for i in xrange(n - 1)] + [ret[-(len(ret) - n + 1):]]

    s = enumSetPartition(m - 1, n - 1)[m - 1][n - 1]
    if aRank < s:
        return [[ret[0]]] + unrankSetPartition(
            m - 1, n - 1, aRank, aList=ret[1:])
    else:
        t = aRank - s
        j = t % n
        tempSP = unrankSetPartition(
            m - 1, n, t // n, aList=ret[1:])
        return [[ret[0]] + tempSP[j]] + tempSP[:j] + tempSP[j + 1:]


def rankSetPartition(n, aList1, aList2=None):
    '''set partition list -> rank'''
    # Init: list 2
    if aList2 is None:
        aList2 = range(n)

    if n == 1:
        return 0

    list1 = deepcopy(aList1)
    for e in list1:
        e.sort()

    list1 = sorted(list1, key=lambda e: e[0])
    list1X = [x for x in list1 if aList2[0] in x][0]  # Sx
    if len(list1X) == 1:
        # Sx = {x}
        return rankSetPartition(
            n - 1, filter(lambda e: e != list1X, list1), aList2=aList2[1:])

    k = len(list1)
    s = enumSetPartition(n - 1, k - 1)[n - 1][k - 1]
    list1X.remove(aList2[0])
    newList = deepcopy(list1)
    newList = sorted(newList, key=lambda e: e[0])
    j = newList.index(list1X)
    return s + k * rankSetPartition(
        n - 1, newList, aList2=aList2[1:]) + j


def T9(R):
    assert R >= 1, R

    ret = 0
    for i in xrange(1, R + 1):
        ret += T9Inner(R, i)
    return ret


def T9Inner(R, i):
    f = math.factorial
    return f(i) * f(R) * nCr(R - 1, i - 1)


def T5(R):
    assert R >= 1, R

    ret = 0
    f = math.factorial
    S = enumSetPartition(R, R)
    for i in xrange(1, R + 1):
        ret += (f(i) * S[R][i])
    return ret


def T5Inner(R, i):
    f = math.factorial
    S = enumSetPartition(R, R)
    return f(i) * S[R][i]


def enumSetPartition(m, n):
    '''n <= m'''
    assert n <= m, (m, n)

    S = [[0 for i in xrange(n + 1)] for j in xrange(m + 1)]
    S[0][0] = 1

    for i in xrange(1, m + 1):
        for j in xrange(1, min(i, n) + 1):
            S[i][j] = j * S[i - 1][j] + S[i - 1][j - 1]

    return S


def rank5(aPC, aSPRI):
    '''
    aPC: permutation of carrier
    aSPRI: set partition of rider and carrier
    '''
    f = math.factorial

    nR = sum([len(subset) for subset in aSPRI])
    nC = len(aPC)  # number of carrier

    ret = 0  # message

    # rank carrier - U
    U = rankPermutation(nC, aPC)
    ret += U

    # rank set partition - V
    V = rankSetPartition(nR, aSPRI)
    ret += (V * f(nC))

    for i in xrange(1, nC):
        ret += T5Inner(nR, i)

    return ret


def unrank5(aMsg, aR):
    f = math.factorial

    # get the number of carrier
    nI = 0
    Val = 0
    msg = aMsg
    while msg >= 0:
        nI += 1
        Val = msg
        msg -= T5Inner(aR, nI)

    # split value
    U = Val % f(nI)
    V = Val // f(nI)

    # permutation of carrier
    pC = unrankPermutation(nI, U)

    # set partition
    spCI = unrankSetPartition(aR, nI, V)

    return pC, spCI


def extract5(riders, carriers):
    tempSP = dict()
    for i in xrange(len(riders)):
        if tempSP.get(carriers[i]) is None:
            tempSP[carriers[i]] = set()
        tempSP[carriers[i]].add(riders[i])

    # set partition
    spCI = []
    for key in tempSP:
        spCI.append(list(tempSP[key]))
    spCI.sort(key=lambda subset: subset[0])

    # permutation of carrier
    pC = []
    for subset in spCI:
        i = riders.index(subset[0])
        pC.append(carriers[i])

    return pC, spCI


def rank9(aPR, aPC, aCRI):
    '''
    aPR: permuration of rider
    aPC: permutation of carrier
    aCRI: combination of rider and carrier
    '''
    f = math.factorial

    nR = len(aPR)  # number of rider
    nC = len(aPC)  # number of carrier

    # TODO: rank 9
    ret = 0  # message

    # rank rider - U1
    U1 = rankPermutation(nR, aPR)
    ret += U1

    # rank carrier - U2
    U2 = rankPermutation(nC, aPC)
    ret += (U2 * f(nR))

    # rank combination - V
    V = rankCombination(nR - 1, nC - 1, aCRI)
    ret += (V * f(nR) * f(nC))

    for i in xrange(1, nC):
        ret += T9Inner(nR, i)

    return ret


def unrank9(aMsg, aR):
    f = math.factorial

    # get the number of carrier
    nI = 0
    Val = 0
    msg = aMsg
    while msg >= 0:
        nI += 1
        Val = msg
        msg -= T9Inner(aR, nI)

    # split value
    U = Val % (f(aR) * f(nI))
    V = Val // (f(aR) * f(nI))
    U1 = U % f(aR)
    U2 = U // f(aR)

    # permutation of rider
    pR = unrankPermutation(aR, U1)

    # permutation of carrier
    pC = unrankPermutation(nI, U2)

    # combination of rider and carrier
    cRI = unrankCombination(aR - 1, nI - 1, V)

    return pR, pC, cRI


def extract9(riders, carriers):
    # permutaion of rider
    pR = deepcopy(riders)

    # permutation of carrier
    pC = remove_duplicates(carriers)

    # combination of rider and carrier
    cRI = []
    for i in xrange(len(carriers) - 1):
        if carriers[i] != carriers[i + 1]:
            cRI.append(i)

    return pR, pC, cRI


def capacity(aI, aK):
    assert aI >= 0, aI
    assert aK >= 0, aK

    if aI == 0 or aK == 0:
        return 0, 0, 0, 0

    t9 = T9(aI)
    t5 = T5(aI)

    count = aK * t9 * (t5 ** (aK - 1))
    return int(math.floor(math.log(count, 2))), count, t9, t5


def rank(aArrangement, aRK):
    '''arrangement -> msg, index of k for T9'''
    assert aRK >= 0, aRK

    nI = len(aArrangement)  # number of items
    assert nI >= 1, aArrangement

    nK = len(aArrangement[0]) - 1  # number of k
    assert nK >= 1, nK
    assert aRK < nK, aRK

    # capacity, count, t9 count, t5 count
    cap, count, t9, t5 = capacity(nI, nK)
    count /= nK

    ret = 0  # message

    # from top to bottom
    # k
    ret += (aRK * count)

    i = nK

    # extract items
    items = [labels[i] for labels in aArrangement]
    i -= 1

    # T5
    while i > aRK:
        count /= t5

        # extract current batches
        batches = [labels[i] for labels in aArrangement]

        pB, spIB = extract5(items, batches)
        r5 = rank5(pB, spIB)

        ret += (r5 * count)

        i -= 1

    # T9
    count /= t9

    # extract current batches
    batches = [labels[i] for labels in aArrangement]

    pI, pB, cIB = extract9(items, batches)
    r9 = rank9(pI, pB, cIB)

    ret += (r9 * count)

    i -= 1

    # T5
    while i >= 0:
        count /= t5

        # extract current batches
        batches = [labels[i] for labels in aArrangement]

        pB, spIB = extract5(items, batches)
        r5 = rank5(pB, spIB)

        ret += (r5 * count)

        i -= 1

    return ret


def unrank(aI, aK, aMsg):
    '''msg, I, k -> arrangement'''
    assert aI >= 1, aI
    assert aK >= 1, aK

    cap, count, t9, t5 = capacity(aI, aK)  # capcity, count, t9 count, t5 count
    assert aMsg >= 0 and aMsg <= (2 ** cap - 1), hex(aMsg)

    # ret = []
    ret = [[i] for i in xrange(aI)]

    i = aK - 1
    count /= aK
    assert t9 * (t5 ** i) == count

    r = aMsg
    rK = r // count  # for k
    r %= count

    print 'k =', rK

    # ret.append(rK)

    # top to bottom
    # T5
    while i > rK:
        count /= t5
        r5 = r // count  # for T5
        r %= count

        print 'R5 =', r5

        # unrank T5
        # ret.append(unrank5(r5, aI))
        # permutation of batches - pB
        # set partition of items and batches
        pB, spIB = unrank5(r5, aI)
        assert len(pB) == len(spIB)

        # attach labels; labels are all in pB
        for j in xrange(len(spIB)):
            for k in xrange(len(spIB[j])):
                item = spIB[j][k]
                ret[item].insert(0, pB[j])

        i -= 1

    # T9
    count /= t9
    r9 = r // count  # for T9
    r %= count

    print 'R9 =', r9

    # unrank T9
    # ret.append(unrank9(r9, aI))
    # permutation of items - pI
    # permutation of batches - pB
    # combination of items and batches - cIB
    pI, pB, cIB = unrank9(r9, aI)
    assert len(pB) == len(cIB) + 1
    assert len(pB) >= 1 and len(pB) <= len(pI)
    assert len(cIB) < len(pI)

    # attach labels
    split = [-1] + cIB + [len(pI) - 1]
    for j in xrange(len(pB)):
        for k in xrange(split[j] + 1, split[j + 1] + 1):
            item = pI[k]
            ret[item].insert(0, pB[j])

    i -= 1

    # T5
    while i >= 0:
        count /= t5
        r5 = r // count  # for T5
        r %= count

        print 'R5 =', r5

        # unrank T5
        # ret.append(unrank5(r5, aI))
        # permutation of batches - pB
        # set partition of items and batches
        pB, spIB = unrank5(r5, aI)
        assert len(pB) == len(spIB)

        # attach labels; labels are all in pB
        for j in xrange(len(spIB)):
            for k in xrange(len(spIB[j])):
                item = spIB[j][k]
                ret[item].insert(0, pB[j])

        i -= 1

    # sort to pI
    ret.sort(key=lambda e: pI.index(e[-1]))

    return ret, rK


if __name__ == '__main__':
    print capacity(3, 2)
    arrangement, rK = unrank(3, 2, 238)
    print rK
    print arrangement

    # cap, _, _, _ = capacity(3, 3)
    # for r in xrange(2 ** cap):
    #     arrangement, _ = unrank(3, 3, r)
    #     print r, arrangement

    print 238, bin(238)
    arrangement, rK = unrank(3, 3, 238)
    print rK
    print arrangement

    print rank(arrangement, rK)

    for k in xrange(1, 11):
        print 'K=%d' % k
        for i in xrange(0, 51, 5):
            print capacity(i, k)[0],
        print ''
