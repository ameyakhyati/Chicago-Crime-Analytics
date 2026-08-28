import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import os
sns.set_theme(style="whitegrid")


def save_graph(filename):   
    os.makedirs("static/graphs", exist_ok = True)
    filepath = os.path.join("static/graphs", filename)

    plt.savefig(filepath, dpi = 300, bbox_inches = "tight")
    plt.close()

    return filepath


def plot_bargraph(data, x_axis, y_axis, graph_title, x_label, y_label, filename, hue = None, palette = "magma", legend = False, grid = True, annotate=None, annotate_format=None,
    annotate_suffix="", orientation="horizontal"):
    plt.figure(figsize = (10,6))
    sns.barplot(data = data, x = x_axis, y = y_axis, hue = hue, palette = palette, legend = legend)

    plt.title(graph_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if grid:
        plt.grid(axis = "x", linestyle = "--", alpha = 0.4)

    plt.xticks(rotation = 45)
    plt.tight_layout()


    if annotate is not None:

        for index, row in data.reset_index(drop=True).iterrows():
            value = row[annotate]
            if annotate_format is not None:
                value = format(value, annotate_format)

            value = f"{value}{annotate_suffix}"
            
            if orientation == "vertical":
                plt.text( index,  row[y_axis], value, va="bottom", ha="center" )

            else:
                plt.text( row[x_axis], index, value, va="center", ha="left" )


    return save_graph(filename)



def plot_piechart(data, labels, values, graph_title, filename, explode = None, shadow = False, colors = None):

    plt.figure(figsize = (8,8))
    plt.pie(data[values], labels = data[labels], autopct = "%1.1f%%", startangle = 90, explode = explode, shadow = shadow, colors = colors )

    plt.title(graph_title)
    plt.tight_layout()

    return save_graph(filename)



def plot_line_graph(data, x_axis, y_axis, graph_title, x_label, y_label, mark, filename, marksize = 5, linewidth = 1, color = "#FE4545"):

    plt.figure(figsize = (10,6))
    sns.lineplot(data = data, x = x_axis, y = y_axis, marker = mark, markersize = marksize, linewidth = linewidth, color = color)

    plt.title(graph_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    return save_graph(filename)



def plot_boxplot(data, column, graph_title,  y_label, filename):

    plt.figure(figsize = (10,6))
    sns.boxplot(data = data , y = column)

    plt.title(graph_title)
    plt.ylabel(y_label)

    plt.tight_layout()

    return save_graph(filename)


def plot_heatmap(data, graph_title, x_label, y_label, filename, annotation = False, annotation_format = "d", color = "Blues"):

    plt.figure(figsize = (12,8))
    sns.heatmap(data, annot = annotation, fmt = annotation_format, cmap = color)

    plt.title(graph_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.tight_layout()

    return save_graph(filename)


