
# read the grid.dir file
with open('data/grid.dir', mode='r') as file:
    dir_data_collection = dict()

    linestring = file.read().split("\n")

    # remove first and last line
    linestring.pop(0)
    linestring.pop(-1)

    for cell in linestring:
        cell = cell.split()
        dir_data_collection[(int(cell[0]), int(cell[1]))] = int(cell[2])

    print(dir_data_collection)

