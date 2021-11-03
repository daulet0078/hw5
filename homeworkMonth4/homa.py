

guess =1
#1 100
left =0
right = 101
coun = 0
while True:
    answer = (left+right)//2
    coun +=1
    print(answer)
    if answer == guess:
        print("угадал")
        break
    elif answer < guess:
        print("число больше")
        left = answer
    elif answer > guess:
        print("число меньше")
        right = answer

print (coun)