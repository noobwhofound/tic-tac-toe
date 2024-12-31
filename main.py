import os
import random
import time

class WrongNumber(Exception):
    """
    number should be either 1 or 2
    """
    ...

class WrongGamemode(Exception):
    """
    game mode should be one of the gamemodes below :
    'pvsp', 'pvsai', 'aivsai'
    """
    ...

class WrongDifficulty(Exception):
    """
    difficulty should be one of the categories below :
    'easy', 'medium', 'hard', 'expert', 'random'
    """
    ...

class Tools:
    """
    methods and varibles used in AI and Game classes
    """

    CORNERS = [0, 2, 6, 8]
    SIDES = [1, 3, 5, 7]
    CENTER = 4

    DIFFICULTIES = ['easy', 'medium', 'hard', 'expert', 'random']

    def get_empty_cells(board : list) -> list:
        """
        returns every index containing zero(empty cell)
        """
        return [i for i, cell in enumerate(board) if cell == 0]
    
    def is_valid(board : list, pos : int) -> bool:
        """
        returns True if the position contains zero(empty cell), else False
        """
        if pos > 8 or pos < 0:
            return False
        if board[pos] == 0:
            return True
        return False
    
    def set_move(board : list, pos : int, number : int) -> None:
        """
        used to change the position to the number 
        """
        if board[pos] == 0:
            board[pos] = number
        else:
            print('cant change a non-0 position')

    def is_winning(board : list, number : int) -> bool:
        """
        returns True if the number specified wins the current board status, else False
        """
        le = number
        bo = board

        return ((bo[6] == le and bo[7] == le and bo[8] == le) or 
            (bo[3] == le and bo[4] == le and bo[5] == le) or 
            (bo[0] == le and bo[1] == le and bo[2] == le) or 
            (bo[6] == le and bo[3] == le and bo[0] == le) or 
            (bo[7] == le and bo[4] == le and bo[1] == le) or
            (bo[8] == le and bo[5] == le and bo[2] == le) or 
            (bo[6] == le and bo[4] == le and bo[2] == le) or 
            (bo[8] == le and bo[4] == le and bo[0] == le))
    
    def is_draw(board : list) -> bool:
        """
        returns True if there is no empty cell in the board, else False
        """
        if len(Tools.get_empty_cells(board)) == 0:
            return True
        return False
    
    def copy_board(board : list) -> list:
        """
        returns a copy of the board
        """
        return board[:]



class AI:
    """
    The AI class with 4 different ai difficulties
    """
    
    def __init__(self, number : int, difficulty : str = None) -> None:
        if difficulty == 'easy':
            self.difficulty = 1
        elif difficulty == 'medium':
            self.difficulty = 2
        elif difficulty == 'hard':
            self.difficulty = 3
        elif difficulty == 'expert':
            self.difficulty = 4
        elif difficulty == 'random':
            self.difficulty = random.choice([1, 2, 3, 4])
        else:
            raise WrongDifficulty
        
        if number in [1, 2]:
            self.number = number
        else:
            raise WrongNumber

    def make_random_move(self, board : list, empties : list) -> int:
        """
        makes a random move and returns the move's position
        """
        move_pos = random.choice(empties)
        Tools.set_move(board, move_pos, self.number)
        return move_pos
    
    def any_possible_winning_move(self, board : list, empties : list, number : int) -> int | None:
        """
        reutrns a position in which the number specified has a winning move, else None
        """
        for empty in empties:
            copied_board = Tools.copy_board(board)
            Tools.set_move(copied_board, empty, number)
            if Tools.is_winning(copied_board, number):
                return empty
        return None
    
    def make_diff2_move(self, board: list, empties : list) -> int:
        """
        medium difficulty move
        """
        pwm_ai = self.any_possible_winning_move(board, empties, self.number)
        if pwm_ai != None:
            Tools.set_move(board, pwm_ai, self.number)
            return pwm_ai

        pwm_hu = self.any_possible_winning_move(board, empties, 1 if self.number == 2 else 2)
        if pwm_hu != None:
            Tools.set_move(board, pwm_hu, self.number)
            return pwm_hu
        
        return self.make_random_move(board, empties)
    
    def make_diff3_move(self, board : list, empties : list) -> int:
        """
        hard difficulty move
        """
        pwm_ai = self.any_possible_winning_move(board, empties, self.number)
        if pwm_ai != None:
            Tools.set_move(board, pwm_ai, self.number)
            return pwm_ai

        pwm_hu = self.any_possible_winning_move(board, empties, 1 if self.number == 2 else 2)
        if pwm_hu != None:
            Tools.set_move(board, pwm_hu, self.number)
            return pwm_hu

        random.shuffle(Tools.CORNERS)
        for pos in Tools.CORNERS:
            if pos in empties:
                Tools.set_move(board, pos, self.number)
                return pos
        
        if Tools.CENTER in empties:
            Tools.set_move(board, Tools.CENTER, self.number)
            return Tools.CENTER

        random.shuffle(Tools.SIDES)
        for pos in Tools.SIDES:
            if pos in empties:
                Tools.set_move(board, pos, self.number)
                return pos
            
    def make_diff4_move(self, board : list, empties : list) -> int:
        """
        expert difficulty move
        """
        pwm_ai = self.any_possible_winning_move(board, empties, self.number)
        if pwm_ai != None:
            Tools.set_move(board, pwm_ai, self.number)
            return pwm_ai

        pwm_hu = self.any_possible_winning_move(board, empties, 1 if self.number == 2 else 2)
        if pwm_hu != None:
            Tools.set_move(board, pwm_hu, self.number)
            return pwm_hu
        
        if len(empties) == 8 and ((not 0 in empties) or (not 2 in empties) or (not 6 in empties) or (not 8 in empties)):
            Tools.set_move(board, Tools.CENTER, self.number)
            return Tools.CENTER

        if len(empties) == 6 and ((not 0 in empties) or (not 2 in empties) or (not 6 in empties) or (not 8 in empties)):
            for pos in Tools.SIDES:
                if pos in empties:
                    Tools.set_move(board, pos, self.number)
                    return pos
                
        return self.make_diff3_move(board, empties)
    
    def make_move(self, board : list) -> int | None:
        """
        main method used to make moves using ai, returns ai's move position
        """
        empties = Tools.get_empty_cells(board)
        if len(empties):
            if self.difficulty == 1:
                return self.make_random_move(board, empties)
            elif self.difficulty == 2:
               return self.make_diff2_move(board, empties)
            elif self.difficulty == 3:
                return self.make_diff3_move(board, empties)
            elif self.difficulty == 4:
                return self.make_diff4_move(board, empties)
        return None



class Game:
    """
    The main Game class for displaying the game and playing it with Game.play
    """
    
    def __init__(self, gamemode : str, ai_difficulty : str = None, ai_number : int = None, delay : int = None) -> None:
        if gamemode == 'pvsp':
            self.gamemode = 1
        elif gamemode == 'pvsai':
            self.gamemode = 2
        elif gamemode == 'aivsai':
            self.gamemode = 3
        else :
            raise WrongGamemode
        
        if self.gamemode != 1 :
            if ai_difficulty in Tools.DIFFICULTIES:
                self.ai_difficulty = ai_difficulty
            else :
                raise WrongDifficulty
            
            if ai_number in [1, 2]:
                self.ai_number = ai_number
            else:
                raise WrongNumber
        
        if self.gamemode == 3:
            self.delay = delay if delay != None else 0.5 # seconds

    def first_move_for_player(self) -> bool:
        """
        returns True if the player starts the game, else False
        """
        rand = random.randint(1, 2)
        if rand == 1:
            return True
        return False 
    
    def x_o(self, number : int) -> str :
        """
        returns Mark based on number
        'X' for number 1 , 'O' for number 2, '-' for number 0
        """
        return ('X' if number == 1 else 'O') if number in [1, 2] else '-'
        
    def print_board(self, board : list) -> None:
        """
        prints the board
        """
        Text = ""
        for i in range(1, 10):
            if i % 3 == 0 :
                Text = Text + " " + self.x_o(board[i - 1]) + "\n"
            else :
                Text = Text + " " + self.x_o(board[i - 1])

        print(Text)

    def clear_print(self, board : list) -> None:
        """
        clears the terminal then prints the board
        """
        os.system('cls')
        self.print_board(board)
    
    def ask_for_move(self, board : list) -> int:
        """
        asks the user for a move
        """
        pos = -1
        while not Tools.is_valid(board, pos - 1):
            try :
                pos = int(input("move : "))
            except ValueError:
                print("input numbers")
        return pos
    
    def play(self) -> None:
        """
        main method to play the game with the specified gamemode
        """
        if self.gamemode == 1:
            os.system('cls')
            board = [0 for _ in range(9)]
            self.print_board(board)
            while True:
                print("player 1's turn :")
                p = self.ask_for_move(board)
                Tools.set_move(board, p - 1, 1)

                self.clear_print(board)

                if Tools.is_winning(board, 1):
                    print("player 1 won")
                    break

                if Tools.is_draw(board):
                    print("draw")
                    break

                print("player 2's turn :")
                p = self.ask_for_move(board)
                Tools.set_move(board, p - 1, 2)

                self.clear_print(board)

                if Tools.is_winning(board, 2):
                    print("player 2 won")
                    break

                if Tools.is_draw(board):
                    print("draw")
                    break
            
            wait = input()

        elif self.gamemode == 2:
            os.system('cls')
            board = [0 for _ in range(9)]
            ai = AI(self.ai_number, self.ai_difficulty)
            if not self.first_move_for_player():
                ai.make_move(board)
            self.print_board(board)
                    
            while True :
                p = self.ask_for_move(board)
                Tools.set_move(board, p - 1, 1 if self.ai_number == 2 else 2)

                self.clear_print(board)

                if Tools.is_winning(board, 1 if self.ai_number == 2 else 2):
                    print("you won")
                    break

                if Tools.is_draw(board):
                    print("draw")
                    break
                
                ai.make_move(board)
                self.clear_print(board)

                if Tools.is_winning(board, self.ai_number):
                    print("you lost")
                    break

                if Tools.is_draw(board):
                    print("draw")
                    break

            wait = input()

        elif self.gamemode == 3:
            os.system('cls')
            board = [0 for _ in range(9)]
            ai1 = AI(self.ai_number, self.ai_difficulty)
            ai2 = AI(1 if self.ai_number == 2 else 2, self.ai_difficulty)
            
            while True:
                ai1.make_move(board)
                self.clear_print(board)

                if Tools.is_winning(board, self.ai_number):
                    print("AI 1 won")
                    break

                if Tools.is_draw(board):
                    print("draw")
                    break

                time.sleep(self.delay)

                ai2.make_move(board)
                self.clear_print(board)

                if Tools.is_winning(board, 1 if self.ai_number == 2 else 2):
                    print("AI 2 won")
                    break

                if Tools.is_draw(board):
                    print("draw")
                    break

                time.sleep(self.delay)
            
            wait = input()

        else :
            raise WrongGamemode

    
if __name__ == "__main__":
    # run this file as a main python file to run this part of the code and test the module
    game = Game('aivsai', 'medium', 1, 2)
    while True :
        game.play()

