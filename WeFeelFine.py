from enums import Enums
import re
from Feeling import Feeling

def displayOption():
    
    strGender = raw_input("Enter your gender: ").strip()
    age = 0
    try:
        age = int(raw_input("Enter your age: ") or 0)
    except ValueError:
        print("\nPlease enter correct age.\n")
        return displayOption()

    city = raw_input("Enter your city: ").strip()

    searchWord = raw_input("""We'll use the top25 feelings, but if you want to add some, 
type in a comma separated list.
Extra feelings (comma separated, <enter> for none): """).strip()

    gender = -1
    if re.match("\\bmale\\b", strGender, re.IGNORECASE) != None:
        gender = Enums.Gender._male
    elif re.match("\\bfemale\\b", strGender, re.IGNORECASE) != None:
        gender = Enums.Gender._female

    if age > 0 and age < 11 :
        age = 10
    elif age > 11:
        age = age / 10 * 10
    
    dictFoundFeelingCount = Feeling(gender, age, city).findFeelingWordInTheSentence(searchWord)
    displayFoundFeelingWithCount(dictFoundFeelingCount)

def displayFoundFeelingWithCount(dictFoundFeelingCount):
    print ("\nWe found {0} matching feelings.\n".format(len(dictFoundFeelingCount)))
    if len(dictFoundFeelingCount) == 0 :
        return
    print "Feeling : Frequency\n"
    for feeling in dictFoundFeelingCount.items():        
        print "{0} : {1}\n".format(feeling[0], feeling[1])

        
if __name__ == "__main__":
    displayOption()