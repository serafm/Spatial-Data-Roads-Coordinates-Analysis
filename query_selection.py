# Open grid.dir file for reading
with open('data/grid.dir', 'r') as dir_file:
    next(dir_file)

    grid_cells = dict()
    pos = 0
    grid_cells_mbr = dict()

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

                    # store coordinates values
                    for coord in object_values[3:]:
                        x, y = map(float, coord.split())
                        coordinates.append([x, y])

                    grid_cells[(cell_x, cell_y)].append([object_id, object_mbr, coordinates])

                    # find MBR of cell
                    if object_min_x_mbr < cell_min_mbr_x:
                        cell_min_mbr_x = object_min_x_mbr
                    if object_min_y_mbr < cell_min_mbr_y:
                        cell_min_mbr_y = object_min_y_mbr
                    if object_max_x_mbr > cell_max_mbr_x:
                        cell_max_mbr_x = object_max_x_mbr
                    if object_max_y_mbr > cell_max_mbr_y:
                        cell_max_mbr_y = object_max_y_mbr

                # store the new position
                pos = grid_file.tell()

                grid_cells_mbr[(cell_x, cell_y)] = [(cell_min_mbr_x, cell_min_mbr_y), (cell_max_mbr_x, cell_max_mbr_y)]

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

                    if min_x_mbr <= query_max_x and max_x_mbr >= query_min_x and min_y_mbr <= query_max_y and max_y_mbr >= query_min_y:
                        reference_point_x = max(min_x_mbr, query_min_x)
                        reference_point_y = max(min_y_mbr, query_min_y)

                        # check if x,y reference points are in the cell
                        if cell_min_x_mbr <= reference_point_x <= cell_max_x_mbr and cell_min_y_mbr <= reference_point_y <= cell_max_y_mbr:
                            if (query_min_x < min_x_mbr < query_max_x and query_min_x < max_x_mbr < query_max_x) or (query_min_y < min_y_mbr < query_max_y and query_min_y < max_y_mbr < query_max_y):
                                results.append(obj[0])
                            else:
                                for i in range(len(obj[2])):
                                    if i < len(obj[2])-1:
                                        x1 = obj[2][i][0]
                                        y1 = obj[2][i][1]
                                        x2 = obj[2][i+1][0]
                                        y2 = obj[2][i+1][1]
                                        x3 = query_min_x
                                        y3 = query_min_y
                                        x4 = query_max_x
                                        y4 = query_max_y

                                        denominator = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
                                        if denominator == 0:
                                            continue

                                        numerator1 = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4))
                                        numerator2 = ((x1-x3)*(y1-y2) - (y1-y3)*(x1-x2))

                                        if numerator1 == 0 or numerator2 == 0:
                                            continue

                                        if 0 <= numerator1/denominator <= 1 and 0 <= numerator2/denominator <= 1:
                                            results.append(obj[0])
                                            break

        results = sorted(list(set(results)))

        # print results for current query
        print(f"Query {query_number} results:")
        print(*results)
        print(f"Cells: {count_cells}")
        print(f"Results: {len(results)}")
        print("----------")