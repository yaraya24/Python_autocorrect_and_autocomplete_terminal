import sys
import tty
import os 
from ansicommand import AnsiCommand 
from auto_complete_trie import TrieNode, PrefixTree 
from spellcheck import spellcheck_API
import config 


def main():
    config.files_location = os.getcwd() + '/'                       # Saves the absolute working directory to a variable in config.py
    config.list_of_commands = PrefixTree.read_all_commands()        # Saves all the autocomplete commands so its only done once 
    config.dictionary_list = spellcheck_API.read_dictionary_text()  # Saves the dictionary into a list so its only done once 
    
    while True:
        cli_command = AnsiCommand() 
        cli_command.print_PS1() 

        while True:
            tty.setraw(sys.stdin)                                   # This will set the terminal to raw so that we can access the stdin and recreate the terminal 
            cli_command.ansi_character = ord(sys.stdin.read(1))     # Reads from the stdin (keyboard) one character at a time and sends it to the ansicommand class to be processed


            if cli_command.cli_action():                            # Processes an action based on the keyboard input and if the user changes directory, to not continue with creating a subprocess
                break
            cli_command.print_to_cli()                              # Displays the terminal 
            



if __name__ == '__main__':
    main()