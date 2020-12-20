def gen_board(n):
    x = []
    for i in range(n):
        y = []
        for j in range(n):
            y.append(i*n+j)
        x.append(y)
    return x

print(gen_board(10))