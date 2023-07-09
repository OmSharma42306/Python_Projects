import random

def game(comp,user):
    if comp==user:
        return None
    elif comp=='s':
        if user=='w':
            return False
        elif user=='g':
            return True


    elif comp=='w':
        if user=='g':
            return False
        elif user=='s':
            return True

    elif comp=='g':
        if user=='s':
            return False
        elif user=='w':
            return True

print("comp turn: Snake(s),Water(w) or Gun(g) ")
rno=random.randint(1,3)
if rno==1:
    comp='s'
elif rno==2:
    comp='w'
elif rno==3:
    comp='g'


user=input("Your's Turn: Snake(s),water(w),gun(g): ")
a=game(comp,user)
print(f"Computer Turn is :{comp} ")
print(f"Your Turn is :{user} ")
if a==None:
    print("Game is A Tie!")
elif a==True:
    print("You Win !")
elif a==False:
    print("You Lose !")