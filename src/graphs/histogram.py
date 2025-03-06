import numpy as np

from graphs.core import plt, apply_theme


def render(file_name: str, theme: dict, values: list):
    ax = plt.subplots()[1]
    counts, groups = np.histogram(values, bins="auto")

    color = theme["line"]

    if color in plt.colormaps():
        apply_cmap(ax, theme, counts, groups)
    else:
        ax.bar(groups[:-1], counts, width=np.diff(groups), align="edge", color=color)

    apply_theme(ax, theme)

    plt.savefig(file_name)
    plt.close()


def apply_cmap(ax, theme, counts, groups):
    """Applies a colormap to a histogram.

    Args:
        ax (Axes): The Matplotlib Axes object.
        theme (dict): A dictionary containing theme colors.
        counts (array-like): Histogram bin counts.
        groups (array-like): Histogram bin edges.
    """
    cmap = plt.get_cmap(theme["line"])

    mask = np.zeros((len(groups), 2))
    mask[:, 0] = np.concatenate([groups[:-1], [groups[-1]]])
    mask[:-1, 1] = counts

    ax.bar(groups[:-1], counts, width=np.diff(groups), align="edge", alpha=0)
    original_ylim = ax.get_ylim()

    extent = [ax.get_xlim()[0], ax.get_xlim()[1], 0, max(counts)]

    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x, y)

    ax.imshow(Y, cmap=cmap, extent=extent, origin="lower", aspect="auto")
    ax.set_ylim(original_ylim)

    graph_background = theme["graph_background"]
    ax.fill_between(mask[:, 0], mask[:, 1], extent[3], color=graph_background, step="post")
    ax.fill_between([extent[0], groups[0]], [0, 0], [extent[3], extent[3]], color=graph_background)
    ax.fill_between([groups[-1], extent[1]], [0, 0], [extent[3], extent[3]], color=graph_background)
