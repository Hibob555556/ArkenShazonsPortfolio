"""
  Customizations: I added a hidden option in one of the rooms and a map display for the game. You will also be able to trigger another play-through after success or death. 
"""

"""
  Author: Cayden Lunt
  Class: CSE - 110
  Date: 7-8-2025
"""

# import needed deps
import os

# define shapes
vert_wall = "    ◙   ◙"
wall = "◙"
person = "☻"
monster = "☼"

# display success message and ask if they would like to play again
def success_message(custom_message):
    clear_console()
    message = ''' __   __           __        __          _ 
 \\ \\ / /__  _   _  \\ \\      / /__  _ __ | |
  \\ V / _ \\| | | |  \\ \\ /\\ / / _ \\| '_ \\| |
   | | (_) | |_| |   \\ V  V / (_) | | | |_|
   |_|\\___/ \\__,_|    \\_/\\_/ \\___/|_| |_(_)
'''
    print(message)
    print("-----------------------------------------------")
    print(custom_message)
    question = "Would you like to play again?"
    options = ["yes", "no"]
    play_again = get_user_input(question, options, False, False)
    if play_again.lower() == "yes":
        game()
    else:
        print("Goodbye!")
        quit()


# display death message and ask if they would like to play again
def death_messge(custom_message = ""):
    clear_console()
    message = """__   __            ____  _          _ _ 
\\ \\ / /__  _   _  |  _ \\(_) ___  __| | |
 \\ V / _ \\| | | | | | | | |/ _ \\/ _` | |
  | | (_) | |_| | | |_| | |  __/ (_| |_|
  |_|\\___/ \\__,_| |____/|_|\\___|\\__,_(_)"""
    print(message)
    print("-----------------------------------------------")
    if custom_message != "":
        print(custom_message)
    question = "Would you like to play again?"
    options = ["yes", "no"]
    play_again = get_user_input(question, options, False, False)
    if play_again.lower() == "yes":
        game()
    else:
        print("Goodbye!")
        quit()


# clear the console to make it look pretty
def clear_console():
    if os.name == 'nt':  # name for windows
        _ = os.system('cls')
    else:  # if not windows it is usually mac or linux and clear should work
        _ = os.system('clear')


# print the chamber wall to nth thickness and height
def print_chamber_wall(thickness: int, height: int):
     for i in range(height):
          print(wall, end="")
          for n in range(thickness - 2):
            print(" ", end="")
          print(wall)


# print a chamber with a monster in it
def print_vertical_chamber_with_monster():
    # print the vertical wall for the offshoot for the door
    for i in range(2):
        print(vert_wall)

    # print walls with holes for the door
    holes = [5,6,7]
    for i in range(13):
        if i not in holes:
            print(wall, end="")    
        else:
            print(" ", end="")

    # print the chamber body /w monster
    print()
    print_chamber_wall(13,1)
    print(f"{wall}     {monster}     {wall}")
    print_chamber_wall(13,3)

    # print walls with holes for the door
    holes = [5,6,7]
    for i in range(13):
            if i not in holes:
                print(wall, end="")  
            elif i == 6:
                print(person, end="")
            else:
                print(" ", end="")
    
    # print the vertical wall for the offshoot for the door
    print()
    for i in range(2):
        print(vert_wall)


# print a chamber with a trap in it
def print_horizontal_chamber_with_trap(door_closed = False):
    # print the top of the chamber
    for i in range(2):
        for j in range (2):
            print(" ", end="")
        print(wall, end="")
        if i < 1:
            for n in range(10):
                print(wall, end="")
        else: 
            for j in range(9):
                print(" ", end="")
            print(wall, end="")
        print()
    
    # print the middle of the chamber
    for i in range(3):
        print(wall, end="")
    for j in range(9):
        print(" ", end="")
    for i in range(3):
        print(wall, end="")
    if door_closed:
        print(f"\n{wall} {person}     x")
    else:
        print(f"\n {person}     x")
    for i in range(3):
        print(wall, end="")
    for j in range(9):
        print(" ", end="")
    for i in range(3):
        print(wall, end="")
    print()

    # print the bottom of the chamber
    for i in range(2):
        for j in range (2):
            print(" ", end="")
        if i == 1:
            print(wall, end="")
            for n in range(10):
                print(wall, end="")
        else:
            print(wall, end="")
            for j in range(9):
                print(" ", end="")
            print(wall, end="")
        print()


# print a straight wall and door
def straight_or_left_wall():
    # print 2 vertical wall sections
    for i in range(2):
        print(vert_wall)

    # print walls going 12 spaces if there is not a doorway there
    holes = [5,6,7]
    for i in range(12):
        if i not in holes:
            print(wall, end="")    
        else:
            print(" ", end="")
    print(f"\n   {person}    ")

    # print the bottom wall section
    for i in range(12):
        print(wall, end="")


# get input from the user
def get_user_input(question: str, options: list, separator = True, spacer = True):
    # store the original question 
    original_question = question

    # check if there should be a space
    if spacer:
        print()

    # check if the seperator (-------...) should be present
    if separator:
        for i in range(len(question)):
            print("-", end="")
        print("\n")

    # store all of the options in lower case
    for option in options:
        if ("[HIDDEN]" not in option):
            question += f"\n  > {option.upper()}"
        
    # add the "answer" text to the end of the question
    question += "\n\nAnswer: "

    # get the users answer
    answer = (input(question)).lower()

    # store all of the options in lower case
    lower_options = []
    for option in options:
        lower_options.append(option.lower())

    # if the answer exists in the lower_options array return the users answer
    if (answer.lower() in lower_options) or (f"[hidden]{answer}" in lower_options):
        return answer.lower()
    # if the answer does not exist in the array ask again
    else:
        return get_user_input(original_question, options)


# print the final chamber with chest
def print_horizontal_chamber_with_chest():
    # print the top of the chamber
    for i in range(2):
        for j in range (2):
            print(" ", end="")
        print(wall, end="")
        if i < 1:
            for n in range(10):
                print(wall, end="")
        else: 
            for j in range(9):
                print(" ", end="")
            print(wall, end="")
        print()
    
    # print the middle of the chamber
    for i in range(3):
        print(wall, end="")
    for j in range(9):
        print(" ", end="")
    print(wall, end="")
    print(f"\n {person}     ♦    {wall}")
    for i in range(3):
        print(wall, end="")
    for j in range(9):
        print(" ", end="")
    print(wall, end="")
    print()

    # print the bottom of the chamber
    for i in range(2):
        for j in range (2):
            print(" ", end="")
        if i == 1:
            print(wall, end="")
            for n in range(10):
                print(wall, end="")
        else:
            print(wall, end="")
            for j in range(9):
                print(" ", end="")
            print(wall, end="")
        print()

# Game 
# -----------------------------------------------------------

def game():
    # clear console for best user experience
    clear_console()

    print("You are a brave adventurer and have stumbled into a dungeon. \nYou have found yourself trapped and need to escape.")
    print("----------------------------------------------------------------------")

    # Print wall
    straight_or_left_wall()

    # define question
    question = "You have come to an intersection. Do you wish to go left, or straight?"
    options = ["Left", "Straight"]

    # get user input
    answer = get_user_input(question, options)

    if (answer == "left"):
        # user chose left

        # clear the console to make it look pretty
        clear_console() 

        # print the vertical chamber
        print_vertical_chamber_with_monster()

        # define the question and answers
        question = "You have come to a room with a monster. Do you want to attempt to sneak around or fight it?"
        options = ["Sneak", "Fight","[HIDDEN]Play the flute"]
        answer = get_user_input(question, options)

        # if the answer was not "play the flute" trigger the death message
        if answer.lower() == "sneak":
            death_messge("You were unable to sneak by the ultra perceptive monster and it ate you!")
        elif answer.lower() == "fight":
            death_messge("Your strength was insufficient to defeat the monster and it sat on you!")
        elif answer.lower() == "play the flute":
            success_message("The monster falls asleep and you exit through the door behind him.")
    else:
        # if the user chose straight

        # clear the console to make it look pretty
        clear_console()

        # print the trapped room to the console
        print_horizontal_chamber_with_trap()

        # define our question and answers
        question = "You have come to a seemingly empty chamber. What do you do?"
        options = ["Walk through", "Walk around the edge", "Go back"]
        answer = get_user_input(question, options)

        # if the answer is go back display new options
        if answer.lower() == "go back":
            # clear the console to make it look pretty
            clear_console()

            # print the chamber with the trap again
            print_horizontal_chamber_with_trap(True)

            # define our question and answers
            question = "The door slams shut! What do you do?"
            options = ["Walk through", "Walk around the edge"]
            answer = get_user_input(question, options)

            # if the answer is walk through trigger the death sequence
            if answer.lower() == "walk through":
                death_messge("You walked straight into a trap and got impaled!")
            # if the answer is walk around the edge display the next chamber
            else:
                # clear the console to make it pretty
                clear_console()

                # print the final chamber
                print_horizontal_chamber_with_chest()

                # define our question and get input
                question = "You see a treasure in the center of the room. What do you do?"
                options = ["Take it", "Leave"]
                answer = get_user_input(question, options)

                # if the answer is "take it" trigger the death message
                if answer.lower() == "take it":
                    death_messge("You shouldn't have been so greedy!")
                # if the user left display the success message
                else:
                    success_message("Because of your honesty a figure appears gifting you a sword and leading you out of the dungeon!")
        # if the user chose to walk through the room trigger the death sequence
        elif answer.lower() == "walk through":
            death_messge("You walked straight into a trap and got impaled!")
        # if the user chose to go around the edge print the final room
        else:
            # clear the console to make it look pretty
            clear_console()

            # print the final room
            print_horizontal_chamber_with_chest()

            # define our question and get input
            question = "You see a treasure in the center of the room. What do you do?"
            options = ["Take it", "Leave"]
            answer = get_user_input(question, options)

            # if the answer is "take it" trigger the death message
            if answer.lower() == "take it":
                death_messge("You shouldn't have been so greedy!")
            # if the user left display the success message
            else:
                success_message("Because of your honesty a figure appears gifting you a sword and leading you out of the dungeon!")
            
# trigger the first run through of the game
game()

# -----------------------------------------------------------
# End Game


#                       -----> [ Hidden ] ------> play the flute
#                       |
# start ------> Left --------> Sneak -----> Death
#        |              |                     ↑
#        |              -----> Fight ---------|--------------------------------------------------------------------
#        |                                        |                        |                                      |
#        -----> straight --------> Walk Through --|       -----> Take it ---                                      |
#                           |                             |                                                       |
#                           -----> Walk Around The Edge -------> Leave it ---------> Win                          |
#                           |                                                                                     |
#                           -----> Go Back -----> Door Closes -----> Walk Through ---> Death    ------> Take it ---
#                                                              |                                | 
#                                                              ----> Walk Around The Edge ------------> Leave it -----> Win