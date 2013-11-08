#!/usr/bin/python
# Copyright(C) 2012 Open Information Security Foundation

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import simplejson as json
import re
import readline
from socket import socket, AF_UNIX, error
from time import sleep
import sys

SURICATASC_VERSION = "0.9"

VERSION = "0.1"
SIZE = 4096

class SuricataException(Exception):
    """
    Generic class for suricatasc exception
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class SuricataNetException(SuricataException):
    """
    Exception raised when network error occur.
    """
    pass

class SuricataCommandException(SuricataException):
    """
    Exception raised when command is not correct.
    """
    pass

class SuricataReturnException(SuricataException):
    """
    Exception raised when return message is not correct.
    """
    pass


class SuricataCompleter:
    def __init__(self, words):
        self.words = words
        self.generator = None

    def complete(self, text):
        for word in self.words:
            if word.startswith(text):
                yield word

    def __call__(self, text, state):
        if state == 0:
            self.generator = self.complete(text)
        try:
            return self.generator.next()
        except StopIteration:
            return None
        return None

class SuricataSC:
    def __init__(self, sck_path, verbose=False):
        self.cmd_list=['shutdown','quit','pcap-file','pcap-file-number','pcap-file-list','iface-list','iface-stat']
        self.sck_path = sck_path
        self.verbose = verbose

    def json_recv(self):
        cmdret = None
        i = 0
        data = ""
        while i < 5:
            i += 1
            data += self.socket.recv(SIZE)
            try:
                cmdret = json.loads(data)
                break
            except json.decoder.JSONDecodeError:
                sleep(0.3)
        return cmdret

    def send_command(self, command, arguments = None):
        if command not in self.cmd_list and command != 'command-list':
            raise SuricataCommandException("No such command: %s", command)

        cmdmsg = {}
        cmdmsg['command'] = command
        if (arguments != None):
            cmdmsg['arguments'] = arguments
        if self.verbose:
            print "SND: " + json.dumps(cmdmsg)
        self.socket.send(json.dumps(cmdmsg))
        cmdret = self.json_recv()

        if cmdret == None:
            raise SuricataReturnException("Unable to get message from server")

        if self.verbose:
            print "RCV: "+ json.dumps(cmdret)

        return cmdret

    def connect(self):
        try:
            self.socket = socket(AF_UNIX)
            self.socket.connect(self.sck_path)
        except error, err:
            raise SuricataNetException(err)

        self.socket.settimeout(10)
        #send version
        if self.verbose:
            print "SND: " + json.dumps({"version": VERSION})
        self.socket.send(json.dumps({"version": VERSION}))

        # get return
        cmdret = self.json_recv()

        if cmdret == None:
            raise SuricataReturnException("Unable to get message from server")

        if self.verbose:
            print "RCV: "+ json.dumps(cmdret)

        if cmdret["return"] == "NOK":
            raise SuricataReturnException("Error: %s" % (cmdret["message"]))

        cmdret = self.send_command("command-list")

        # we silently ignore NOK as this means server is old
        if cmdret["return"] == "OK":
            self.cmd_list = cmdret["message"]["commands"]
            self.cmd_list.append("quit")


    def close(self):
        self.socket.close()

    def interactive(self):
        print "Command list: " + ", ".join(self.cmd_list)
        try:
            readline.set_completer(SuricataCompleter(self.cmd_list))
            readline.set_completer_delims(";")
            readline.parse_and_bind('tab: complete')
            while True:
                command = raw_input(">>> ").strip()
                arguments = None
                if command.split(' ', 2)[0] in self.cmd_list:
                    if command == "quit":
                        break;
                    if "pcap-file " in command:
                        try:
                            [cmd, filename, output] = command.split(' ', 2)
                        except:
                            print "Error: arguments to command '%s' is missing" % (command)
                            continue
                        if cmd != "pcap-file":
                            print "Error: invalid command '%s'" % (command)
                            continue
                        else:
                            arguments = {}
                            arguments["filename"] = filename
                            arguments["output-dir"] = output
                    elif "iface-stat" in command:
                        try:
                            [cmd, iface] = command.split(' ', 1)
                        except:
                            print "Error: unable to split command '%s'" % (command)
                            continue
                        if cmd != "iface-stat":
                            print "Error: invalid command '%s'" % (command)
                            continue
                        else:
                            arguments = {}
                            arguments["iface"] = iface
                    elif "conf-get" in command:
                        try:
                            [cmd, variable] = command.split(' ', 1)
                        except:
                            print "Error: unable to split command '%s'" % (command)
                            continue
                        if cmd != "conf-get":
                            print "Error: invalid command '%s'" % (command)
                            continue
                        else:
                            arguments = {}
                            arguments["variable"] = variable
                    else:
                        cmd = command
                else:
                    print "Error: unknown command '%s'" % (command)
                    continue

                cmdret = self.send_command(cmd, arguments)
                #decode json message
                if cmdret["return"] == "NOK":
                    print "Error:"
                    print json.dumps(cmdret["message"], sort_keys=True, indent=4, separators=(',', ': '))
                else:
                    print "Success:"
                    print json.dumps(cmdret["message"], sort_keys=True, indent=4, separators=(',', ': '))
        except KeyboardInterrupt:
            print "[!] Interrupted"
