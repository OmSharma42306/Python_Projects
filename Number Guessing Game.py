import random
lower=int(input("Enter Starting value : "))
higher=int(input("Enter End Value :"))
x=random.randint(lower,higher)
print(f"{x}")
guesses=0
while guesses<=10:
    a=int(input("Enter Your Guess"))
    if a==x:
        print("Congradulations ! You Guessed it right")     
    elif a<=x:
        print("You Guessed it Very Small")
    elif a>=x:
        print("You Guessed It Very High")
    guesses=guesses+1

if guesses>10:
    print("Better Luck Next Time !")
