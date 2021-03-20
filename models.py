class Thing():
    """Класс содержит в себе следующие параметры - тип предмета,
    название, процент защиты, атаку и жизнь.
    """
    def __init__(self, item_type: str, item_name: str, item_defence_pct: float,
                 item_attack: float, item_hit_point: float):
        self.item_type = item_type
        self.item_name = item_name
        self.item_defence_pct = item_defence_pct
        self.item_attack = item_attack
        self.item_hit_point = item_hit_point

    def __str__(self):
        return f'{self.item_type}, {self.name}'


class Person():
    """Класс, содержащий в себе следующие параметры:
    - Имя, пол, кол-во жизней, базовую атаку, базовый процент защиты.
    Параметры передаются через конструктор;
    - метод, принимающий на вход список вещей *`setThings(things)`*;
    - метод вычитания жизни на основе входной атаки, а также методы
    для выполнения алгоритма, представленного ниже;
    """
    def __init__(self, name: str, sex: str, person_hp: float,
                 person_attack: float, person_defence_pct: float):
        self.name = name
        self.sex = sex
        self.person_hp = person_hp
        self.person_attack = person_attack
        self.person_defence_pct = person_defence_pct
        self.wins = 0
        self.loses = 0
        self.damage_made = 0
        self.damage_get = 0
        self.is_dead = False

    def update_stats(self, wins: int = 0, loses: int = 0,
                     damage_made: float = 0, damage_get: float = 0):
        """Обновляем статистику по персонажа: побед в боях, поражений в боях,
        нанесенный урон, полученный урон
        """
        self.wins += wins
        self.loses += loses
        self.damage_made += damage_made
        self.damage_get += damage_get

    def set_total_params(self, attack, defence, hp):
        """Записываем итоговые параметры. Значения с учетом бонысов от предметов и т.п.
        """
        self.person_total_attack = attack
        self.person_total_hp = hp
        self.person_total_defence_pct = defence

    def set_current_hp(self, hp):
        """Изменяем текущий уровень здоровья на переданный параметр.
        """
        self.current_hp += hp

    def change_parameters(self, thing: Thing, undress: int = 1):
        """Изменяем параметры персонажа на основании характеристики предмета.
        Дополнительный необязательный параметр указывает снимаем ли мы предмет.
        1 - надеваем, -1 - снимаем.
        Т.е. увеличиваем, либо уменьшаем характеристики.
        """
        self.set_total_params(
            self.person_total_attack + thing.item_attack * undress,
            self.person_total_defence_pct + thing.item_defence_pct * undress,
            self.person_total_hp + thing.item_hit_point * undress)
        self.set_current_hp(thing.item_hit_point * undress)

    def restore_health(self):
        """Восстанавливаем здоровье персонажа до максимального
        """
        self.current_hp = self.person_total_hp

    def set_things(self, things):
        """Надеваем вещи.
        """
        self.things = things
        for item in things:
            self.change_parameters(item)

    def take_damage(self, attack_damage: float):
        """Получаем урон. Если урон превышает оставшуюся жизнь,
        приравниваем оставшуюся жизнь к 0.
        """
        loss = 0
        damage = attack_damage - attack_damage * self.person_total_defence_pct
        if damage >= self.current_hp:
            self.set_current_hp(-self.current_hp)
            self.is_dead = True
            loss = 1
        else:
            self.set_current_hp(-damage)
        self.update_stats(loses=loss, damage_get=damage)
        return damage

    def attack_enemy(self, enemy):
        """Проводим атаку по указанному врагу
        """
        win = 0
        dam = enemy.take_damage(self.person_total_attack)
        print(f'{self.name} наносит урон {dam:.2f} по {enemy.name}. '
              + f'Осталось {enemy.current_hp:.2f} HP')
        if enemy.current_hp <= 0:
            win = 1
        self.update_stats(wins=win, damage_made=dam)
        return dam

    def __str__(self):
        return (f'{self.person_type} - {self.name}; '
                + f'Att: {self.person_total_attack} '
                + f'HP: {self.person_total_hp:.2f} '
                + f'Def: {self.person_total_defence_pct:.0%}')


class Paladin(Person):
    """Класс наследуется от персонажа, при этом количество присвоенных
    жизней и процент защиты умножается на 2 в конструкторе;
    """
    def __init__(self, person_type: str, name: str, sex: str, person_hp: float,
                 person_attack: float, person_defence_pct: float):
        super().__init__(name, sex, person_hp,
                         person_attack, person_defence_pct)
        self.person_type = person_type
        self.person_hp = self.person_hp * 2
        self.person_defence_pct = self.person_defence_pct * 2
        self.set_total_params(self.person_attack,
                              self.person_defence_pct,
                              self.person_hp)
        self.restore_health()


class Warrior(Person):
    """Класс наследуется от персонажа, при этом атака умножается
    на 2 в конструкторе."""
    def __init__(self, person_type: str, name: str, sex: str, person_hp: float,
                 person_attack: float, person_defence_pct: float):
        super().__init__(name, sex, person_hp,
                         person_attack, person_defence_pct)
        self.person_type = person_type
        self.person_attack = self.person_attack * 2
        self.set_total_params(self.person_attack,
                              self.person_defence_pct,
                              self.person_hp)
        self.restore_health()


class Battle():
    def __init__(self, battle_num: int, pers1: Person, pers2: Person):
        self.battle_num = battle_num
        self.pers1 = pers1
        self.pers2 = pers2
        self.rounds = 0
        self.damage = 0
        self.winner = None

    def update_battle_info(self, round_num: int = 0, damages: float = 0,
                           winner=None):
        self.rounds += round_num
        self.damage += damages
        self.winner = winner

    def __str__(self):
        return (f'{self.pers1}\n{self.pers2}\nРаундов: {self.rounds}, '
                + f'Всего урона: {self.damage}')


class Tournament():
    def __init__(self, name: str):
        self.name = name
        self.battles = []

    def update_tournament_info(self, battle: Battle):
        self.battles.append(battle)

    def __str__(self):
        return f'{self.name}'
