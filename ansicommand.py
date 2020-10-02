import sys               
import tty              
import termios         
import os               
import subprocess 
import getpass
import re
from auto_complete_trie import TrieNode, PrefixTree
from spellcheck import spellcheck_API
import config



# class to implement ANSI escape characters to interact with the terminal 
class AnsiCommand:
    """ Class that will will record the stdinput one character at a time 
    and process that to allow maniulation of the terminal 
    """
    
    autocorrect_status = True                                                                           # Determines if autocorrect feature is turned on or off

    def __init__(self, text='', index=0, ansi_character=0):
        """ Method to initialise the AnsiCommand class
        with variables required to emulate a terminal, allow
        autocomplete and autocorrect

        """

        self.text = text                                                                                # The text being written in one command
        self.index = index                                                                              # The index to determine position of cursor
        self.ansi_character = ansi_character                                                            # The keyboard input by character
        self.total_rows, self.total_columns = os.popen('stty size', 'r').read().split()                 # The total row and columns for the terminal window
        self.cwd = os.getcwd()                                                                          # The current working directory for the PS1
        self.username = getpass.getuser()                                                               # The username for the PS1
        self.starting_row =  AnsiCommand.get_cursor_position() + 1                                      # Uses the static method to determine the row number for each command
        self.original_text = ''                                                                         # The text that is saved if an auto-correct is undone using Ctrl-Z
        self.autocomplete = PrefixTree()                                                                # Creates an auto_complete instance
        self.auto_complete_options = []                                                                 # The list of available commands for autocomplete
        self.auto_complete_index = 0                                                                    # Variable to determine which auto_complete option from the available options using up and down arrows
                                                                         

        for command in config.list_of_commands:
            self.autocomplete.insert(command)
        

    


    def print_PS1(self):
        """Method that will print the PS1, emulating the bash PS1.
        Will also show if autocorrect is on or off
        """
        
        sys.stdout.write('\033[?7h')
        if AnsiCommand.autocorrect_status == True:                                          
            print('\u001b[34m' + '$' + self.username +':' '\u001b[31m' +  self.cwd + ' ' + '\u001b[32m' + 'On' +'\u001b[0m' )
        else:
            print('\u001b[34m' + '$' + self.username +':' '\u001b[31m' +  self.cwd + ' ' + '\u001b[33m' + 'Off' +'\u001b[0m' )
        

    def change_directory(self):
        """Method that will change the directory by using regex to determine if the command 
         starts with cd. It will also determine if it is an absolute or relative path being used.
         If changing the directory is successful, it will save the command into the auto_complete trie.

        """

        sys.stdout.write('\u001b[1000D')                                                # Sets the cursor to the very left
        sys.stdout.write("\u001b[0J")                                                   # Clears the screen from the cursor to the end of the terminal
        if re.search("^cd ", self.text):
            try:
                cd_path = re.search("(^cd)(.+)", self.text).groups()[1].strip()
                if cd_path[0] == '/':
                    os.chdir(cd_path)
                else:
                    os.chdir(self.cwd + '/' + cd_path)
                self.insert_into_trie()
                
                os.system('stty sane')                                                  # Resets the terminal to normal so stdout or stderror can be displayed correctly
                
            except FileNotFoundError:
                os.system('stty sane')
                print("Directory Not Found")
            except IndexError:
                os.system('stty sane')
                print("Please specify a directory")
            return True
        return False

    def enter_command(self):
        """Method that will read the command and create a subprocess to pass to bash to execute.
         Timout implemented on the child subprocess if command doesn't end naturally in 3 seconds. 
         If command is successful, save the command in autocomplete.
         Determines if successful by the return code.
        """
        sys.stdout.write("\u001b[0J")
        proc = subprocess.Popen(['/bin/bash'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, universal_newlines=True)
        os.system('stty sane')                                          
        try:
            result = proc.communicate(self.text, timeout=3)
            if proc.returncode == 0:
                sys.stdout.write(result[0])
                self.insert_into_trie()
            else:
                print(result[1], end='')
        except subprocess.TimeoutExpired:
            proc.kill()                                                                                                   # As per python documentation, to kill subprocesses that timeout.
            sys.stdout.write("Only commands that end naturally can be run (will have a work around in due course)\n")

        

        
        

    def insert_into_trie(self):
        """Method that will insert a successful command into the autocomplete trie
         Will first ensure that command isn't already in the trie.
        """
        if self.autocomplete.search_trie(self.text) == False:
            config.list_of_commands.append(self.text)
            self.autocomplete.insert(self.text)

    def cli_action(self):
        """Method that will read the stdin of the keyboard and determine an action
        """
        if self.ansi_character in {10, 13}:
            """If the stdinp is [ENTER] which is 10 or 13, change the directory or run
             the command using subprocess.
            """
            
            if self.change_directory():
                return True   
            else:
                self.enter_command()
                return True
            

        elif self.ansi_character == 3: 
            """If the user presses Control-C, to save all the commands into the autocomplete text
             file, reset the terminal and exit the program.
            """
            PrefixTree.save_command()
            os.system('stty sane')
            sys.exit()

        elif self.ansi_character == 26: #control Z   
            """If the user presses Control-Z, to undo an auto-correct.
            """         
            if self.original_text != '':
                self.index += len(self.original_text + ' ') - len(self.text) 
                self.text = self.original_text + ' '
                

        elif 32 <= self.ansi_character <= 126:
            """If a regular text input is entered, add to character self.text and 
             add to the index to move the cursor.
            """

            if chr(self.ansi_character) == ' ' and AnsiCommand.autocorrect_status == True:
                """If the client presses space, check if the last word is in
                 the dictionary, if it isn't, send API request to Bing Autocorrect
                """
                
                check_word = self.text
                if self.original_text != '':
                    check_word = check_word[len(self.original_text)-1:]                 # Will make sure not to send words that have been corrected and undone by the user to be autocorrected again
                spell_check = spellcheck_API(check_word)
                if not spell_check.check_dictionary():
                    try:
                        auto_corrected_word = spell_check.get_spellcheck()
                        if auto_corrected_word == False:                                # If the return value is false, an error has been raised so turn off autofeature
                            AnsiCommand.autocorrect_status = False
                            return
                    except KeyError:
                        return


                    if len(auto_corrected_word) > 0:                                    # Updates the index if the autocorrected word has a different length to the orginal word
                        self.original_text = self.text
                        self.text = self.text.replace(check_word, auto_corrected_word)
                        self.index += len(auto_corrected_word) - len(check_word)

            
                
            self.text = self.text[:self.index] + chr(self.ansi_character) + self.text[self.index:]    # Adds the character to the text and updates the index
            self.index += 1
            

            

        elif self.ansi_character == 27:  
            """If the user presses one of the arrow keys, to change index (left, right)
             or to cycle through available autocomplete suggestions (up, down)
            """
            next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
            if next1 == 91:
                if next2 == 68:                                             # left arrow
                    self.index = max(0, self.index-1)                                                   
                elif next2 == 67:                                           # Right arrow
                    self.index = min(len(self.text), self.index + 1)
                elif next2 == 65:                                           # Up arrow
                    self.auto_complete_index += 1
                elif next2 == 66:                                           # Down arrow
                    self.auto_complete_index -= 1

        elif self.ansi_character == 127: 
            """If client presses backspace, to remove the preceding character
             from the text depending on where the cursor is and to then
             move the cursor position left by one. 
            """     
            if self.index > 0:
                self.text = self.text[:self.index-1] + self.text[self.index:]
                self.index -= 1


        elif self.ansi_character == 9: 
            """If the user presses Tab and there is an available autocomplete
             suggestion, it will make the autosuggestion the text.
            """
            if len(self.auto_complete_suggestions()) > 0:
                self.index += len(self.auto_complete_suggestions()) - len(self.text)
                self.text = self.auto_complete_suggestions()
        

        elif self.ansi_character == 15:
            """ Will turn autocorrect feature on and off 
            by pressing Control O.
            """
            if AnsiCommand.autocorrect_status == True:
                AnsiCommand.autocorrect_status = False
            else:
                 AnsiCommand.autocorrect_status = True
                

        
    def auto_complete_suggestions(self):
        """Generates a list of available autocomplete suggestions based on the text that has been typed.
        Uses the autocomplete index to detemine which suggestion to highlight.
        """
        self.auto_complete_options = self.autocomplete.auto_complete(self.text) 
        if len(self.auto_complete_options) > 0: 
            self.auto_complete_index =  self.auto_complete_index % len(self.auto_complete_options)
            return self.auto_complete_options[self.auto_complete_index]
        else:
            return ''
    
    


    def print_to_cli(self):
            """Method that after every input will display the text, move the cursor
            to the right position and clear the screen as needed.
            """
            
           
            sys.stdout.write('\u001b[' + str(self.starting_row) + ';1H')                # Returns the cursor the starting row and then clears the entire terminal below it
            sys.stdout.write('\u001b[1000D')  
            sys.stdout.write("\u001b[0J")
            
            auto_complete_to_write = self.auto_complete_suggestions()                   # Obtains the available autocomplete suggestions
            
            if self.text != auto_complete_to_write:                     
                sys.stdout.write(self.text + '' + '\u001b[33m' + auto_complete_to_write[len(self.text):] + '\u001b[0m')     # Writes the text and the autocomplete suggestion if available
            else:
                sys.stdout.write(self.text)

            
           
            sys.stdout.write('\u001b[' + str(self.starting_row) + ';1H')                  # Moves the cursor back to the starting position
            sys.stdout.write('\u001b[1000D')
            
            


             #places the curser at the correct index
            if self.index > 0:   
                sys.stdout.write("\u001b[" + str(self.index%int(self.total_columns)) + "C")     # moves cursor the index (correct column position)
            
            if self.index > int(self.total_columns):
                sys.stdout.write("\u001b[" + str((self.index)//int(self.total_columns)) + "B")  # moves cursor to the index  (correct row position)
            
            sys.stdout.flush()                                                                  # Flushes all the above commands from the buffer to be visible on the terminal


    @classmethod
    def get_cursor_position(cli):
        """Static method to obtain the cursor row position. Allows correct placement of the cursor to clear
        the terminal. The Ansi Command ESC[6n will print the cursor position, the method
        reads the result and using regex obtain the row number.
        """

        buf = ""
        stdin = sys.stdin.fileno()
        tattr = termios.tcgetattr(stdin)

        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            sys.stdout.write("\x1b[6n")                             # Command to get cursor position in ANSI
            sys.stdout.flush()

            while True:
                buf += sys.stdin.read(1)
                if buf[-1] == "R":
                    break

        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, tattr)

        
        try:
            matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)         # Prevents errors where as it reads the cursor position, user types over the command.
            groups = matches.groups()
        except AttributeError:
            return None
        

        return int(groups[0])