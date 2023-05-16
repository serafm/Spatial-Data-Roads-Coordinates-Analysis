import csv

# Open the CSV file
with open('data/tiger_roads.csv', mode='r') as file:
    # Create a reader object
    roads = csv.reader(file)

    # Skip first line
    next(roads)

    # list of points of road
    points = []
    # list of roads
    records = []
    ID = 1

    # read linestrings
    for row in roads:
        for coordinates in row:
            # split every x,y coordinates and convert to float
            x = float(coordinates.split(" ")[0])
            y = float(coordinates.split(" ")[1])
            # add x,y in the points lists
            points.append([x, y])

        # find MBR of linestring
        min_mbr_x = min(x[0] for x in points)
        max_mbr_x = max(x[0] for x in points)
        min_mbr_y = min(y[1] for y in points)
        max_mbr_y = max(y[1] for y in points)
        mbr = [(min_mbr_x, min_mbr_y), (max_mbr_x, max_mbr_y)]

        # add linestring to records list
        records.append([ID, mbr, points])

        # empty points list
        points = []
        ID += 1

    # Max MBR of all linestrings in file
    min_x = min(mbr[1][0][0] for mbr in records)
    max_x = max(mbr[1][1][0] for mbr in records)
    min_y = min(mbr[1][0][1] for mbr in records)
    max_y = max(mbr[1][1][1] for mbr in records)

    # Create a grid of cells with equal range of values
    grid = dict()
    for x in range(10):
        for y in range(10):
            grid[(x, y)] = [(min_x + x * (max_x - min_x) / 10, min_y + y * (max_y - min_y) / 10),
                            (min_x + (x + 1) * (max_x - min_x) / 10, min_y + (y + 1) * (max_y - min_y) / 10)]

    # Create grid.dir file to add max min MBR of all linestrings and cells with their number of IDs
    grid_dir = open("data/grid.dir", "a")
    # Write in file first line the MBR values
    grid_dir.write(str(min_x) + " " + str(max_x) + " " + str(min_y) + " " + str(max_y) + "\n")

    # Create a grid.grd file to add linstrings with theri MBR and coordinate values
    grid_grd = open("data/grid.grd", "a")

    # check MBRs
    for cell in grid:
        # Add a list at every key of the cell's dictionary
        grid[cell].append([])
        # For every road in records and get min max MBR, get cell's coordinates
        for road in records:
            xmin, ymin = road[1][0]
            xmax, ymax = road[1][1]
            xmin_cell, ymin_cell = grid[cell][0]
            xmax_cell, ymax_cell = grid[cell][1]

            # Check if road is in cell
            if xmin >= xmin_cell and xmax <= xmax_cell and ymin >= ymin_cell and ymax <= ymax_cell:
                # Add road's ID in cell
                grid[cell][2].append(road[0])

                # Get the MBR of road
                min_x_mbr, min_y_mbr = str(road[1][0][0]), str(road[1][0][1])
                max_x_mbr, max_y_mbr = str(road[1][1][0]), str(road[1][1][1])

                # Convert the array of coordinates of road to a string
                coordinates = ', '.join(str(sublist).replace(',', '') for sublist in road[2])

                # Remove the [ ] characters from the string
                coordinates = coordinates.replace('[', '').replace(']', '')

                # Write in grid.grd file the ID,MBR,coordinates of file
                grid_grd.write(
                    str(road[0]) + ", " + str(min_x_mbr) + " " + str(min_y_mbr) + ", " + str(max_x_mbr) + " " + str(
                        max_y_mbr) + ", " + str(coordinates) + "\n")

            xmin_new = max(xmin, xmin_cell)
            ymin_new = max(ymin, ymin_cell)
            xmax_new = min(xmax, xmax_cell)
            ymax_new = min(ymax, ymax_cell)

            if xmax_new >= xmin_new and ymax_new >= ymin_new:
                grid[cell][2].append(road[0])
                min_x_mbr, min_y_mbr = str(road[1][0][0]), str(road[1][0][1])
                max_x_mbr, max_y_mbr = str(road[1][1][0]), str(road[1][1][1])
                # Convert the array to a string
                coordinates = ', '.join(str(sublist).replace(',', '') for sublist in road[2])
                # Remove the [ ] characters from the string
                coordinates = coordinates.replace('[', '').replace(']', '')
                grid_grd.write(
                    str(road[0]) + ", " + str(min_x_mbr) + " " + str(min_y_mbr) + ", " + str(max_x_mbr) + " " + str(
                        max_y_mbr) + ", " + str(coordinates) + "\n")

        # Write in grid.dir file the cell coordinates and number of ID's that are in that cell
        grid_dir.write(str(cell[0]) + " " + str(cell[1]) + " " + str(len(grid[cell][2])) + "\n")

    grid_dir.close()
    grid_grd.close()
