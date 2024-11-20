import random
import msvcrt
import os
import time


class Player:
    def __init__(self, name, hp, atk, df, pos_x, pos_y):
        self.name = name
        self.hp = hp
        self.current_hp = hp
        self.atk = atk
        self.df = df
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.bounty = 0


def show_dungeon(dungeon, player, bounty_count):
    print(player.name, '*', f'   найдено сокровищ: {player.bounty}/{bounty_count}')
    print(f'Здоровье: {player.current_hp}/{player.hp}')
    print('Перемещайтесь стрелочками')
    for i in range(len(dungeon)):
        print('|', end='')
        for j in range(len(dungeon)):
            print(f'{dungeon[i][j]}', end='|')
        print('')
        

def bounty_generate(dungeon, bounty_count):
    for bounty_counter in range(bounty_count):
        flag = True
        while flag:
            new_bounty = (random.randint(0, 3), random.randint(0, 3))
            if not (dungeon[new_bounty[0]][new_bounty[1]] in '*b'):
                dungeon[new_bounty[0]][new_bounty[1]] = 'b'
                flag = False

def monsters_generate(dungeon, monsters_count):
    for monsters_counter in range(monsters_count):
        flag = True
        while flag:
            new_monster = (random.randint(0, 3), random.randint(0, 3))
            if not (dungeon[new_monster[0]][new_monster[1]] in '*bM'):
                dungeon[new_monster[0]][new_monster[1]] = 'M'
                flag = False

def battle(player):
    monster_hp = random.randint(7, 10)
    monster_hp_current = monster_hp
    monster_atk = random.randint(1, 3)
    while player.current_hp > 0 and monster_hp_current > 0:
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Вы нашли монстра. Начинается бой!')
        print('Ваши характеристики:')
        print(f'Здоровье: {player.current_hp}/{player.hp}')
        print(f'Защита: {player.df}')
        print(f'Атака: {player.atk}')
        print(
            "Ваш противник:\n"
            " .-.\n"
            "(o o) boo!\n"
            "| O \\\n"
            " \\   \\\n"
            "  `~~~'\n"
        )
        print('Характеристики монстра:')
        print(f'Здоровье: {monster_hp_current}/{monster_hp}')
        print(f'Атака: {monster_atk}')
        print('1 - атаковать, 2 - защищаться')
        key = b''
        trust_key = True
        is_def = False
        while trust_key:
            key = msvcrt.getch()
            match key:
                case b'1':
                    monster_hp_current -= player.atk
                    print(f'Монстр получил {player.atk} урона!')
                    trust_key = False
                case b'2':
                    print(f'Вы защищаетесь!')
                    trust_key = False
                    is_def = True
        if is_def:
            player.current_hp -= (monster_atk - player.df)
            print(f'Вам нанесли {monster_atk - player.df} урона')
            if player.current_hp >= 0:
                print(f'Вы восстановили 2 здоровья, пока защищались')
                player.current_hp += 2
        else:
            player.current_hp -= monster_atk
        if player.current_hp <= 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Вы погибли')
            time.sleep(1)
            return 0
        if monster_hp_current <= 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Вы победили монстра')
            print(
                " .-.\n"
                "(x x) boo!\n"
                "| O \\\n"
                " \\   \\\n"
                "  `~~~'\n"
            )
            time.sleep(1)
            return 1


print('Текстовая игра подземелье')

bounty_count = 6
monsters_count = 3

Win = 0
player = Player(
    input('Введите имя персонажа: '),
    random.randint(15, 25),
    random.randint(3, 4),
    random.randint(0, 2),
    random.randint(0,3),
    random.randint(0,3)
)
dungeon = [
    ['-', '-', '-', '-'],
    ['-', '-', '-', '-'],
    ['-', '-', '-', '-'],
    ['-', '-', '-', '-'],
]
visible_dungeon = [
    ['?', '?', '?', '?'],
    ['?', '?', '?', '?'],
    ['?', '?', '?', '?'],
    ['?', '?', '?', '?'],
]
dungeon[player.pos_y][player.pos_x] = '*'
visible_dungeon[player.pos_y][player.pos_x] = '*'

bounty_generate(dungeon, bounty_count)
monsters_generate(dungeon, monsters_count)
while Win == 0:
    os.system('cls' if os.name == 'nt' else 'clear')
    show_dungeon(visible_dungeon,player, bounty_count)
    match dungeon[player.pos_y][player.pos_x]:
        case 'b':
            player.bounty += 1
            if player.bounty == bounty_count:
                Win = 1
                continue
            else:
                print('Вы нашли сокровище')
            dungeon[player.pos_y][player.pos_x] = '-'
        case 'M':
            battle_result = battle(player)
            if battle_result == 0:
                Win = -1
                continue
            else:
                dungeon[player.pos_y][player.pos_x] = '-'
                continue
        case _:
            print('Здесь пусто')
    key = b''
    trust_key = True
    last_x = player.pos_x
    last_y = player.pos_y
    while trust_key:
        key = msvcrt.getch()
        match key:
            case b'H':
                if player.pos_y > 0:
                    player.pos_y -= 1
                    trust_key = False
            case b'P':
                if player.pos_y < 3:
                    player.pos_y += 1
                    trust_key = False
            case b'K':
                if player.pos_x > 0:
                    player.pos_x -= 1
                    trust_key = False
            case b'M':
                if player.pos_x < 3:
                    player.pos_x += 1
                    trust_key = False
    visible_dungeon[last_y][last_x] = '-'
    visible_dungeon[player.pos_y][player.pos_x] = '*'

if Win == 1:
    print('Вы нашли все сокровища. Вы победили!')
else:
    print('Игра окончена!')
end = input('Нажмите Enter для закрытия')