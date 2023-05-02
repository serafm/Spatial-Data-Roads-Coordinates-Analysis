# Open grid.dir file for reading
with open('data/grid.dir', 'r') as dir_file:
    next(dir_file)

    grid_cells = dict()
    pos = 0
    grid_cells_mbr = dict()
    all_mbrs = []

    for line in dir_file:
        cell_x, cell_y, number_of_ids = map(int, line.split())

        if number_of_ids > 0:
            with open('data/grid.grd', 'r') as grid_file:
                grid_cells[(cell_x, cell_y)] = []
                # seek to the last position in the file
                grid_file.seek(pos)

                cell_min_mbr_x = 0
                cell_min_mbr_y = 9999
                cell_max_mbr_x = -9999
                cell_max_mbr_y = 0

                for obj in range(number_of_ids):
                    coordinates = []
                    object_values = grid_file.readline().split(',')
                    # object id
                    object_id = int(object_values[0])

                    # store mbr values
                    object_min_mbr = object_values[1].split()
                    object_max_mbr = object_values[2].split()
                    object_min_x_mbr = float(object_min_mbr[0])
                    object_min_y_mbr = float(object_min_mbr[1])
                    object_max_x_mbr = float(object_max_mbr[0])
                    object_max_y_mbr = float(object_max_mbr[1])
                    object_mbr = [(object_min_x_mbr, object_min_y_mbr), (object_max_x_mbr, object_max_y_mbr)]
                    all_mbrs.append(object_mbr)

                    # store coordinates values
                    for coord in object_values[3:]:
                        x, y = map(float, coord.split())
                        coordinates.append([x, y])

                    grid_cells[(cell_x, cell_y)].append([object_id, object_mbr, coordinates])

                # store the new position
                pos = grid_file.tell()

                # find MBR of cells
                min_x = min(mbr[0][0] for mbr in all_mbrs)
                max_x = max(mbr[1][0] for mbr in all_mbrs)
                min_y = min(mbr[0][1] for mbr in all_mbrs)
                max_y = max(mbr[1][1] for mbr in all_mbrs)

                # Create a grid of cells with equal range of values
                for x in range(10):
                    for y in range(10):
                        grid_cells_mbr[(x, y)] = [(min_x + x * (max_x - min_x) / 10, min_y + y * (max_y - min_y) / 10), (min_x + (x + 1) * (max_x - min_x) / 10, min_y + (y + 1) * (max_y - min_y) / 10)]

# Open queries.txt file for reading
with open('data/queries.txt', 'r') as queries:
    for query in queries:
        query = query.split(',')
        query_number = query[0]
        query_min_x = float(query[1].split()[0])
        query_max_x = float(query[1].split()[1])
        query_min_y = float(query[1].split()[2])
        query_max_y = float(query[1].split()[3])

        count_cells = 0
        results = []

        for cell in grid_cells:
            # get cell mbr values
            cell_min_x_mbr = grid_cells_mbr[cell][0][0]
            cell_min_y_mbr = grid_cells_mbr[cell][0][1]
            cell_max_x_mbr = grid_cells_mbr[cell][1][0]
            cell_max_y_mbr = grid_cells_mbr[cell][1][1]

            # check if cell mbr is in window query mbr
            if cell_min_x_mbr <= query_max_x and cell_max_x_mbr >= query_min_x and cell_min_y_mbr <= query_max_y and cell_max_y_mbr >= query_min_y:
                count_cells += 1
                for obj in grid_cells[cell]:
                    min_x_mbr = obj[1][0][0]
                    min_y_mbr = obj[1][0][1]
                    max_x_mbr = obj[1][1][0]
                    max_y_mbr = obj[1][1][1]

                    reference_point_x = max(min_x_mbr, query_min_x)
                    reference_point_y = max(min_y_mbr, query_min_y)

                    # check if x,y reference points are in the cell
                    if cell_min_x_mbr <= reference_point_x <= cell_max_x_mbr and cell_min_y_mbr <= reference_point_y <= cell_max_y_mbr:
                        if min_x_mbr <= query_max_x and max_x_mbr >= query_min_x and min_y_mbr <= query_max_y and max_y_mbr >= query_min_y:
                            results.append(obj[0])

        results = sorted(list(set(results)))

        # print results for current query
        print(f"Query {query_number} results:")
        print(*results)
        print(f"Cells: {count_cells}")
        print(f"Results: {len(results)}")
        print("----------")
