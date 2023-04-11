from inspect import getsourcelines
from scipy.integrate import dblquad
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d


def FuncToStr(f):
    line = getsourcelines(f)[0][0]
    return line[line.find(': ')+2:-2].strip().replace("np.", "")


def plotBounds(g, f, a, b, title, padX=5, res=100):
    # plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.spines["bottom"].set_position("zero")
    ax.spines["left"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlabel("$x$", size=12, labelpad=-24, x=1.02)
    ax.set_ylabel("$y$", size=12, labelpad=-21, y=1.02, rotation=0)
    ax.grid(which="both", color="grey", linewidth=1, linestyle="-", alpha=0.2)

    plt.title(title, loc="left")
    x = np.linspace(a - padX, b + padX, res)
    # plt.figure("Function sketches")

    try:
        plt.plot(x, f(x), color="m", label=f"y={FuncToStr(f)}")
    except:
        plt.axhline(y=f(x), color="m", label=f"y={FuncToStr(f)}")

    try:
        plt.plot(x, g(x), color="y", label=f"y={FuncToStr(g)}")
    except:
        plt.axhline(y=g(x), color="y", label=f"y={FuncToStr(g)}")

    plt.axvline(x=a, color="r", ls="--", lw=1.5, label=f"Xs -> {a:.2f}")
    plt.axvline(x=b, color="b", ls="--", lw=1.5, label=f"Xe -> {b:.2f}")
    plt.fill_between(x, f(x), g(x),
                     where=[a <= x <= b for x in x],
                     color="k",
                     alpha=0.2,
                     label="Area")
    plt.legend(loc="best")
    plt.show()


def plotBounds3d(g, f, a, b, title, padX=5, res=100):
    x = np.linspace(a, b, 100)
    y = np.linspace(g(a), f(b), 100)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)

    ax.contour3D(X, Y, Z, 50, cmap='binary')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.title(title, loc="left")
    x = np.linspace(a - padX, b + padX, res)

    # Plot f(x) and g(x) on the surface plot
    try:
        ax.plot(x, f(x), color="m", label=f"y={FuncToStr(f)}")
    except:
        x_line = np.linspace(a, b, 100)
        y_line = np.full_like(x_line, f(x_line))
        ax.plot(x_line, y_line, 0, color="m", label=f"y={FuncToStr(f)}")

    try:
        ax.plot(x, g(x), color="y", label=f"y={FuncToStr(g)}")
    except:
        x_line = np.linspace(a, b, 100)
        y_line = np.full_like(x_line, g(x_line))
        ax.plot(x_line, y_line, 0, color="g", label=f"y={FuncToStr(g)}")

    # Fill the area between f(x) and g(x)
    x_fill = np.linspace(a, b, res)
    y_fill_f = f(x_fill)
    y_fill_g = g(x_fill)
    X, Y = np.meshgrid(x_fill, np.array([0, 1], dtype=object))
    Z = np.vstack((y_fill_f, np.repeat(y_fill_g, res))).T

    ax.plot_surface(X, Y, Z,
                    color="k",
                    alpha=0.2,
                    label="Area")

    # Convert y_fill_f and y_fill_g to 2D arrays for plotting
    y_fill_f = np.array([y_fill_f, y_fill_f], dtype=object)
    y_fill_g = np.array([y_fill_g, y_fill_g], dtype=object)

    # Plot lines connecting f(x) and g(x)
    ax.plot(x_fill, y_fill_f[0], 0, color="k", alpha=0.5, label="Fill")
    ax.plot(x_fill, y_fill_g[0], 0, color="k", alpha=0.5)

    y_line = np.linspace(-10, 10, 100)
    x_line = np.full_like(y_line, a)
    ax.plot(x_line, y_line, 0, color="r", ls="--",
            lw=1.5, label=f"Xs -> {a:.2f}")

    y_line = np.linspace(-10, 10, 100)
    x_line = np.full_like(y_line, b)
    ax.plot(x_line, y_line, 0, color="b", ls="--",
            lw=1.5, label=f"Xe -> {b:.2f}")

    ax.legend(loc="best")
    plt.show()


if __name__ == "__main__":
    # def f(y, x): return (x-1)/(6-x)
    # xBound = (1, 6)
    # yBound = (lambda x: 1,
    #           lambda x: -x+7)
    # def f(y, x): return 1
    # xBound = (0, np.pi/2)
    # yBound = (lambda x: np.sin(x),
    #           lambda x: 3*np.sin(x))
    # def f(y, x): return np.arctan(np.tan(x))*y
    # xBound = (0, np.pi)
    # yBound = (1, 3)
    # def f(y, x): return (x/y)**2
    # xBound = (1, 2)
    # yBound = (lambda x: 1/x, lambda x: x)
    # def f(y, x): return x**2 - y**2
    # xBound = (0, 1)
    # yBound = (lambda x: x**2,
    #           lambda x: np.sqrt(x))
    def func(y, x): return np.e**(x+y)
    xBound = (0, 1)
    yBound = (lambda x: 0,
              lambda x: x)

    area, err = dblquad(func, *xBound, *yBound)
    plotBounds(*yBound, *xBound, f"Area: {area:.2f}\nError: ±{err:.2f}")
