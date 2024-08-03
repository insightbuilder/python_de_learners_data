import turtle
import random

po = turtle.Turtle(shape="turtle")
po.color("green")
po.penup()
po.goto(-200, 100)
pt = po.clone()
pt.color("blue")
pt.penup()
pt.goto(-200, -100)

po.goto(300, 60)
po.pendown()
po.circle(40)
po.penup()
po.goto(-200, 100)

pt.goto(300, -140)
pt.pendown()
pt.circle(40)
pt.penup()
pt.goto(-200, -100)

die = [1, 2, 3, 4, 5, 6]

for i in range(20):
    if po.pos() >= (300, 100):
        print("player one wins!")
    elif pt.pos() >= (300, -100):
        print("player two wins")
        break

    else:
        pot = input("Press Enter to roll the die")
        die_ot = random.choice(die)

        po.fd(20 * die_ot)

        ptt = input("Press enter to roll die")
        die_ot = random.choice(die)

        pt.fd(20 * die_ot)
