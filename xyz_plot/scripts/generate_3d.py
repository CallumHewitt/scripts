import matplotlib.pyplot as plt
from matplotlib import animation;
import math
import argparse
from pathlib import Path
from adjustText import adjust_text
from xyzlib import extract_int_property, extract_str_property, read_file_as_list, DEFAULT_INPUT_COORDS, DEFAULT_INPUT_VECTORS, DEFAULT_OUTPUT_DIR


def generate_3d(title, coords_path, vectors_path, output_dir, interactive):
    coords = read_file_as_list(coords_path)
    vectors = read_file_as_list(vectors_path)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    xs = extract_int_property('x', coords)
    ys = extract_int_property('y', coords)
    zs = extract_int_property('z', coords)
    names = extract_str_property('name', coords)

    coords_by_name = get_coords_by_name(xs, ys, zs, names)
    add_vectors(ax, vectors, coords_by_name)
    add_text(ax, coords)
    ax.scatter(xs, ys, zs, marker='o')
    format_plot(ax, title)

    if (interactive):
        plt.show()
    else:
        save(fig, ax, output_dir)


def get_coords_by_name(xs, ys, zs, names):
    coords_by_name = {}
    for x, y, z, name in zip(xs, ys, zs, names):
        coords_by_name[name] = [x, y, z]
    return coords_by_name


def add_vectors(ax, vectors, coords_by_name):
    for vector in vectors:
        start = coords_by_name[vector['start']]
        end = coords_by_name[vector['end']]
        ax.plot([start[0], end[0]], [start[1], end[1]], [
                start[2], end[2]], 'black', linestyle='--', marker='')


def add_text(ax, coords):
    texts = []
    for entry in coords:
        texts.append(ax.text(
            int(entry['x']),
            int(entry['y']),
            int(entry['z']),
            entry['name']
        ))
    adjust_text(texts)


def format_plot(ax, title):
    ax.set_xlabel('X', color='black')
    ax.set_ylabel('Y', color='black')
    ax.set_zlabel('Z', color='black')
    ax.set_title(title)

def save(fig, ax, output_dir):
    def init():
        return fig,

    def animate(i):
        ax.view_init(elev=15., azim=i/2)
        return fig,

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=720, interval=20, blit=True)
    anim.save(output_dir / '3d_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates a 3D plot of the data provided and exports it as an mp4 animation.')
    parser.add_argument('--title', '-t', dest='title', type=str, default='3D Plot')
    parser.add_argument('--coords', '-c', dest='coords_path',
                        type=Path, default=DEFAULT_INPUT_COORDS)
    parser.add_argument('--vectors', '-v', dest='vectors_path',
                        type=Path, default=DEFAULT_INPUT_VECTORS)
    parser.add_argument('--output_dir', '-o', dest='output_dir',
                        type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument('--interactive', '-i', dest='interactive', action='store_true')
    args = parser.parse_args()
    generate_3d(args.title, args.coords_path, args.vectors_path, args.output_dir, args.interactive)
