# XYZ Plotter

These scripts are used to plot 3D data and calculate the distances between connected points.

## Input files

There are two inputs files:

- ```input/coords.csv``` is a csv file representing the 3D points to be plotted. The file has the following columns:
    - ```name``` The name of the point to plot
    - ```x``` The x co-ordinate
    - ```y``` The y co-ordinate
    - ```z``` The z co-ordinate
- ```input/vectors.csv``` is a csv file representing the connections between 3d points. The file has the following columns:
    - ```start``` The name of the point specified in ```coords.csv``` to start the vector from
    - ```end``` The name of the point specified in ```coords.csv``` to end the vector on

## calculate_distances.py

Outputs a file into ```output/distances.csv``` containing the distances of all the vectors specified in ```input/vectors.csv```.

```shell script
$ python calculate_distances.py -h
usage: calculate_distances.py [-h] [--coords COORDS_PATH] [--vectors VECTORS_PATH] [--output_dir OUTPUT_DIR]

Generate a .csv file containing the distances of the vectors in the input

optional arguments:
  -h, --help            show this help message and exit
  --coords COORDS_PATH, -c COORDS_PATH
  --vectors VECTORS_PATH, -v VECTORS_PATH
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
```

## generate_images.py

Generates 3 2D plots of the x/y, y/z and x/z projections of the input co-ordinates and vectors. These plots are placed into the ```output/``` folder as ```.png``` files. Adding the transparent flag will export the axes without the white background.

You will need to have the [adjustText](https://github.com/Phlya/adjustText) library installed when running this script.

```shell script
$ python generate_images.py -h
usage: generate_images.py [-h] --title TITLE [--coords COORDS_PATH] [--vectors VECTORS_PATH] [--output_dir OUTPUT_DIR]

Generate 2D projections of the 3D co-ordinates and vectors

optional arguments:
  -h, --help            show this help message and exit
  --title TITLE, -t TITLE
  --transparent
  --coords COORDS_PATH, -c COORDS_PATH
  --vectors VECTORS_PATH, -v VECTORS_PATH
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
```

## generate_3d.py

Generates a 3D view of the input co-ordinates and vectors and exports it as an mp4 animation. Toggling the interactive flag allows the plot to be manipulated manually instead of being exported to video.

Please note to run this script you will need to install [ffmpeg](https://ffmpeg.org/) and place it on your path.

```shell script
$ python scripts/generate_3d.py -h
usage: generate_3d.py [-h] [--title TITLE] [--coords COORDS_PATH] [--vectors VECTORS_PATH] [--output_dir OUTPUT_DIR] [--interactive]

Generates a 3D plot of the data provided and exports it as an mp4 animation.

optional arguments:
  -h, --help            show this help message and exit
  --title TITLE, -t TITLE
  --coords COORDS_PATH, -c COORDS_PATH
  --vectors VECTORS_PATH, -v VECTORS_PATH
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
  --interactive, -i
```
