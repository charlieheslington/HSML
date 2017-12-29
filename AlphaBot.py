from HSMLParser import *
print 'AlphaBot Chatbot'
FilePath = 'ResponseBase.hsml'
ParseXML(FilePath)
print 'Type "Exit" to exit the conversation'

def Conversation():
    run = True
    while run == True:
        searchTrigger = raw_input("\n>>> ")
        if searchTrigger == "Exit":
            run = False
        else:
            response = Respond(searchTrigger)
            if response == '404':
                response = TagRespond(searchTrigger)
            if response == '404':
                response = 'I do not understand this'
            print response

Conversation()

