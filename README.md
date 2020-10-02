# README

**Develop and Describe an algorithmic solution for an application that utilises two way communication over a network.**

The application is an autocorrect and autocomplete system for the terminal using python. It can be broken down into three main 
utilities to achieve this. 

    1. The ability for the user to utilise the terminal like bash.
    2. The ability for the user to have their typed text be automatically corrected as they type in the terminal
    3. The ability for the user to be presented with autocomplete suggestions that they can cycle through

All of the above features require that the terminal reads user input as they type, rather then pressing enter for the request to be processed.

### Solution 1 - Custom Terminal: 

To recereate the terminal in the image of bash, I utilised ANSI Escape Commands and set the terminal to raw.
This allows the application to read the user input one character at a time and process the request.
Upon a regular character being entered (alphanumeric), it will, like any text editor, display that character and move the cursor to the correct position.
Once the user presses Enter, it will create a subprocess using bash to run the command and display the stderr and stdout to the terminal screen.
This facilitates autcomplete and autocorrect as python will then be able to run code based on a single keyboard input.

There is a class named AnsiCommand that will have instance varaibles that track the relevent information to achieve this.
Each instance of the class is a command in the terminal, pressing enter will create a new instance of the class.

**Required python dependencies:**

*sys:* Used to write to the terminal as stdout and read from the stdin
*tty:* Changes the terminal mode to raw to allow access to stdin and stdout
*termios:* Provides access to the terminal and read the cursor position
*os:* Allows operating system commands like reseting the terminal, change directory and obtain the current working directory
*subprocess:* Allows python to create a child process to run the commands of the custom terminal 
*getpass:*  Obtains the username for the PS1 in an effort to emulate bash
*re:* Regex used to find if the command is 'cd' and to read the cursor position


### Solution 2 - Autocorrect:

The autocorrect feature will work by being supplied a word that will be checked if it is correctly or incorrectly spelt.
The class will have access to a dictionary text file and create a list from that file. utilising linear search, a method within the
autocorrect class will determine if that word is in the dictionary. If it is in the dictionary, it will be classified as correctly
spelt and no further actions will be made. 

However, if the word is not found in the dictionary file, an API request will be sent to Bing Autocorrect and retrieve a
suggestion. An instance method will loop through the json response and update the word to be checked by replacing the incorrect
word with the autocorrected word.

Within the AnsiCommand class, the ability to undo the change will be available.

Furthermore, due to the nature of terminal commands, autocorrect may not be desired in all situations. Thus, using boolean logic,
the autocorrect feature can be turned on and off and the status is displayed in the PS1.

The autocorrect will have one class with one instance variable being the word to be checked.
One instance method to determine if the word to be checked is in the dictionary.
Another instance method to send the word to Bing as an API request and return the autocorrected
suggestion if there is one.

**Required python dependencies:**
*requests:* Allows API requests to be posted to Bing and retrieve the results
*json:* Allows the API result to be processed using Json for improved accessibility


### Solution 3 - Autocomplete:

Much like the autocorrect feature, the autocomplete system will retrieve autocomplete suggestions as the user types in the terminal.
A trie data structure has been implemented to achieve thi.

The trie utilises nodes which contain the text for that node, a dictionary which holds all child nodes and variable to determine if it is a whole word
or just a prefix.

As the user types into the terminal, the typed string will be sent to the autocomplete trie and treated as a prefix.
It will start from the root node and go character by character down the tree if there are matching nodes. If there isn't a node for that particular
sequence of characters, the autocomplete feature will return an empty list.

However, if for a given preifx there are complete words, it will return a list of available autocomplete suggestions.

There are two classes for this solution, a node class which is created everytime a command or word inserted into the trie. 
The other class which is the actual trie data structure, will obtain the prefix as input and search the whole data structure for
corresponding commands that match that prefix.

