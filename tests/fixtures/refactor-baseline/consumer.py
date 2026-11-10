from service import MessageService

def welcome(actor, name):
    return MessageService().greet(actor, name)
