from matplotlib import pyplot as plt


def rysowanie(x, y, title, xlabel, ylabel):
    plt.plot(x,y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()
