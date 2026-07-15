def sequence(matrix):
    if len(matrix) == 1:
        return True
    return False

def incidence(matrix):
    #sum col
    sum_col = []
    for k in range(len(matrix[0])):
        sum_ = 0
        for l in range(len(matrix)):
            sum_ += int(matrix[l][k])
        sum_col.append(sum_)

    if sum(sum_col) == 2 * (len(matrix[0])):
        return True
    return False


def adjacency(matrix):
    #trace
    count = 0
    for n in range(len(matrix)):
        for m in range(len(matrix[0])):
            if matrix[n][m] == 0 and n == m:
                count += 1
    if count == len(matrix) and len(matrix[0]) == len(matrix):
        return True
    return False


def edge(matrix):
    count = 0
    for i in range(len(matrix)):
        if len(matrix[i]) == 2:
            count +=1
    if count == len(matrix):
        return True
    return False

def sum_row(matrix):
    deg = []
    for i in range(len(matrix)):
        sum_row = 0
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                continue
            else:
                matrix[i][j] /= matrix[i][j]
            sum_row += int(matrix[i][j])
        deg.append(sum_row)
    return deg


def detect(content):
    matrix = []
    deg = []

    #matrix
    for i in content.split("\n"):
        row =[]
        for j in i.strip().replace("\t",",").replace(" ",",").split(","):
            if j == "":
                continue
            else:
                row.append(int(j))
        matrix.append(row)

    # edge list
    if edge(matrix):
        deg_dict = {}
        for number in range(len(matrix)):
            if len(matrix[number]) != 2:
                continue
            deg_dict.setdefault(matrix[number][0], 0)
            deg_dict.setdefault(matrix[number][1], 0)
            deg_dict[matrix[number][0]] += 1
            deg_dict[matrix[number][1]] += 1
        for value in deg_dict.values():
            deg.append(value)
        return deg

    # sequence
    elif sequence(matrix):
        for i in matrix[0]:
            deg.append(int(i))
        return deg

    # incidence
    elif incidence(matrix):
        deg = sum_row(matrix)
        return deg

    #adjacency
    elif adjacency(matrix):
        deg = sum_row(matrix)
        return deg


#read file
def readfile(file):
    file_graph = open(file,"r")
    content = file_graph.read()
    file_graph.close()
    return detect(content)
