import requests
import json
import config

class spellcheck_API:
    """ Class that will check if a word is correctly spelt, and if it isn't, to send
    an API request to Bing to get an autocorrect suggestion.
    """

    api_key = '26c4fd8d2a5346b5b7a415ff230de4ca'                                            # a key to use the Bing Autocorrect service
    endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/SpellCheck"                   #The address that the POST request is sent to
    params = {'mkt':'en-AU','mode':'proof'}                                                 # As per API documentation, need to provide the location (en-AU) and the mode (spell or proof)
    headers = {'Content-Type': 'application/x-www-form-urlencoded','Ocp-Apim-Subscription-Key': api_key} 

    def __init__(self, word_to_check): 
        """initalise an instance of the class and every instance reqiures the word 
        that needs to be checked"""
        self.word_to_check = word_to_check

    def check_dictionary(self):
        """Instance method that will read from a dictionary text file and if it is found, 
        return True so that autocorrect is not requried (speeds up the program as doesn't have to wait on API after every word)
        """
        try:
            if self.word_to_check.split()[-1] in config.dictionary_list: 
                return True
        except IndexError:          # Due to the way undo works after an autocorrect that isn't wanted, sometimes an empty string will be provided. Thus to return True and not to continue with Autocorrect
            return True

 
    def get_spellcheck(self):   
        """Instance method to send a POST reuest with the required parameters and the word_to_check 
        """
        try:
            data = {'text': self.word_to_check}
            response = requests.post(spellcheck_API.endpoint, headers=spellcheck_API.headers, params=spellcheck_API.params, data=data)
            spell_check_API_response= response.json()

            final_corrected_word = ''
            for i in spell_check_API_response['flaggedTokens']: 
                """ As per the JSON returned, the loop will go through all of the suggestions and 
                replace the word_to_check with the auto corrected words.
                """

                provided_word = i['token']
                corrected_word_response = i['suggestions'][0]['suggestion']
                final_corrected_word = self.word_to_check
                final_corrected_word = self.word_to_check.replace(provided_word, corrected_word_response)
                self.word_to_check = final_corrected_word   

            return final_corrected_word
        except:                                  
            return False                     # Turns off auto correct if there are any errors, mainly no internet connection


    @staticmethod 
    def read_dictionary_text():
        """A static method that will read from the dictionary file - used in the check_dictionary method. 
        Using config.py so that it the dictionary doesn't have to be opened and read into a list at 
        every instance of the class, just once when the program is first run.
        """
        with open(config.files_location +'files/dictionary.txt', 'r') as reader: # At every initialisation of the class, it will read
            dictionary_list = reader.read().splitlines()
        return dictionary_list

