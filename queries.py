# Open grid.dir file for reading
with open('data/grid.dir', 'r') as dir_file:
    # Read the first line and extract MBR values
    mbr_values = dir_file.readline().split()
    min_x_mbr, max_x_mbr, min_y_mbr, max_y_mbr = map(float, mbr_values)

    # Create data structure for cell contents
    cell_contents = []
    grid = dict()
    pos = 0
    cell_ids = dict()

    # Loop over each line in grid.dir file
    for line in dir_file:
        # Extract x, y, and num_ids values
        x_cell, y_cell, num_ids = map(int, line.split())

        # If num_ids is greater than zero, load contents from grid.grd file
        if num_ids > 0:
            cell_ids[(x_cell, y_cell)] = []
            # Open corresponding section of grid.grd file for reading
            with open('data/grid.grd', 'r') as grd_file:
                # seek to the last position in the file
                grd_file.seek(pos)

                for _ in range(num_ids):
                    # Extract ID, MBR, and geometry values
                    id_line = grd_file.readline()
                    id_values = id_line.split(',')
                    id_val = int(id_values[0])
                    mbr_coords = [[float(id_values[1].split(' ')[1]), float(id_values[1].split(' ')[2])], [float(id_values[2].split(' ')[1]), float(id_values[2].split(' ')[2])]]
                    geometry_coords = []
                    for coord in id_values[5:]:
                        x, y = map(float, coord.split())
                        geometry_coords.append([x, y])

                    # Store ID, MBR, and geometry in cell_contents data structure
                    cell_contents.append([id_val, mbr_coords, geometry_coords])
                    cell_ids[(x_cell, y_cell)].append(id_val)

                # store the new file position
                pos = grd_file.tell()

            # add cell content to grid
            grid[(x_cell, y_cell)] = cell_contents
            cell_contents = []

    # read queries from txt file
    with open('data/queries.txt', 'r') as queries:
       for query in queries:
           query = query.split(',')
           # add query to list
           query_number = query[0]
           query_min_x = float(query[1].split()[0])
           query_min_y = float(query[1].split()[1])
           query_max_x = float(query[1].split()[2])
           query_max_y = float(query[1].split()[3])

           # initialize list to hold results
           results = []
           id_count = 0
           num_cells = 0

           for cell in grid:
               for point in grid[cell]:
                   min_x_mbr = float(point[1][0][0])
                   min_y_mbr = float(point[1][0][1])
                   max_x_mbr = float(point[1][1][0])
                   max_y_mbr = float(point[1][1][1])

                   # check if cell overlaps with query window
                   if min_x_mbr <= query_max_x and max_x_mbr >= query_min_x and min_y_mbr <= query_max_y and max_y_mbr >= query_min_y:
                       num_cells += 1

                       # calculate reference point
                       ref_x = max(min_x_mbr, query_min_x)
                       ref_y = max(min_y_mbr, query_min_y)

                       # check if reference point is inside cell
                       if min_x_mbr <= ref_x <= max_x_mbr and min_y_mbr <= ref_y <= max_y_mbr:
                           id_count += 1
                           results.append(point[0])

           # print results for current query
           print(f"Query {query_number} results:")
           print(results)
           print(f"Cells: {num_cells}")
           print(f"Results: {id_count}")
           print("----------")