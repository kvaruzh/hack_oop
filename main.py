import random as rnd

import colorama as clr

import constants as cst
import models as md


def prepare_things():
    """Создаем предметы. Наименование состоит из префикса, имени и
    суффикса. Префикс и название определяем в зависимости от типа предмета.
    """
    elements = []
    items_num = rnd.randint(cst.items_min, cst.items_max)
    for i in range(1, items_num):
        item_type = f'{rnd.choice(cst.thing_types)}'
        item_name = (f'{rnd.choice(cst.thing_name_prefix[item_type])} '
                     + f'{rnd.choice(cst.thing_names[item_type])} '
                     + f'{rnd.choice(cst.thing_name_suffix)}')
        item_attack = rnd.randint(cst.item_attack_min, cst.item_attack_max)
        item_defence = rnd.randint(cst.item_defence_min,
                                   cst.item_defence_max) / 100
        item_hp = rnd.randint(cst.item_hp_min, cst.item_hp_max)
        new_item = md.Thing(item_type, item_name, item_defence, item_attack,
                            item_hp)
        elements.append(new_item)
    return elements


def prepare_persons():
    """Создаем персонажей. Имя персонажей выбираем в зависимости от пола.
    """
    elements = []
    for i in range(0, cst.persons_num):
        pers_sex = rnd.choice(cst.person_sex)
        pers_type = rnd.choice(cst.person_type)
        pers_name = (f'{rnd.choice(cst.person_names[pers_sex])} '
                     + f'{rnd.choice(cst.person_name_suffix[pers_sex])}')
        pers_attack = rnd.randint(cst.person_attack_min, cst.person_attack_max)
        pers_defence = rnd.randint(cst.person_defence_min,
                                   cst.person_defence_max) / 100
        pers_life = rnd.randint(cst.person_hp_min, cst.person_hp_max)
        if pers_type == 'воин':
            new_pers = md.Warrior(pers_type, pers_name, pers_sex, pers_life,
                                  pers_attack, pers_defence)
        elif pers_type == 'паладин':
            new_pers = md.Paladin(pers_type, pers_name, pers_sex, pers_life,
                                  pers_attack, pers_defence)
        elements.append(new_pers)
    return elements


def dress_person(person, things):
    """Одеваем персонажей. берем произвольно от 1 до 4 предметов.
    если очередному персонажу не хватает предметов, он зибарет все оставшиеся
    или не получает ни одного предмета (если предметов не осталось).
    """
    things_num = rnd.randint(1, 4)
    if len(things) < things_num:
        things_num = len(things)
    added_things = []
    for i in range(0, things_num):
        new_thing = rnd.choice(things)
        added_things.append(new_thing)
        left_things.remove(new_thing)
    person.set_things(added_things)
    return 'персонаж {person} одет'


def two_units_fight(unit1, unit2):
    """Проводим бой между двумя персонажами. Если здоровье одного персонажа
    достигает 0, бой завершается. Возвращаем победителя и кол-во раундов.
    """
    cur_round = 0
    while True:
        cur_round += 1
        print(clr.Fore.YELLOW + f'Раунд {cur_round}.')
        print(clr.Style.RESET_ALL, end='')
        unit1.attack_enemy(unit2)
        if unit2.current_hp <= 0:
            left_persons.remove(unit2)
            return unit1, cur_round
        unit2.attack_enemy(unit1)
        if unit1.current_hp <= 0:
            left_persons.remove(unit1)
            return unit2, cur_round


# Создаем предметы и показываем список созданных, отсоритрованный по защите.
all_things = prepare_things()
all_things.sort(key=lambda thing: thing.item_defence_pct)
left_things = all_things[:]
clr.init()
i = 0
for el in all_things:
    i += 1
    print(f'{i}. {el.item_type}, {el.item_name}, Att: {el.item_attack}, '
          f'Def: {el.item_defence_pct:.0%}, HP: {el.item_hit_point}')
"""Создаем персонажей и раздаем им предметы. Показываем созданных персонажей
с их характеристиками. Для каждого персонажа показываем характеристики с
учетом надетых предметов и перечисляем предметы персонажа
"""
persons = prepare_persons()
i = 0
for el in persons:
    i += 1
    # отображаем созданного персонажа
    print(f'{i}. Класс: {el.person_type}, пол: {el.sex}. '
          f'Имя: {el.name}. Att: {el.person_total_attack}, '
          f'Def: {el.person_defence_pct:.0%}, HP: {el.person_hp}')
    dress_person(el, left_things)
    # отображаем характеристики с учтом надетых вещей
    print('\t', f'Att: {el.person_total_attack}, '
          + f'Def: {el.person_total_defence_pct:.0%}, '
          + f'HP: {el.person_total_hp}')
    j = 0
    # отображаем надетые вещи и их характеристики
    for t in el.things:
        j += 1
        print(f'\t\t{j}. {t.item_type}, {t.item_name}, {t.item_attack}, '
              + f'{t.item_defence_pct:.0%}, '
              + f'{t.item_hit_point}')

left_persons = persons[:]
battle_num = 0
while len(left_persons) > 1:
    battle_num += 1
    # Персонажи, доступные для выбора являются копией оставшихся персонажей'
    persons_to_select = left_persons[:]
    # Выбираем перонажей
    unit1 = rnd.choice(persons_to_select)
    persons_to_select.remove(unit1)
    unit2 = rnd.choice(persons_to_select)
    # Проводим бой. Описываем ход боя
    txt = f'\nНачинается бой {battle_num} между:\n\t1. {unit1}\n\t2. {unit2}'
    print(clr.Fore.BLUE + txt)
    print(clr.Style.RESET_ALL, end='')
    # Результаты боя
    battle_results = two_units_fight(unit1, unit2)
    txt = f'В {battle_results[1]} раунде победу одержал: {battle_results[0]}'
    print(clr.Fore.RED + txt)
    print(clr.Style.RESET_ALL)
    # Восстанвливаем здоровье победителя после боя
    battle_results[0].restore_health()
    print(f'Осталось бойцов: {len(left_persons)}')
print(clr.Fore.GREEN + f'Победитель турнира {left_persons[0]}')
