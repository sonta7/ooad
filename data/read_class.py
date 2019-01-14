def file_reader(filename):
    with open(filename) as f:
        col = 0
        line = 0
        while line:
            line = f.readline()
            col+=1
    print(col)


file_reader('class_info.txt')
