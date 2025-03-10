from graphs.core import plt, apply_theme


def render(theme: dict):
    x = [i for i in range(100)]

    ax = plt.subplots()[1]
    ax.plot(x, x, label="Data")
    plt.grid()

    ax.set_title("Sample Graph")
    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")

    apply_theme(ax, theme)

    plt.savefig("sample_graph.png")

    plt.close()