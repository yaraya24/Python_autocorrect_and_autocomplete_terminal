from ansicommand import AnsiCommand
from auto_complete_trie import TrieNode, PrefixTree
import config
import sys, tty, os

def main():
    config.files_location = os.getcwd()
    config.list_of_commands = PrefixTree.read_all_commands()
    
    print(config.files_location)
    print(config.list_of_commands)
    while True:
        cli_command = AnsiCommand('', 0, 0)
        cli_command.print_PS1()

        while True:
            tty.setraw(sys.stdin)
            cli_command.ansi_character = ord(sys.stdin.read(1))


            if cli_command.cli_action():
                break
            cli_command.print_to_cli()
            



main()