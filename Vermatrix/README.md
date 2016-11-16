# vermatrix (crypto 100)
hangout.py is the code of server.  
After looks through the code of server, we find that it encrypt by  
``` python
def fixmatrix(matrixa, matrixb):
    out = [[0 for x in xrange(3)] for x in xrange(3)]    
    for rn in xrange(3):
        for cn in xrange(3):
            out[cn][rn] = (int(matrixa[rn][cn])|int(matrixb[cn][rn]))&~(int(matrixa[rn][cn])&int(matrixb[cn][rn]))
    return out
```
(a|b)&~(a&b) is actually a^b
So we only needs to XOR the string back by its permutation. The seed is arranged to 3*3 matrixes, and transpose every iteration. After some try and error we figure out the solution (solve.py).
