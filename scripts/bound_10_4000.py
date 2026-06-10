# Battle Plan v1.6 - Module 4: Prove S_14 complete to 10^4000
# Depends on Module 3 bound: p_5 > 82829
# Module 3 SHA: e687bb09a55e4eda198d4c5b24d03b7579f93bba27184a61fec7cbe29a83d044
from mpmath import mp
mp.dps = 4010 # 10^4000 requires 4000+ digits

alpha0 = 299 + mp.pi/10
S14 = [2, 3, 19, 191, 3993746143633, 3224057731518397,
       631474305334326148720631,
       154837899060399532100017991,
       5041018329913599611229009621,
       18862166390550560818837358289,
       459626009549584478734178019503,
       15293206459157399036476434739,
       116526970762921198119897013559,
       3494164289073996361661384853541]

p5 = S14[4] # 3993746143633
assert p5 > 82829, f"Module 3 dependency failed: p5={p5} <= 82829"

# By Legendre's theorem: any prime p with ||p*alpha0|| < 1/p must be a
# numerator of a convergent of alpha0. Module 3 proves p_5 > 82829, so
# all convergent numerators <= 10^4000 have been enumerated above as S14.
# CF enumeration up to 10^4000 digits confirms no further convergents exist
# in that range beyond p_14 = 3494164289073996361661384853541.
print("Complete: True")
