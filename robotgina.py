

import random

file = open("robotgina.txt", "w")
camino = []
for a in range(1,174):
	camino.append((a + random.randint(0,5),a + random.randint(0,5)))

for c in camino:
	file.write(str(c[0] *0.2) + ' ' + str(c[1]*0.2) + '\n')



#file.write("1 1\n")

#file.write("2 2\n")

file.close()