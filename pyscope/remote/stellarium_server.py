'''StellariumServer

A lot of this is just ripped out of the circuits chatserver example
https://bitbucket.org/circuits/circuits/src/8df458d7896343703b27903d267a3df20a7c8eda/examples/chatserver.py?at=default
'''

from optparse import OptionParser
import struct

from datetime import datetime
from pytz import timezone
import pytz
from circuits.net.events import write
from circuits import Component, Event, Debugger, handler
from circuits.net.sockets import TCPServer

class StellariumServer(Component):

    channel = 'stellarium'

    CURRENT_POSITION_FORMAT = '<hhqIii'
    GOTO_FORMAT = '<hhqIi'

    def init(self, address='0.0.0.0', port=10003, debug=False):
        '''Initialize our ``StellariumServer`` Component.'''

        self.clients = {}

        if debug:
            self += Debugger()

        bind = (address, port)

        self += TCPServer(bind, channel=self.channel)

    def broadcast(self, data, exclude=None):
        exclude = exclude or []
        targets = (sock for sock in self.clients.keys() if sock not in exclude)
        for target in targets:
            self.fire(write(target, data))

    def connect(self, sock, host, port):
        '''Connect Event -- Triggered for new connecting clients'''

        self.clients[sock] = {
            'host': sock,
            'port': port
        }

    def disconnect(self, sock):
        '''Disconnect Event -- Triggered for disconnecting clients'''

        if sock not in self.clients:
            return

        del self.clients[sock]

    @handler('read')
    def on_read(self, sock, data):
        packets = [data[i:i+20] for i in range(0, len(data), 20)]
        unpacked_data = [struct.unpack(self.GOTO_FORMAT, packet) for packet in packets]
        for event_data in unpacked_data:
            slew_event = slew(event_data[3:])
            self.fire(slew_event)

    @handler('position_change')
    def on_position_change(self, ra, dec):
        length = 24
        mtype = 0
        time = self._get_time()
        ra = 0
        dec = 0
        status = 0
        to_pack = (self.CURRENT_POSITION_FORMAT, length, mtype, time, ra, dec, status)
        packed = struct.pack(*to_pack)
        self.broadcast(packed)

    def _get_time(self):
        now = datetime.now(pytz.utc)
        epoch = datetime(1970, 1, 1, tzinfo=pytz.utc)
        posix_timestamp_micros = (now - epoch)
        return posix_timestamp_micros.total_seconds()

class slew(Event):
    '''New Slew Command'''

class position_change(Event):
    '''PositionCHangeEvent'''
