# README

**Develop and Describe an algorithmic solution for an application that utilises two way communication over a network.**

The application is an autocorrect and autocomplete system for the terminal using python. It can be broken down into three main 
utilities to achieve this. 

    1. The ability for the user to utilise the terminal like bash.
    2. The ability for the user to have their typed text be automatically corrected as they type in the terminal
    3. The ability for the user to be presented with autocomplete suggestions that they can cycle through

All of the above features require that the terminal reads user input as they type, rather then pressing enter for the request to be processed.

**Solution 1**: 
To recereate the terminal in the image of bash, I utilised ANSI Escape Commands and set the terminal to raw.
This allows the application to read the user input one character at a time and process the request.
Upon a regular character being entered (alphanumeric), it will, like any text editor, display that character and move the cursor to the correct position.
Once the user presses Enter, it will create a subprocess using bash to run the command and display the stderr and stdout to the terminal screen.
This facilitates autcomplete and autocorrect as python will then be able to run code based on a single keyboard input.

There is a class named AnsiCommand that will have instance varaibles that track the relevent information to achieve this.
Each instance of the class is a command in the terminal, pressing enter will create a new instance of the class.

Required python dependencies:


**Solution 2**:
The 