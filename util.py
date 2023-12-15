from os import system, name

class Util:
    @staticmethod
    def clearTerminal():
        if name == 'nt' : system('cls')
        else: system('clear')