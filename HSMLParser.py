def CheckForIntent(search): #Function that returns whether a Intent has been found. 
    query = root.findall('intent') #Finds all the intents and saves to list
    for intent in query: #Cycles through every intent in the list
        intentName = intent.findtext('name') #Finds the name of the intent
        intentDescription = intent.findtext('description') #Finds the description of the intent
        if intentName == search: #If the name of the intent is the same of the search criteria...
            return ('Intent ', search, ' has been found with the description: ', intentDescription) #The return value is set to tell the user it has been found
    return ('Intent has not been found') # Or show the user that the Intent has not been found

def FindIntentFromTrigger(searchTrigger): #Function that returns the intent of a sentance
    query = root.findall('intent') #Finds all the intents and saves to list
    for intent in query:  #Cycles through every intent in the list
        call = intent.findall('calls')
        intentName = intent.findtext('name') #Finds the name of the current intent
        for triggers in call:  #Cycles through every call in the intent
            callwords = triggers.findall('trigger') #callwords is made as a list of attributes called triggers
            for i in callwords: #Cycles through every trigger
                currentTrigger = i.text #Finds the text inside the trigger attribute in question
                if currentTrigger == searchTrigger: #Compares the text to the text in question
                    return intentName #If they are the same the name of the intent being searched is returned
    return '404' #If not, a not found notice is returned

def FindResponseList(searchIntent, positive): #Returns a list of responces from a list
    query = root.findall('intent') #Finds all the intents and saves to list
    for intent in query: #Cycles through every intent in the list
        intentName = intent.findtext('name') #Finds the name of the intent
        if intentName == searchIntent: #If the intent name matches the Intent being searched for
            locationResponse = intent.find('response')#Find the location of the response tags 
            if positive ==  True: #if the positive parameter is True
                locationPositive = locationResponse.find('positive') #Find the posititve responses
                responsesList = locationPositive.findall('result') #Add all the positive reponses to a list
                return responsesList #Return the list
            else: #if the positive parameter is False
                locationNegative = locationResponse.find('negative')#Find the negative responses
                responsesList = locationNegative.findall('result')  #Add all the negative reponses to a list
                return responsesList #Return the list
    return '404' #Return not found if none found

def FindTags(searchIntent): #Returns a list of responces from a list
    query = root.findall('intent') #Finds all the intents and saves to list
    for intent in query: #Cycles through every intent in the list
        intentName = intent.findtext('name') #Finds the name of the intent
        if intentName == searchIntent: #If the intent name matches the Intent being searched for
            locationTags = intent.find('tags')#Find the location of the tags tags
            print locationTags
            responsesList = locationTags.findall('tag') #Add all the tags to a list
            return responsesList #Return the list
    return '404' #Return not found if none found

def IntentFromTags(CompareTags):
    query = root.findall('intent') #Finds all the intents and saves to list
    HighestScoringIntent = '404'
    HighestScore = 0
    for intent in query: #Cycles through every intent in the list
        intentName = intent.findtext('name') #Finds the name of the intent
        locationTags = intent.find('tags')#Find the location of the tags tags
        responsesList = locationTags.findall('tag') #Add all the tags to a list
        CurrentTotal = 0 #Sets a variable for the total of matches for the intent
        for tag in responsesList: #Loops to compare every word with tags from the HSML file
            for CompareTag in CompareTags:
                if tag.text == CompareTag: #If they match
                    TagStrength = int(tag.get('strength')) #ADD the strength to the current score
                    CurrentTotal = CurrentTotal + TagStrength #ADD the strength to the current score
        if CurrentTotal == HighestScore: #If the scores are the same, there is no way to distingush so a draw is called
            HighestScoringIntent = 'DRAW' #Highest scorer set to a draw
        if CurrentTotal > HighestScore: #If the score is higher than the current high score
            HighestScore = CurrentTotal #The new intent is made the HighestScorer
            HighestScoringIntent = intentName 
    return HighestScoringIntent #Return the most appropriate intent

def RandomResponse(searchIntent, positive): #Runs the FindResponseList() Function and randomly selects one
    import random #Use Pythons in-build random module
    responsesList = FindResponseList(searchIntent, positive) #Calls the function and saves result
    if responsesList == '404':
        return '404'
    else:
        lengthOfList = len(responsesList) #Find the number of responses in the list
        randomGen = random.randint(1,lengthOfList)-1 #Generates a random number
        response = responsesList[randomGen].text #Makes the Variable response equal to the random response
        return response #Returns the response

def Respond(Trigger):
    Trigger = Trigger.upper()
    intent = FindIntentFromTrigger(Trigger)
    if intent == '404':
        return '404'
    else:
        return RandomResponse(intent, True)

def TagRespond(searchTrigger):
    searchTrigger = searchTrigger.upper()
    CompareTags = searchTrigger.split(" ")
    intent = IntentFromTags(CompareTags)
    if intent == '404' or intent == 'DRAW':
        return '404'
    else:
        return RandomResponse(intent, True)

def ParseXML(ParseFile):
    import xml.etree.ElementTree as ET #Imports the needed module to parse the XML file
    tree = ET.parse(ParseFile) #Parse the file
    global root
    root = tree.getroot() #Find the root of the XML Tree

def ParserHelp():
    print '         Parser Help!'
    print '----------------------------------\n\n'
    print 'To Check Whether an Intent Exists, use the function > CheckForIntent(search, root) \n    search - STRING - intent you are checking exists \n'
    print 'To Find an Intent from a Trigger, use the function > FindIntentFromTrigger(searchTrigger, root) \n    searchTrigger - STRING - Trigger you are investigating \n'
    print '\n\n----------------------------------\n'

print 'Type ParserHelp() for Help!'

