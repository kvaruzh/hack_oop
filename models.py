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
        self.set_total_params(self.person_attack, self.person_defence_pct,
                              self.person_hp)
        self.restore_health()

    def set_total_params(self, attack, defence, hp):
        """Приравниваем итоговые параметры переданным.
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
        """Получаем урон
        """
        damage = attack_damage - attack_damage * self.person_total_defence_pct
        if damage >= self.current_hp:
            self.set_current_hp(-self.current_hp)
        else:
            self.set_current_hp(-damage)
        return damage

    def attack_enemy(self, enemy):
        """Проводим атаку по указанному врагу
        """
        dam = enemy.take_damage(self.person_total_attack)
        print(f'{self.name} наносит урон {dam:.2f} по {enemy.name}. '
              + f'Осталось {enemy.current_hp:.2f} HP')

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
                              self.person_total_defence_pct,
                              self.person_total_hp)
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
                              self.person_total_defence_pct,
                              self.person_total_hp)
        self.restore_health()
