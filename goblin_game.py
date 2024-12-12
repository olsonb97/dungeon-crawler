import random
import time

def slow_type(text, delay=0.01):

    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def new_line():
    slow_type("------------------------------------")

def get_valid_input(prompt, options=None):
    while True:
        try:
            user_input = input(prompt)
            if int(user_input) in options:
                return int(user_input)
            slow_type("That's not a valid option. Please try again.")
        except ValueError:
            slow_type("That's not a valid option. Please try again.")

class Move:

    def __init__(self, name, power, special=False, recharge=False, status="", target=""):
        self.name = name
        self.power = power
        self.special = special
        self.status = status
        self.target = target
        self.recharge = recharge

    def __repr__(self):
        return self.name

# player moves
punch = Move("Punch", 3)
entomb = Move("Entomb", 0, special=True, status="paralyzed", target='enemy')
maul = Move("Maul", 4)
annihilate = Move("Annihilate", 5)
drowsy_punch = Move("Drowsy Punch", 0, special = True, status="asleep", target='enemy')
takedown = Move("Takedown", 6)
overcharge = Move("Overcharge", 10, recharge=True)

# enemy moves
kick = Move("Kick", 5)
charge = Move("Charge", 0, special=True, status='heal', target='user')
yabber = Move("Yabber", 0, special=True, status='asleep', target='enemy')
stab = Move("Stab", 4)
bump = Move("Bump", 3)
headrush = Move("Head Rush", 7)

class Player:

    def __init__(self):
        self.name = "Player"
        self.hp = 100
        self.maxhp = 100
        self.attack = 5
        self.defense = 3
        self.level = 1
        self.learnable_moves = {1: punch, 2: entomb, 3: maul, 4: annihilate, 5: drowsy_punch, 6: takedown, 7: overcharge}
        self.money = 0
        self.attacks = [self.learnable_moves[1]]
        self.location = None

    def __repr__(self):
        return self.name

class Goblin:

    def __init__(self, level=1):
        self.name = "Goblin"
        self.maxhp = int(random.randint(30, 50)*(level*0.5))
        self.hp = self.maxhp
        self.attack = random.randint(2,3)
        self.defense = random.randint(4,5)
        self.attacks = [
            kick,
            charge,
            yabber,
            bump
        ]

    def __repr__(self):
        return self.name

class KingGoblin:

    def __init__(self, level=1):
        self.name = "King Goblin"
        self.maxhp = int(random.randint(80, 100)*(level*0.5))
        self.hp = self.maxhp
        self.attack = 4
        self.defense = 5
        self.attacks = [
            kick,
            yabber,
            stab,
            bump,
            charge,
            headrush
        ]

    def __repr__(self):
        return self.name

class Room:

    id = 0

    def __init__(self):
        Room.id += 1
        self.id = Room.id
        self.name = f"Room {Room.id}"
        self.defeated = False
        self.mice = [Goblin(Room.id), Goblin(Room.id), KingGoblin(Room.id)]

    def __repr__(self):
        return self.name

class Battle:

    def __init__(self, room, player, enemy):
        self.room = room
        self.player = (player)
        self.player.paralyzed = False
        self.player.paralyzed_counter = 0
        self.player.asleep = False
        self.player.asleep_counter = 0
        self.player.recharging = False
        self.player.recharge_counter = 0
        self.enemy = enemy
        self.enemy.paralyzed = False
        self.enemy.paralyzed_counter = 0
        self.enemy.asleep = False
        self.enemy.asleep_counter = 0
        self.enemy.recharging = False
        self.enemy.recharge_counter = 0

    def already_affected_check(self, checkee):
        if checkee.asleep or checkee.paralyzed:
            slow_type(f"{checkee} is already affected by a status.")
            time.sleep(0.5)
            return True
        return False

    def make_status(self, attacker, defender, move):
        if move.target == "enemy":
            if move.status == "asleep":
                if not self.already_affected_check(defender):
                    defender.asleep = True
                    slow_type(f"{defender} fell asleep!")
            if move.status == "paralyzed":
                if not self.already_affected_check(defender):
                    defender.paralyzed = True
                    slow_type(f"{defender} became paralyzed!")
        elif move.target == "user":
            if move.status == "asleep":
                if not self.already_affected_check(attacker):
                    attacker.asleep = True
                    slow_type(f"{attacker} fell asleep!")
            if move.status == "paralyzed":
                if not self.already_affected_check(attacker):
                    attacker.paralyzed = True
                    slow_type(f"{attacker} became paralyzed!")
            if move.status == 'heal':
                heal_power = int((attacker.maxhp * .2))
                attacker.hp += heal_power
                if attacker.hp > attacker.maxhp:
                    attacker.hp = attacker.maxhp
                slow_type(f"{attacker} healed for {heal_power}!")
        time.sleep(0.5)

    def make_recharging(self, attacker, move):
        if move.recharge:
            attacker.recharging = True
            attacker.recharge_counter = 0

    def check_status(self, checkee):
        if checkee.paralyzed:
            if random.randint(1, 101) < 50:
                return True
            else:
                slow_type(f"{checkee} is paralyzed and couldn't attack.")
                time.sleep(0.5)
                return False
        elif checkee.asleep:
            if checkee.asleep_counter < 1:
                slow_type(f"{checkee} is asleep!")
                checkee.asleep_counter += 1
                return False
            else:
                if checkee.asleep_counter >= 3:
                    slow_type(f"{checkee} woke up!")
                    checkee.asleep = False
                    checkee.asleep_counter = 0
                    return True
                elif random.randint(1, 100) < 30:
                    slow_type(f"{checkee} woke up!")
                    checkee.asleep = False
                    checkee.asleep_counter = 0
                    return True
                else:
                    slow_type(f"{checkee} is asleep!")
                    checkee.asleep_counter += 1
                    return False
        return True
                
    def choose_enemy_move(self, enemy):
        move = random.choice(enemy.attacks)
        return move
    
    def get_damage(self, move, attacker, defender):
        damage = int(move.power * attacker.attack * defender.defense * 0.25)
        return damage
    
    def take_damage(self, damage, taker):
        taker.hp -= damage
        if taker.hp <= 0:
            taker.hp = 0
                
    def print_health(self, player=False, enemy=False):
        new_line()
        if player:
            slow_type(f"{self.player} HP: {self.player.hp}/{self.player.maxhp}")
        if enemy:
            slow_type(f"{self.enemy} HP: {self.enemy.hp}/{self.enemy.maxhp}")

    def check_recharge(self, attacker):
        if attacker.recharging and attacker.recharge_counter <1:
            attacker.recharge_counter += 1
            slow_type(f"{attacker} is recharging from the last attack!")
            return False
        else:
            attacker.recharge_count = 0
            attacker.recharging = False
            return True

    def attack(self, attacker, defender, move):
        new_line()
        if self.check_recharge(attacker):
            if self.check_status(attacker) and not attacker.recharging :
                if move.power == 0:
                    slow_type(f"{attacker} used {move}!")
                    self.make_status(attacker, defender, move)
                else:
                    slow_type(f"{attacker} used {move}!")
                    damage = self.get_damage(move, attacker, defender)
                    self.take_damage(damage, defender)
                    slow_type(f"{defender} took {damage} damage!")
                    self.make_recharging(attacker, move)

    def player_turn(self, player, enemy):
        for index, move in enumerate(player.attacks):
            slow_type(f"{index+1}. {move}")
        choice_index = get_valid_input("Enter number: ", list(range(1, len(player.attacks)+1)))-1
        self.attack(player, enemy, player.attacks[choice_index])

    def enemy_turn(self, enemy, player):
        self.attack(enemy, player, self.choose_enemy_move(enemy))

    def health_check(self, player, enemy):
        if player.hp <= 0 or enemy.hp <= 0:
            return False
        return True

    def battle_check(self, player, enemy):
        if player.hp <= 0:
            slow_type("You lost the fight...")
            return None
        elif enemy.hp <= 0:
            slow_type("You won the fight!")
            return random.randint(1, 10)

    def battle(self):
        while self.player.hp > 0 and self.enemy.hp > 0:
            if not self.health_check(self.player, self.enemy):
                return self.battle_check(self.player, self.enemy)
            self.print_health(player=True, enemy=True)
            self.player_turn(self.player, self.enemy)
            time.sleep(0.5)
            if not self.health_check(self.player, self.enemy):
                return self.battle_check(self.player, self.enemy)
            self.print_health(player=True, enemy=True)
            self.enemy_turn(self.enemy, self.player)
            time.sleep(0.5)

class Game:

    def __init__(self, player):
        self.player = player

    def lose(self, manual=False):
        if self.player.hp <= 0 or manual:
            slow_type("You lost the game...", 0.05)
            slow_type(f"Final Score: ${self.player.money}", 0.05)
            input()
            quit()

    def generate_room(self):
        yield Room()

    def room_loop(self, player, room):
        while True:
            if len(room.mice) <= 0:
                new_line()
                slow_type(f"You beat {room.name}!")
                time.sleep(1)
                slow_type(f"{player} healed to full")
                time.sleep(1)
                return True
            room_encounters = len(room.mice)
            slow_type(f"---------- {room.name} ----------")
            slow_type(f"1. Fight ({room_encounters} left)\n2. Check Money\n3. Quit")
            choice = get_valid_input("Enter number: ", [1,2,3])
            if choice == 1:
                money_won = Battle(room, player, room.mice[0]).battle()
                if money_won is not None:
                    slow_type(f"{player} won ${money_won}!")
                    player.money += money_won
                    room.mice.pop(0)
                else:
                    break
            elif choice == 2:
                slow_type(f"You have ${player.money}")
            elif choice == 3:
                self.lose(manual=True)
        self.lose()

    def game_loop(self):
        while self.player.hp >= 0:
            room = next(self.generate_room())
            if self.room_loop(self.player, room):
                self.player.attacks += [self.player.learnable_moves[Room.id+1]]
                slow_type(f"{player} learned {self.player.learnable_moves[Room.id+1]}")
                self.player.hp = self.player.maxhp
                time.sleep(1)
                continue
            else:
                self.lose()

player = Player()
game = Game(player)
game.game_loop()
