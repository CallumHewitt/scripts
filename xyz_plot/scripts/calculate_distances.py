import csv
import math
import argparse
from pathlib import Path
from xyzlib import read_file_as_list, create_parent_dir, DEFAULT_INPUT_COORDS, DEFAULT_INPUT_VECTORS, DEFAULT_OUTPUT_DIR


def calculate_distances(coords_path, vectors_path, output_dir):
    coords = read_file_as_list(coords_path)
    vectors = read_file_as_list(vectors_path)

    coords_by_name = get_coords_by_names(coords)

    distances_by_title = {}
    for vector in vectors:
        start = coords_by_name[vector['start']]
        end = coords_by_name[vector['end']]
        title = vector['start'] + ' -> ' + vector['end']
        distances_by_title[title] = calculate_distance(start, end)

    write_dictionary_to_csv(output_dir / 'distances.csv', distances_by_title)


def get_coords_by_names(coords):
    coords_by_name = {}
    for coords in coords:
        coords_by_name[coords['name']] = [
            int(coords['x']), int(coords['y']), int(coords['z'])
        ]
    return coords_by_name


def calculate_distance(start, end):
    return round(math.sqrt(
        (pow(start[0] - end[0], 2)) +
        (pow(start[1] - end[1], 2)) +
        (pow(start[2] - end[2], 2))
    ), 2)


def write_dictionary_to_csv(file_name, dict):
    create_parent_dir(file_name)
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        for key, value in dict.items():
            writer.writerow([key, value])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a .csv file containing the distances of the vectors in the input')
    parser.add_argument('--coords', '-c', dest='coords_path',
                        type=Path, default=DEFAULT_INPUT_COORDS)
    parser.add_argument('--vectors', '-v', dest='vectors_path',
                        type=Path, default=DEFAULT_INPUT_VECTORS)
    parser.add_argument('--output_dir', '-o', dest='output_dir',
                        type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    calculate_distances(args.coords_path, args.vectors_path, args.output_dir)
