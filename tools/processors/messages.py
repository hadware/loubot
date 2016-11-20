import random
from datetime import datetime

from .commons import *


class DispatcherBotProcessor(MessageProcessor):
    """A processor that matches a context, then forwards the message to a list of sub-processors.
    This enables the botprocessor-matching mechanism to behave kinda like a decision tree"""

    def __init__(self, processors_list : List[MessageProcessor]):
        self.dispatcher = MessageDispatcher(processors_list)

    def process(self, text : str, sender_id : str, users_list : UserList):
        return self.dispatcher.dispatch(text, sender_id, users_list)


class RandomAutoresponseBot(MessageProcessor):

    possible_responses = []

    def process(self, text: str, sender_id: str, users_list: UserList):
        return random.choice(self.possible_responses)


class MrleBot(RandomAutoresponseBot, MessageProcessor):

    possible_responses = [
        "MDR mrle ce pd", "wesh yé ou ce pd de mrle" , "yé chaud mrle", "ouee?"]

    def match(self, text : str, sender_id : str, users_list : UserList):
        return "MRLE" in text.upper()


class WeshBot(MessageProcessor):

    def match(self, text : str, sender_id : str, users_list : UserList):
        return "WESH" in text.upper()

    def process(self, text : str, sender_id : str, users_list : UserList):
        name = users_list.name(sender_id)
        return "WESH %s" % name.upper()


class CommandsDispatcherProcessor(DispatcherBotProcessor):
    """Reacts to commands of the form '/botname command' or 'botname, command' """

    def match(self, text : str, sender_id : str, users_list : UserList):
        return text.upper().startswith(users_list.my_name.upper() + ",") \
               or text.upper().startswith("/" + users_list.my_name.upper())

    def process(self, text : str, sender_id : str, users_list : UserList):
        response = super().process(text, sender_id, users_list)
        return "Commande non reconnue, pd" if response is None else response


class TimeTeller(MessageProcessor):

    def match(self, text : str, sender_id : str, users_list : UserList):
        return "quelle heure" in text.lower()

    def process(self, text : str, sender_id : str, users_list : UserList):
        return "Il est %s" % datetime.now().strftime("%I:%M%p")