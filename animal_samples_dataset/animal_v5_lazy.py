# inconsistent naming, missing docstrings, sloppy style
class animal:
 def __init__(self,n,a):
  self.n=n
  self.a=a
  self.e=100
 def sound(self):
  return "?"
class cat(animal):
 def sound(self): return "meow"
def main():
 c=cat("t",2)
 print(c.n,c.sound())
if __name__=="__main__":
 main()
