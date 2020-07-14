import random
import itertools
cand = [10,20,30,40,50]
for i in range(1000):
    A = random.randint(0, 4)

    with open("step.txt", "a") as myfile:
        myfile.write(str(cand[A])+'\n')

# results = list(itertools.permutations([0,1,2,3], 4))

# #results = list(itertools.combinations_with_replacement([0,1,2,3], 4))

# print(results)