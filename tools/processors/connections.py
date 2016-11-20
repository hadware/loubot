import logging
import random
from typing import List

from tools.commons import UserList
from tools.constants import PUTES_PAS_RANDOM


class ConnectProcessor:
    def match(self, sender_id: str, users_list: UserList) -> bool:
        """Returns true if this is the kind of user connection a processor should respond to"""
        pass

    def process(self, sender_id: str, users_list: UserList) -> str:
        """Processes a message and returns an answer"""
        pass


class ConnectionDispatcher:

    def __init__(self, processor_list: List[ConnectProcessor]):
        self.processor_list = processor_list

    def dispatch(self, sender_id: str, users_list: UserList) -> str:
        """Tells its first botprocessor to match the message to process this message and returns its answer"""
        for processor in self.processor_list:
            if processor.match(sender_id, users_list):
                logging.info("Matched %s" % processor.__class__.__name__)
                return processor.process(sender_id, users_list)

        return None


class PuteRandomConnect(ConnectProcessor):

    def match(self, sender_id: str, users_list: UserList):
        return users_list.name(sender_id) not in PUTES_PAS_RANDOM and random.randint(1,3) == 1

    def process(self, sender_id: str, users_list: UserList):
        return "Wesh %s t'es qui sale pute qui se la joue random?" % users_list.name(sender_id)

