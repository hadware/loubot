#!/usr/bin/env python3

import argparse
import asyncio
import html
import json
import logging

import websockets

from tools.commons import UserList
from tools.constants import DEFAULT_COOKIE, DEFAULT_CHANNEL
from tools.processors import MessageDispatcher, WeshBot, MrleBot, PdChecker, \
    CommandsDispatcherProcessor, ConnectionDispatcher
from tools.processors.connections import PuteRandomConnect


class Scorbot:

    def __init__(self, cookie : str, channel : str,
                 messages_dispatcher : MessageDispatcher,
                 connect_dispatcher : ConnectionDispatcher):

        # setting up variables required by the server. The default is a Kabutops on the main lou server, I think
        self.cookie = DEFAULT_COOKIE if cookie is None else cookie
        if args.channel is None:
            self.channel = DEFAULT_CHANNEL
        else:
            self.channel = "" if channel == "root" else channel
        self.msg_dispatch = messages_dispatcher
        self.cnt_dispatch = connect_dispatcher
        self.user_list = {}

    async def _send_message(self, websocket, message):
        if message is not None:
            data = {"lang": "fr", "msg": message, "type": "msg"}
            await websocket.send(json.dumps(data))

    async def listen(self):
        logging.info("Listening to channel %s" % self.channel)
        async with websockets.connect('wss://loult.family/socket/%s' % self.channel,
                                      extra_headers={"cookie": "id=%s" % self.cookie}) as websocket:

            while True:
                msg = await websocket.recv()
                websocket.recv()
                if type(msg) != bytes:
                    msg_data = json.loads(msg, encoding="utf-8")
                    msg_type = msg_data["type"]
                    if msg_type == "userlist":
                        self.user_list = UserList(msg_data["users"])
                        logging.info(str(self.user_list))

                    elif msg_type == "msg":
                        msg_data["msg"] = html.unescape(msg_data["msg"]) # removing HTML shitty encoding
                        logging.info("%s says : \"%s\"" % (self.user_list.name(msg_data["userid"]), msg_data["msg"]))

                        response = None
                        # dispatching the message to the processors. If there's a response, send it to the chat
                        if not self.user_list.itsme(msg_data["userid"]):
                            response = self.msg_dispatch.dispatch(msg_data["msg"], msg_data["userid"], self.user_list)

                        await self._send_message(websocket, response)

                    elif msg_type == "connect":
                        # registering the user to the user list
                        self.user_list.add_user(msg_data["userid"], msg_data["params"])
                        logging.info("%s connected" % self.user_list.name(msg_data["userid"]))
                        message = self.cnt_dispatch.dispatch(msg_data["userid"], self.user_list)
                        await self._send_message(websocket, message)

                    elif msg_type == "disconnect":
                        # removing the user from the userlist
                        logging.info("%s disconnected" % self.user_list.name(msg_data["userid"]))
                        self.user_list.del_user(msg_data["userid"])

                else:
                    logging.debug("Received sound file")

# setting up argument parser
parser = argparse.ArgumentParser(description='Le lou bot')
parser.add_argument('--cookie', type=str, help='usercookie to use')
parser.add_argument('--channel', type=str, help='channel to watch')

# setting up the various dispatchers
cmd_dispatcher_proc = CommandsDispatcherProcessor([PdChecker()])

root_messages_dispatcher = MessageDispatcher([cmd_dispatcher_proc, WeshBot(), MrleBot()])

connections_dispatcher = ConnectionDispatcher([PuteRandomConnect()])

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    args = parser.parse_args()

    screbte = Scorbot(args.cookie, args.channel, root_messages_dispatcher, connections_dispatcher)
    asyncio.get_event_loop().run_until_complete(screbte.listen())



