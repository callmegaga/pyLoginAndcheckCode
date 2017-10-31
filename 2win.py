import fileinput
file = open("result_win.txt","a")

for line in fileinput.input("result.txt"):
    line = line + "\r\n\r\n"
    file.write(line)   
