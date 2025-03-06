import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.legend_handler import HandlerLine2D, HandlerLineCollection


class LineHandler(HandlerLine2D):
    """Custom legend handler for Line2D objects."""

    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        """Creates a simple horizontal line as a legend representation."""
        line = plt.Line2D([0, 21], [3.5, 3.5], color=orig_handle.get_color())
        return [line]


class CollectionHandler(HandlerLineCollection):
    """Custom legend handler for LineCollection objects."""

    def create_artists(self, legend, artist, xdescent, ydescent, width, height, fontsize, trans):
        """Creates a collection of lines to represent gradients in legends."""
        x = np.linspace(0, width, self.get_numpoints(legend) + 1)
        y = np.zeros(self.get_numpoints(legend) + 1) + height / 2. - ydescent
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap=artist.cmap, transform=trans)
        lc.set_array(x)
        return [lc]


def get_line_cmap(ax, line_index, cmap_name):
    """Replaces a line in the given Axes with a gradient LineCollection.

    Args:
        ax (Axes): The Matplotlib Axes object.
        line_index (int): The index of the line to replace.
        cmap_name (str): The name of the colormap to apply.

    Returns:
        LineCollection: The LineCollection created using the given colormap.
    """
    cmap = plt.get_cmap(cmap_name)

    line = ax.get_lines()[line_index]
    x, y = line.get_data()
    ax.lines[line_index].remove()

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, zorder=50, linewidth=1)
    lc.set_array(x)
    ax.add_collection(lc)

    return lc


def apply_theme(ax: Axes, theme: dict, themed_line_index: int = 0):
    """Applies a custom theme to a Matplotlib Axes object.

    Args:
        ax (Axes): The Matplotlib Axes object to style.
        theme (dict): A dictionary containing theme colors.
        themed_line_index (int, optional): The index of the line to apply a colormap to. Defaults to 0.
    """
    # Backgrounds
    ax.figure.set_facecolor(theme["background"])
    ax.set_facecolor(theme["graph_background"])

    # Text
    ax.title.set_color(theme["text"])
    ax.xaxis.label.set_color(theme["text"])
    ax.yaxis.label.set_color(theme["text"])

    # Axis
    ax.tick_params(axis="both", which="both", colors=theme["axis"], labelcolor=theme["text"])
    for axis in ax.spines.values():
        axis.set_color(theme["axis"])

    # Grid
    if theme["grid"] is None:
        ax.grid(False)
    else:
        ax.grid(color=theme["grid"])

    # Line
    legend_lines = []
    legend_labels = []
    handler_map = {}
    line_color = theme["line"]

    for i, line in enumerate(ax.get_lines()):
        label = line.get_label()
        if label.startswith("_"):
            label = "\u200B" + label

        # Recoloring
        line_handler = LineHandler()

        if i == themed_line_index:
            if line_color in plt.colormaps():
                line = get_line_cmap(ax, themed_line_index, line_color)
                line_handler = CollectionHandler(numpoints=50)
            else:
                line.set_color(line_color)

        # Appending to legend
        legend_lines.append(line)
        legend_labels.append(label)
        handler_map[line] = line_handler

    # Legend
    if len(legend_lines) > 1:
        legend = ax.legend(legend_lines, legend_labels, handler_map=handler_map, loc="upper left", framealpha=0.5)
        legend.get_frame().set_facecolor(theme["graph_background"])
        legend.get_frame().set_edgecolor(theme["axis"])
        for text in legend.get_texts():
            text.set_color(theme["text"])


def remove_file(file_name: str):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        print("File not found.")
