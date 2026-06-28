def havel_hakimi(deg:list)->bool:
    print(deg)
    while True:
        if len(deg) == 0:
            return False

        deg.sort(reverse=True)
        delta = deg[0]

        if delta == 0:
            return True
        if delta >= len(deg):
            return False

        del deg[0]
        print(deg)

        for i in range(0, delta):
            deg[i] -= 1
            if deg[i] < 0:
                return False

        print(deg)
