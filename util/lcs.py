import sys

def lcs_for_zh(s1, s2, max_length = 10):
    len1, len2 = len(s1), len(s2)
    ir, jr = 0, 0
    for i1 in range(len1):
        i2 = s2.find(s1[i1])
        while i2 >= 0:
            j1, j2 = i1+1, i2+1
            while j1 < len1 and j2 < len2 and s2[j2] == s1[j1]:
                if j1-i1 > jr-ir:
                    ir, jr = i1, j1
                    if jr - ir + 1 == max_length:
                        return (s1[ir:jr+1])
                j1 += 1; j2 += 1
            i2 = s2.find(s1[i1], i2+1)

    lcs = s1[ir:jr+1]
    if len(lcs) <=2:
        return None
    return lcs
    
def _l_find(l, s, s_i=0):
    for i in range(s_i, len(l)):
        if l[i] == s:
            return i
    return -1

def lcs_for_en(s1, s2, max_length = 10):
    l1 = s1.split(' ')
    l2 = s2.split(' ')
    len1, len2 = len(l1), len(l2)
    ir, jr = 0, 0
    for i1 in range(len1):
        i2 = _l_find(l2, l1[i1])
        while i2 >= 0 and i2 is not None:
            j1, j2 = i1+1, i2+1
            while j1 < len1 and j2 < len2 and l2[j2] == l1[j1]:
                if j1-i1 > jr-ir:
                    ir, jr = i1, j1
                    if jr - ir + 1 == max_length:
                        lcs = ' '.join(l1[ir:jr+1])
                        if len(lcs) <=2:
                            return None
                        return lcs
                j1 += 1; j2 += 1
            i2 = _l_find(l2, l1[i1], s_i=i2+1)

    lcs = ' '.join(l1[ir:jr+1])
    if len(lcs) <=2:
        return None
    return lcs