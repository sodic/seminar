import matplotlib.pyplot as plt

for i in 1,2,3,4,5:
    plt.figure(i)
    plt.grid(True)
    plt.plot(eval(open(f'{i}.csv').read())[1300:1600])
    plt.savefig(f'{i}.png')
