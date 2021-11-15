import random

def estimate_pi(totalpoint):
    point = 0
    pointincircle = 0
    while(point < totalpoint):
        x = random.random()
        y = random.random()
        if ((x-0.5)**2)+((y-0.5)**2) < 0.25:
            pointincircle += 1
        point += 1
    return 4 * (pointincircle/totalpoint)

pi = estimate_pi(300000)
print(pi)
    
