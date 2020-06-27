#
# A simple Python server and an Elixir client sending to it
# Python server will reply with its own Pid, so then you know the Pid and can
# send to it directly (second send call).
#

import logging

from term import Atom
from pyrlang.gen_server import GenServer
from pyrlang import Node, Process
#from pyrlang import GeventEngine as Engine
from pyrlang import AsyncioEngine as Engine

LOG = logging.getLogger("+++EXAMPLE+++")
logging.getLogger("").setLevel(logging.DEBUG)
ch = logging.StreamHandler()
LOG.addHandler(ch)

class MyProcess(GenServer):
    def __init__(self, node) -> None:
        GenServer.__init__(self,
                           accepted_calls=['hello', 'hello2', 'hello_again', 'do_crash', 'self_crash'])

        node.register_name(self, Atom('my_process'))
        LOG.info("registering process - 'my_process'")

    def handle_info(self, msg):
        if type(msg) == tuple:
            print("handle_info: ", msg)
        else:
            if msg.decode('utf-8') == "do_crash":
                raise Exception("unknown error")
            print("handle_info: ", msg.decode('utf-8'))

    def hello(self):
        """ This is called via ``gen_server:call`` """
        LOG.debug("handle call with no params")
        return self.pid_

    def hello2(self, param1):
        """ This is called via ``gen_server:call`` """
        LOG.debug("handle call with params: " + str(param1))
        return self.pid_

    def self_crash(self):
        """ This is called via ``gen_server:call`` """
        LOG.debug(str(self))
        raise Exception("unknown error")

    def exit(self, reason=None):
        LOG.info("MyProcess: Received EXIT(%s)" % reason)
        #node = self.get_node()

        Process.exit(self, reason)

    @staticmethod
    def hello_again():
        """ This is called from Elixir test after ``hello`` returned success. """
        return b'Approved!'

    @staticmethod
    def do_crash():
        """ This is called from Elixir test after ``hello`` returned success. """
        #raise Exception("unknown error")
        1/0
        #return b'Crashed!'


def remote_receiver_name():
    return Atom('test@127.0.0.1'), Atom("py_proxy")

def main():
    event_engine = Engine()
    node = Node(node_name="py@127.0.0.1", cookie="COOKIE", engine=event_engine)

    proc = MyProcess(node)

    def task():
        node.send(sender=proc.pid_,
                         receiver=remote_receiver_name(),
                         message=(Atom("py_proxy"),
                                  Atom("init_link"),
                                  proc.pid_))

    task()

    event_engine.run_forever()


if __name__ == "__main__":
    main()