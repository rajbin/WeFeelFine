from enums import Enums
import re
from Feeling import Feeling

def displayOption():    
    age = 0
    gender = -1

    strGender = raw_input("Enter your gender, <enter for none>: ").strip()
    try:
        # default age =  1
        age = int(raw_input("Enter your age, <enter for none>: ") or 1)
        if age < 1:
            raise ValueError
    except ValueError:
        print("\nPlease enter correct age.\n")
        return displayOption()

    city = raw_input("Enter your city, <enter for none>: ").strip()

    searchWord = raw_input("""\nWe'll use the top 25 feelings, but if you want to add some, 
type in a comma separated list.\n
Extra feelings (comma separated, <enter> for none): """).strip()

    if re.match("\\bmale\\b", strGender, re.IGNORECASE) != None:
        gender = Enums.Gender._male
    elif re.match("\\bfemale\\b", strGender, re.IGNORECASE) != None:
        gender = Enums.Gender._female

    # calculate the age group: (20 - 29 = 20). Age group 1-19 are considered in age group 10
    if age > 0 and age < 10 :
        age = 10
    else:
        age = age / 10 * 10
    
    dictFoundFeelingCount = Feeling(gender, age, city).findFeelingWordInTheSentence(searchWord)
    displayFoundFeelingWithCount(dictFoundFeelingCount)


# Display feelings and it's corresponding frequencies, if available
def displayFoundFeelingWithCount(dictFoundFeelingCount):
    foundFeelingCount = len(dictFoundFeelingCount)
    print ("\nWe found {0} matching feelings.\n".format(foundFeelingCount))
    if foundFeelingCount == 0 :
        return
    print "Feeling : Frequency\n"
    for feeling in dictFoundFeelingCount.items():        
        print "{0} : {1}\n".format(feeling[0], feeling[1])

        
if __name__ == "__main__":
    displayOption()