# Minified, single-line-ish, poor readability
class A: 
 def __init__(s,n,a):s.n=n;s.a=a;s.e=100
 def m(s):return"?"
class C(A):def m(s):return"m"
if __name__=="__main__":print(C("x",1).m())
