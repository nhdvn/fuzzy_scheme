import os

dir = "Inter/"
result = "inter.txt"
resultFile = open(result, "w")

for root, subdirectories, files in os.walk(dir):
    for file in files:
        with open(os.path.join(root, file), "r") as f:
            Lines = f.readlines()

            if (len(Lines) != 117):
                print(file)

            for line in Lines:
                words = line.split(" ")
                if (words[1].strip() == "True"):
                    y = words[0].strip()
                    if (y[-1] == ':'):
                        y = y[:-1]

                    resultFile.write(file + " " + y + "\n")

resultFile.close()
