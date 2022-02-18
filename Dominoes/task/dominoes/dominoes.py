import itertools
import random


def new_game():
    stock_pieces = [list(i) for i in itertools.combinations_with_replacement(range(7), 2)]
    dominoes_of_players = random.sample(stock_pieces, 14)
    for dominos in dominoes_of_players:
        stock_pieces.remove(dominos)
    player_pieces = dominoes_of_players[:7]
    computer_pieces = dominoes_of_players[7:]
    return stock_pieces, player_pieces, computer_pieces


def rotate_piece(lst):
    return lst[::-1]


def print_game_status():
    print("======================================================================")
    print(f"Stock size: {len(start[0])}")
    print(f"Computer pieces: {len(start[2])}")
    print()
    print_dominoes_snake()
    print()
    print("Your pieces:")
    for num, piece in enumerate(start[1]):
        print(f"{num + 1}:{piece}")
    print()
    if status == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    else:
        print("Status: Computer is about to make a move. Press Enter to continue...")


def print_dominoes_snake():
    if len(domino_snake) <= 6:
        print(*domino_snake)
    else:
        print(*domino_snake[:3] + ["...", ] + domino_snake[-3:])


def choose_player(flg):
    return ("player", "computer")[flg]


def check_game_possibility(lst):
    figure = lst[0][0]
    count = 0
    for i in lst:
        for j in i:
            if j == figure:
                count += 1
    return figure == lst[-1][1] and count == 8


def computer_move():
    global start, flag, domino_snake
    dict_of_points = {i: 0 for i in range(7)}
    possible_pieces = list(filter(lambda x: domino_snake[0][0] in x or domino_snake[-1][1] in x, start[2]))
    for i in range(7):
        for j in possible_pieces + start[2]:
            if i in j:
                dict_of_points[i] += 1
    if len(possible_pieces) > 0:
        possible_pieces = sorted(list(zip(possible_pieces,
                                          list(map(lambda x: dict_of_points[x[0]] + dict_of_points[x[1]],
                                                   possible_pieces)))), key=lambda x: x[1])
        comp_choice = possible_pieces[-1][0]
        start[2].remove(comp_choice)
        if domino_snake[0][0] in comp_choice:
            if domino_snake[0][0] == comp_choice[1]:
                domino_snake.insert(0, comp_choice)
            else:
                domino_snake.insert(0, rotate_piece(comp_choice))
        else:
            if domino_snake[-1][1] == comp_choice[0]:
                domino_snake.append(comp_choice)
            else:
                domino_snake.append(rotate_piece(comp_choice))
    else:
        start[2].append(start[0].pop(random.choice(list(range(0, len(start[0]))))))
    flag = not flag


def player_move(ans):
    global start, flag, domino_snake
    if ans > 0 and domino_snake[-1][1] in start[1][ans - 1]:
        if domino_snake[-1][1] == start[1][ans - 1][0]:
            domino_snake.append(start[1].pop(ans - 1))
        else:
            domino_snake.append(rotate_piece(start[1].pop(ans - 1)))
        flag = not flag
    elif ans < 0 and domino_snake[0][0] in start[1][abs(ans) - 1]:
        if domino_snake[0][0] == start[1][abs(ans) - 1][1]:
            domino_snake.insert(0, start[1].pop(abs(ans) - 1))
        else:
            domino_snake.insert(0, rotate_piece(start[1].pop(abs(ans) - 1)))
        flag = not flag
    elif ans == 0:
        if len(start[0]) > 0:
            taken_piece = random.choice(start[0])
            start[0].remove(taken_piece)
            start[1].append(taken_piece)
            flag = not flag


def print_final_status():
    print("======================================================================")
    print(f"Stock size: {len(start[0])}")
    print(f"Computer pieces: {len(start[2])}")
    print()
    print_dominoes_snake()
    print()
    print("Your pieces:")
    for num, piece in enumerate(start[1]):
        print(f"{num + 1}:{piece}")


def check_answer(answr):
    return all([i in "-1234567890" for i in answr]) and len(start[1]) >= abs(int(answr))


def check_right_piece(ans):
    return ans == 0 or ans > 0 and domino_snake[-1][1] in start[1][ans - 1] or ans < 0 and domino_snake[0][0] in \
           start[1][abs(ans) - 1]


flag = True
domino_snake = []
start = new_game()

while len(list([i for i in start[1] if i[1] == i[0]])) == 0 and len(list([i for i in start[2] if i[1] == i[0]])) == 0:
    start = new_game()
if len(list([i for i in start[1] if i[1] == i[0]])) != 0:
    max_double_comp = max([sum(i) for i in start[1] if i[1] == i[0]]) // 2
else:
    max_double_comp = 0
if len(list([i for i in start[2] if i[1] == i[0]])) != 0:
    max_double_player = max([sum(i) for i in start[2] if i[1] == i[0]]) // 2
else:
    max_double_player = 0
if max_double_comp > max_double_player:
    start[1].remove([max_double_comp, max_double_comp])
    domino_snake.append([max_double_comp, max_double_comp])
else:
    start[2].remove([max_double_player, max_double_player])
    domino_snake.append([max_double_player, max_double_player])
    flag = False

while len(start[1]) > 0 and len(start[2]) > 0 and not check_game_possibility(domino_snake):
    status = choose_player(flag)
    print_game_status()
    if status == "player":
        answer = input().strip("> ")
        while not check_answer(answer):
            print("Invalid input. Please try again.")
            answer = input()
        while not check_right_piece(int(answer)):
            print("Illegal move. Please try again.")
            answer = input()
        player_move(int(answer))
    else:
        input()
        computer_move()
print_final_status()
if len(start[1]) == 0:
    print("Status: The game is over. You won!")
elif len(start[2]) == 0:
    print("Status: The game is over. The computer won!")
else:
    print("Status: The game is over. It's a draw!")
