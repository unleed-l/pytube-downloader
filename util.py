from os import system, name
class Util:
    @staticmethod
    def clear_terminal():
        if name == 'nt':
            system('cls')
        else:
            system('clear')
