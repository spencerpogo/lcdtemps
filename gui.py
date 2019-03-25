from guizero import App, Text, PushButton
import random
list_a = []
list_b = []
list_c = []

with open("/home/pi/python/shakespeare/insults.csv", "r") as f:
    for line in f:
        words = line.split(",")
        list_a.append(words[0])
        list_b.append(words[1])
        list_c.append(words[2].strip())
def insult():
    a = random.choice(list_a)
    b = random.choice(list_b)
    c = random.choice(list_c)
    insult = "Thou a " + a + " " + b + " " + c + "! \nGood Day! "
    return insult

app = App(title="LCD Temperature", layout="auto", bg="white", width="750")
mtext = Text(app, text="", size=20, color="black")
def new_insult():
    ins = insult()
    mtext.value = ins
btext = "Insult me again"
button = PushButton(app, command=new_insult, text=btext)
app.display()
