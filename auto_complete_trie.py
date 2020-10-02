import config


class TrieNode:
    """ Class that initialises a node for the trie
    text that tracks the prefix provided, the children of each node which is a dictionary
    and variable that is True or False depending on whether it is a full command rather than just a prefix
    """
    def __init__(self, text=''):
        self.text = text
        self.children = dict()
        self.is_word = False  

class PrefixTree:
    """ The actual trie data structure initalises a node which is always the root. Instance methods
    will then be used to go down from the root node to find a word based on the prefix.
    """
    
    def __init__(self):
        self.root = TrieNode() 
        


    def insert(self, word): 
        """ The insert method will use the word provided to insert it into the trie data structure.
        The method will loop through the word and if there is no node for particular prefix, it wil create one.
        If the various prefix of the word is already in the trie, no further nodes will be created.
        Once it has looped over the whole word, it will set the last child's node to be True to advise it is a full word and not just a prefix.
        """
        current_node = self.root 
        for count, char in enumerate(word): 
            if char not in current_node.children: 
                prefix = word[0:count+1] 
                current_node.children[char] = TrieNode(prefix)
            current_node = current_node.children[char]
        current_node.is_word = True


    def search_trie(self, word):
        """ The method will go loop through the word and determine if that word is within the data structure.
        If the word is not in the data structure, it will return False otherwise it will return the last node if it is a full word.
        """ 
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        
        if current_node.is_word:
            return current_node

    def auto_complete(self, prefix):
        """ The method will return a list of available words based on the prefix provided.
        If for a given prefix there are no words or commands, it will return an empty list.
        Will then use a recursive method to obtain all the valid words for a given prefix.
        """
        if len(prefix) == 0:
            return []
        commands = []
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return []
            current_node = current_node.children[char]

        self.__child_words_for(current_node, commands)
        return commands


    def __child_words_for(self, node, words):
        """ A helper function that will recursevily go down all of the child nodes for a given prefix
        and add them to a list if they are full words.
        """
        if node.is_word:
            words.append(node.text)
        for letter in node.children:
            self.__child_words_for(node.children[letter], words)

    @staticmethod
    def save_command():
        """ Static method that will save all the commands in the list_of_commands list to a text file.
        Using config.files_location to determine the absolute path due to application being able 
        to change directories.

        Note: You may not have permission to save to this file.
        """
        try:
            with open(config.files_location + 'files/autocomplete_list.txt', 'w') as write:
                for command in config.list_of_commands:
                    write.write(command + '\n')
        except PermissionError:
            print("You do not have write permission, unfortunately commands will not be saved")


    @staticmethod
    def read_all_commands():
        """ Static method that will read a file for commands that have been previously saved and return a list.
        Using config.files_location to determine the absolute path due to application being able 
        to change directories.
        """
        with open(config.files_location + 'files/autocomplete_list.txt', 'r') as reader:
            commands_list = reader.read().splitlines()
        return commands_list
