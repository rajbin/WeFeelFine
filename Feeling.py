import urllib2
import contextlib
import re

class Feeling(object):
    """Find a word in the list of sentences"""

    __apiUrl = "http://api.wefeelfine.org:8080/ShowFeelings?display=text&returnfields=sentence&limit=1500"
    __apiFeelingUrl = "http://www.wefeelfine.org/data/files/feelings.txt"
    _dictFeelings = {}
    _lstFeelingSentences = []

    def __init__(self, *args, **kwargs):
        self._gender = args[0]
        self._age = args[1]
        self._city = args[2]

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
            print "An error occured."
        finally:
            response.close()

        for index, feeling in enumerate(self._lstFeelingSentences):
            self._lstFeelingSentences[index] = str(feeling).strip()
        return self._lstFeelingSentences

    def _getFeelings(self):
        try:
            response = urllib2.urlopen(self.__apiFeelingUrl).read()
            lstFeelings = response.split("\n")
            for index, feeling in enumerate(lstFeelings):
                if index > 24:
                    break
                lstFeelingDetails = feeling.split("\t")
                key = lstFeelingDetails[0]
                self._dictFeelings[key] = int(lstFeelingDetails[1])
                        
        except IndexError, IOError:
            pass
        return self._dictFeelings

    def findFeelingWordInTheSentence(self, searchWord=""): 
        self._getFeelingSentences()
        self._getFeelings()
        dictFoundFeelingCount = {}
        count = 0

        if searchWord != "":
            for word in searchWord.split(","):
                word = word.strip()
                if not word.isspace() and word != "":
                    self._dictFeelings[word] = 0

        for feeling in self._dictFeelings.keys():
            for sentence in self._lstFeelingSentences:
                if re.search("\\b" + feeling + "\\b", sentence, re.IGNORECASE) != None:
                    count += 1
                    dictFoundFeelingCount[feeling] = count
                    #print "{0} found".format(feeling)
            else:
                count = 0

        return dictFoundFeelingCount