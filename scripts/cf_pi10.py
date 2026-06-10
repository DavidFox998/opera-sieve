# Battle Plan v1.6 - Module 3: CF of pi/10
# Library: mpmath 1.3.0 (pinned for Modules 1-3)
# Seed fix: p=1,pp=0 tracks numerators; q=0,qq=1 tracks denominators
from mpmath import mp
mp.dps = 50 # 50 decimal places sufficient; 500 used by agent for audit

x = mp.pi/10
a = []
for _ in range(8): # compute a0..a7
    ai = int(x)
    a.append(ai)
    x = x - ai
    if x == 0: break
    x = 1/x

# a = [0, 3, 5, 2, 5, 1, 733, 11]
p, q = 1, 0
pp, qq = 0, 1
for i, ai in enumerate(a):
    p, pp = ai*p + pp, p
    q, qq = ai*q + qq, q
    if i == 5: # n=5
        p5, q5 = p, q # 71, 226

a6 = a[6] # 733
a7 = a[7] # 11
bound = a6 * q5 // 2 # 82829

print(f"CF: {a}")
print(f"p_5={p5}, Q_5={q5}, a_6={a6}, a_7={a7}, bound={bound}")
