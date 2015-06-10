import urllib2
import contextlib
import re

class Feeling(object):
    """Find a word in the list of sentences"""

    __apiUrl = "http://api.wefeelfine.org:8080/ShowFeelings?display=text&returnfields=sentence&limit=1500"
    __apiFeelingUrl = "http://www.wefeelfine.org/data/files/feelings.txt"
    
    # private objects
    _dictFeelings = {}
    _lstFeelingSentences = []

    def __init__(self, *args, **kwargs):
        self._gender = args[0]
        self._age = args[1]
        self._city = args[2]

    # Retrieve all the sentences from the api based on gender, age and city and put it in a list
    def _getFeelingSentences(self):
        url = self.__apiUrl
        if self._gender == 0 or self._gender == 1:
            url += "&gender={0}".format(self._gender)
        if self._age > 0:
            url += "&agerange={0}".format(self._age)
        if self._city != "":
            url += "&city={0}".format(self._city)
        try:
            response = urllib2.urlopen(url)
            content = response.read()
            content = content.strip()
            self._lstFeelingSentences = content.split("<br>")
        except IOError:
            print "An error occured while retrieving data."
        finally:
            response.close()
        
        # remove whitespaces from each sentence
        for index, feeling in enumerate(self._lstFeelingSentences):
            self._lstFeelingSentences[index] = str(feeling).strip()
        return self._lstFeelingSentences

    # Get the top 25 feelings and its frequencies from the list provided by the api
    def _getFeelings(self):
        try:
            response = urllib2.urlopen(self.__apiFeelingUrl).read()
            lstFeelings = response.split("\n")
            for index, feeling in enumerate(lstFeelings):
                # get only top 25 feelings from the list
                if index > 24:
                    break
                lstFeelingDetails = feeling.split("\t")
                # key = feeling
                key = lstFeelingDetails[0]
                # value = count of the feeling in the list provided by the api
                self._dictFeelings[key] = int(lstFeelingDetails[1])
                        
        except IndexError, IOError:
            pass
        return self._dictFeelings
    
    # Find all the feeling word in the list of sentences and count it's frequency
    def findFeelingWordInTheSentence(self, searchWord=""): 
        self._getFeelingSentences()
        self._getFeelings()
        dictFoundFeelingCount = {}
        count = 0
        
        # if dictionary of feelings does not have any value then return empty dictionary
        if len(self._dictFeelings) == 0:
            return dictFoundFeelingCount

        # append user entered feelings into the dictionary as key and value = 0
        if searchWord != "":
            for word in searchWord.split(","):
                word = word.strip()
                if not word.isspace() and word != "":
                    self._dictFeelings[word] = 0
        
        # search for each feeling in the list of sentences and increment the count by 1 when found and insert it into a dictionary
        for feeling in self._dictFeelings.keys():
            for sentence in self._lstFeelingSentences:
                if re.search("\\b" + feeling + "\\b", sentence, re.IGNORECASE) != None:
                    count += 1
                    dictFoundFeelingCount[feeling] = count
            else:
                # reset count = 0, after searching for a key in all the sentences
                count = 0

        return dictFoundFeelingCount