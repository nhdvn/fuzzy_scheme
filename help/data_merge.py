import os

dir = "data/ebd"
result = "data/The"
resultFile = open(result, "w")

id = 0
for root, subdirectories, files in os.walk(dir):
    if (dir == root):
        continue
    id += 1
    for file in files:
        with open(os.path.join(root, file), "r") as f:
            for val in f:
                resultFile.write(str(val)[:-1] + ',')
        resultFile.write(str(id) + "\n")

resultFile.close()
