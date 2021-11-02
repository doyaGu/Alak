def newBoard(n):
    return [0 for i in range(n)]


def display(board, n):
    def trans(num):
        if num == 0:
            return '.'
        else:
            return 'x' if num == 1 else 'o'
    output = ' '.join(list(map(trans, board)))
    print(output + '\n' + ' '.join([str(i) for i in range(1, n + 1)]))


def getInput():
    while True:
        try:
            i = int(input("Choose a licit number of square : "))
        except ValueError:
            print("You should enter an integer.")
        else:
            return i - 1


def possible(board, n, player, removed, i):
    return n > i >= 0 == board[i] and i not in removed[player - 1]


def select(board, n, player, removed):
    if player == 1:
        print('Player 1')
    else:
        print('Player 2')

    i = getInput()
    while not possible(board, n, player, removed, i):
        i = getInput()
    return i


def getGroups(board):
    from itertools import groupby
    keys = []
    groups = []
    index = 0
    for key, group in groupby(board):
        indices = list(group)
        for i in range(len(indices)):
            indices[i] = index
            index += 1
        keys.append(key)
        groups.append(indices)
    return keys, groups


def search(part, player):
    adversary = 2 if player == 1 else 1
    if not part or part[0] != adversary:
        return False
    try:
        player_index = part.index(player)
    except ValueError:
        if 0 in part:
            return False
        else:
            return True
    else:
        return 0 not in part[:player_index]


def check(keys, player, k, groups, removed, direction):
    adversary = 2 if player == 1 else 1
    left = keys[:k]
    right = keys[k + 1:]

    if direction != 'left':
        if search(right, player):
            removed[adversary - 1].extend(groups[k + 1 if k < len(groups) - 1 else 0])
    if direction != 'right':
        left.reverse()
        if search(left, player):
            removed[adversary - 1].extend(groups[len(groups) - 1 if k <= 0 else k - 1])


def put(board, player, removed, i):
    adversary = 2 if player == 1 else 1
    removed[adversary - 1].clear()
    board[i] = player

    keys, groups = getGroups(board)
    for k, g in enumerate(groups):
        if i == g[0] and i == g[-1]:
            check(keys, player, k, groups, removed, 'both')
            break
        elif i == g[0]:
            check(keys, player, k, groups, removed, 'left')
            break
        elif i == g[-1]:
            check(keys, player, k, groups, removed, 'right')
            break

    for i in removed[adversary - 1]:
            board[i] = 0


def again(board, n, player, removed):
    if 0 in board:
        if removed[player - 1]:
            empties = set(filter(lambda i: board[i] == 0, list(range(n))))
            return bool(empties.difference(set(removed[player - 1])))
        else:
            return True
    return False


def win(board, n):
    display(board, n)
    if board.count(1) > board.count(2):
        print('Winner : 1')
    elif board.count(1) < board.count(2):
        print('Winner : 2')
    else:
        print("Winner: Tie")


def alak(n):
    board = newBoard(n)
    removed = [[], []]
    player = 1
    while again(board, n, player, removed):
        display(board, n)
        print('\n')
        i = select(board, n, player, removed)
        print('\n')
        put(board, player, removed, i)

        player = 2 if player == 1 else 1
    win(board, n)


if __name__ == '__main__':
    alak(9)
