import logging
from typing import List

from tools.commons import UserList


class MessageProcessor:
    """Parent class for all processors. A processor is basically a bot response triggered by a condition.
    The match method returns a boolean telling if the trigger condition is verified, and the process
    method returns a string of the output message. All bot processors are to be grouped in a list then
    given to a Dispatcher"""

    def match(self, text : str, sender_id : str, users_list : UserList) -> bool:
        """Returns true if this is the kind of text a processor should respond to"""
        pass

    def process(self, text : str, sender_id : str, users_list : UserList) -> str:
        """Processes a message and returns an answer"""
        pass


class MessageDispatcher:
    """Dispatches the current input message to the first botprocessor that matches the context given
    to the dispatch method."""

    def __init__(self, processor_list : List[MessageProcessor]):
        self.processor_list = processor_list

    def dispatch(self,text : str, sender_id : str, users_list : UserList) -> str:
        """Tells its first botprocessor to match the message to process this message and returns its answer"""
        for processor in self.processor_list:
            if processor.match(text, sender_id, users_list):
                logging.info("Matched %s" % processor.__class__.__name__)
                return processor.process(text, sender_id, users_list)

        return None