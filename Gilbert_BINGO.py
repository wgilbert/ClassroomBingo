"""
Gilbert_BINGO

Description:
"""
import random
import pp
import tsapp

#global variables
players = 1
called_numbers = []
uncalled_numbers = []
all_gameboards = []
number_dislplay = []
window = None
title_label = None
blue = (14,35,62)
green = (118, 190,67)
title_labels = []

for i in range(1,76):
    uncalled_numbers.append(i)


##FUNCTION DEFINITIONS##

def new_game():
    """
    resets the game for the next round
    
    Parameters
    ----------
    None
    
    Return
    -------
    None
    """
    
    global uncalled_numbers
    for i in range(1,76):
        uncalled_numbers[i-1] = i
    called_numbers = []

def call_number(choices):
    """
    gets a random choice from the uncalled number list
    
    Parameters
    ----------
    choices: list of integers
        numbers 1 to 75 that haven't yet been used
    
    Return
    -------
        str:  returns the letter: number combo for the caller to display
        
    """
    global called_numbers
    
    number = random.choice(choices)
    choices.remove(number)
    called_numbers.append(number)
    called_numbers.sort()
    
    if number < 16:
        return "B: " + str(number)
    elif number < 31:
        return "I: " + str(number)
    elif number < 46:
        return "N: " + str(number)
    elif number < 61:
        return "G: " + str(number)
    else:
        return "O: " + str(number)
    
def get_gameboard():
    """
    gets a scrambled game board
    
    Parameters
    ----------
    None
    
    Return
    -------
        grid: a 5x5 matrix of numbers
    """
    used = []
    game_board = []
    game_board.append(["B  ", "I  ","N  ","G  ","O"])
    for row in range(5):
        column = []
        for col in range(5):
            num = random.randint(1,15) + (col*15)
            while num in used:
                num = random.randint(1,15) + (col*15)
            if(row == 2 and col == 2):
                used.append("FS")
                column.append("FS")
            else:
                used.append(num)
                column.append(num)
        game_board.append(column)
    return game_board
    
#### MAIN GAME LOOP ####

def write_boards_to_file(quantity, file_name, label):
    boards = open(file_name, "w")
    for i in range(quantity):
        board = get_gameboard()
        boards.write("Player " + str(i+1) + " board:\n")
        for row in range(len(board)):
            for col in range(len(board[row])):
                boards.write(str(board[row][col]) + "\t")
            boards.write("\n")
        boards.write("\n")                                
    boards.close()

    label.text = str(quantity) + " boards are ready and can be found in your project data."
    label.text += "\nUnder the filename:  " + file_name
    window.finish_frame()
    
def get_gameboard_screen():
    global window
    global number_display
    global title_labels
    
    window = tsapp.GraphicsWindow(1018,573, tsapp.WHITE)
    for label in title_labels:
        window.add_object(label)
    message = "Enter the number of players in the text entry console.\nI will generate random boards for each player."
    text = tsapp.TextLabel("SpecialElite-Regular.ttf", 45, 20, 200, window.width-40, message, blue)
    window.add_object(text)
    window.finish_frame()
    
    players = input("Number of players?\t")
    while not players.isdigit():
        players = input("Not a valid number. Enter number of players?\t")
    players = int(players)
    write_boards_to_file(players, "gameboards.txt", text)
    
def setup_calling_window():
    global window
    global number_display
    global title_labels
    
    window = tsapp.GraphicsWindow(1018,573, tsapp.WHITE)
    for label in title_labels:
        window.add_object(label)
    
    number_display = []
    letter_row = []
    letters = "BINGO"
    grid_squares = []
    grid_square = tsapp.Sprite("IconSquareBlackOutline.png", 0, 0)
    grid_square.scale = .4
    square_width = grid_square.width
    square_height = grid_square.height
    gap = 5
    left_margin = (window.width - ((square_width + gap) * 15))/2
    left_margin = int(left_margin)
    top_margin = (window.height - ((square_height + gap) * 4))/2
    top_margin = int(top_margin)
    
##draw the empty squares##
    for row in range(5):
        column = []
        for col in range(16):
            grid_square = tsapp.Sprite("IconSquareBlackOutline.png", 0, 0)
            grid_square.scale = .4
            grid_square.center_x = left_margin + (square_width + gap) * col
            grid_square.center_y = top_margin + (square_height + gap) * row
            column.append(grid_square)
            window.add_object(grid_square)
        grid_squares.append(column)
    
    ##draw the numbers##      
    for i in range(len(letters)):
        letter = letters[i]
        text = tsapp.TextLabel("SpecialElite-Regular.ttf", 45, 0, 0, square_width, letter, blue)
        text.align = "center"
        text.center_x = grid_squares[i][0].center_x
        text.y = grid_squares[i][0].center_y+10
        window.add_object(text)
    
    for row in range(5):
        column = []
        for col in range(1,16):
            number = str(col + (row*15))
            text = tsapp.TextLabel("SpecialElite-Regular.ttf", 40, 0, 0, square_width, number, blue)
            text.align = "center"
            text.center_x = grid_squares[row][col].center_x
            text.y = grid_squares[row][col].center_y+12
            column.append(text)
            window.add_object(text)
        number_display.append(column)
 
    window.finish_frame()
    

window = tsapp.GraphicsWindow(1018,573, tsapp.WHITE)
x1 = int(window.width * (1/3))
x2 = int(window.width * (2/3))
y = int(window.height/2)

#### create welcome / choice screen grapics ####

title_label_shadow = tsapp.TextLabel("CaveatBrush-Regular.ttf", 80, 5, 90, window.width-40, "Gil-Bingo 2000", blue)
title_label = tsapp.TextLabel("CaveatBrush-Regular.ttf", 80, 0, 85, window.width-40, "Gil-Bingo 2000", green)
title_label_shadow.align = "center"
title_label.align = "center"
title_labels.append(title_label)
title_labels.append(title_label_shadow)
window.add_object(title_label_shadow)
window.add_object(title_label)

screen = 1
make_board_button = tsapp.Sprite("EmptyButton.png", 0, 0)
make_board_button.center = (x1, y)
window.add_object(make_board_button)
make_board_button_label = tsapp.TextLabel("SpecialElite-Regular.ttf", 40, 0, 0, window.width/2, "MAKE GAMEBOARDS", blue)
make_board_button_label.align = "center"
make_board_button_label.center_x = make_board_button.center_x
make_board_button_label.y = make_board_button.y - make_board_button_label.font_size/2
window.add_object(make_board_button_label)

call_game_button = tsapp.Sprite("EmptyButton.png", 0, 0)
call_game_button.center = (x2, y)
window.add_object(call_game_button)
call_game_button_label = tsapp.TextLabel("SpecialElite-Regular.ttf", 40, 0, 0, window.width/2, "CALL A GAME", blue)
call_game_button_label.align = "center"
call_game_button_label.center_x = call_game_button.center_x
call_game_button_label.y = call_game_button.y - call_game_button_label.font_size/2
window.add_object(call_game_button_label)



window.finish_frame()

while window.is_running:
    mouse_x, mouse_y = tsapp.get_mouse_position()

    if screen == 1:
        if make_board_button.is_colliding_point(mouse_x, mouse_y):
            make_board_button.image = "EmptyButtonPressed.png"
            if tsapp.was_mouse_pressed():
                screen = 2
        else:
            make_board_button.image = "EmptyButton.png"
        if call_game_button.is_colliding_point(mouse_x, mouse_y):
            call_game_button.image = "EmptyButtonPressed.png"
            if tsapp.was_mouse_pressed():
                screen = 3

        else:
            call_game_button.image = "EmptyButton.png"
            
    elif screen == 2:
        get_gameboard_screen()
        screen = 5
    elif screen == 3:
        setup_calling_window()
        screen = 4
    elif screen == 4:
        
        input("Press Enter to call the next number: ")
    
        call = call_number(uncalled_numbers)
        index = call.find(" ")
        num = int(call[index+1:])
        
        row = int((num-1) / 15)
        col = int((num)% 15)
        """
        for r in range(len(number_display)):
            for c in range(len(number_display[r])):
                print(number_display[r][c].text, end=" ")
            print()
        """
        if(row >= 0 and row < len(number_display) and col >= 0 and col < len(number_display[0])):
            number_display[row][col-1].color = tsapp.RED
        else:
            print(row, col, "was out of bounds")
        print(call, "  ", num)
        if len(uncalled_numbers) == 0:
            print("That was the last number.")
            window.is_running = False
    window.finish_frame()





