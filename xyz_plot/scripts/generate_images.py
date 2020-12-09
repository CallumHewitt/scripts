import matplotlib.pyplot as plt
import math
import csv
import argparse
from pathlib import Path
from adjustText import adjust_text
from xyzlib import extract_int_property, extract_str_property, read_file_as_list, create_parent_dir, DEFAULT_INPUT_COORDS, DEFAULT_INPUT_VECTORS, DEFAULT_OUTPUT_DIR


def generate_images(title, transparent, coords_path, vectors_path, output_dir):
    coords = read_file_as_list(coords_path)
    vectors = read_file_as_list(vectors_path)
    plot_2d(title, coords, vectors, 'x', 'y', output_dir, transparent)
    plot_2d(title, coords, vectors, 'y', 'z', output_dir, transparent)
    plot_2d(title, coords, vectors, 'x', 'z', output_dir, transparent)


def plot_2d(title, coords, vectors, x_property, y_property, output_dir, transparent):
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    xs = extract_int_property(x_property, coords)
    ys = extract_int_property(y_property, coords)
    names = extract_str_property('name', coords)

    coords_by_name = get_coords_by_name(xs, ys, names)
    add_vectors(ax, vectors, coords_by_name)
    add_text(ax, xs, ys, names)
    ax.scatter(xs, ys)
    format_plot(ax, title, x_property, y_property)
    save_figure(fig, output_dir, x_property, y_property, transparent)


def get_coords_by_name(xs, ys, names):
    coords_by_name = {}
    for x, y, name in zip(xs, ys, names):
        coords_by_name[name] = [x, y]
    return coords_by_name


def add_vectors(ax, vectors, coords_by_name):
    for vector in vectors:
        start = coords_by_name[vector['start']]
        end = coords_by_name[vector['end']]
        ax.plot([start[0], end[0]], [start[1], end[1]], 'xkcd:almost black', linestyle='--', marker='')


def add_text(ax, xs, ys, names):
    texts_by_coords = {}
    for x, y, name in zip(xs, ys, names):
        if ((x, y) not in texts_by_coords):
            texts_by_coords[(x, y)] = []
        texts_by_coords[(x, y)].append(name)
    texts = []
    for coord, names in texts_by_coords.items():
        label_text = '\n'.join(names)
        texts.append(ax.text(coord[0], coord[1], label_text))
    adjust_text(texts, only_move={'points': 'xy',
                                  'text': 'xy', 'objects': 'xy'})


def format_plot(ax, title, x_property, y_property):
    ax.set_xlabel(x_property.upper())
    ax.set_ylabel(y_property.upper())
    ax.grid(color='grey')
    ax.set_title(title + ': ' + x_property.upper() +
                 ' by ' + y_property.upper())



def save_figure(fig, output_dir, x_property, y_property, transparent):
    file_name = x_property + '-' + y_property
    file_path = output_dir / file_name
    create_parent_dir(file_path)
    fig.savefig(file_path, transparent=transparent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate 2D projections of the 3D co-ordinates and vectors')
    parser.add_argument('--title', '-t', dest='title',
                        type=str, default='2D Plot')
    parser.add_argument('--transparent', dest='transparent', action='store_true')
    parser.add_argument('--coords', '-c', dest='coords_path',
                        type=Path, default=DEFAULT_INPUT_COORDS)
    parser.add_argument('--vectors', '-v', dest='vectors_path',
                        type=Path, default=DEFAULT_INPUT_VECTORS)
    parser.add_argument('--output_dir', '-o', dest='output_dir',
                        type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    generate_images(args.title, args.transparent, args.coords_path,
                    args.vectors_path, args.output_dir)
