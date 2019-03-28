
"""A set of libraries that are useful to both the proxy and regular servers."""

#Testing github connection

# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# The Python socket API is based closely on the Berkeley sockets API which
# was originally written for the C programming language.
#
# https://en.wikipedia.org/wiki/Berkeley_sockets
#
# The API is more flexible than you need, and it does some quirky things to
# provide that flexibility. I recommend tutorials instead of complete
# descriptions because those can skip the archaic bits. (The API was released
# more than 35 years ago!)
import socket

import time

# Read this many bytes at a time of a command. Each socket holds a buffer of
# data that comes in. If the buffer fills up before you can read it then TCP
# will slow down transmission so you can keep up. We expect that most commands
# will be shorter than this.
COMMAND_BUFFER_SIZE = 256




def CreateServerSocket(port):
# Creates a socket that listens on a specified port.
#
#   Args:
#     port: int from 0 to 2^16. Low numbered ports have defined purposes. Almost
#         all predefined ports represent insecure protocols that have died out.
#   Returns:
#     An socket that implements TCP/IP.
    Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server_Socket.bind(('', port)) #bind host address and port together
    Server_Socket.listen(1) #how many clients server can listen to at once
    print("Waiting for client connection")
    return Server_Socket

def ConnectClientToServer(server_sock, port):
# Wait until a client connects and then get a socket that connects to the
# client.
    clientSocket, address = server_sock.accept()
    return clientSocket, (address, port)

def CreateClientSocket(server_addr, port):
#Create a socket that connects to a port on a server.
    Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client_Socket.connect((server_addr, port))
    return clientSocket


def ReadCommand(clientSocket):
# Read a single command from a socket. The command must end in newline.
    D = clientSocket.recv(COMMAND_BUFFER_SIZE)
    return D

def ParseCommand(command):

 #Parses a command and returns the command name, first arg, and remainder.

 #All commands are of the form:
#COMMAND arg1 remaining text is called remainder
 #Spaces separate the sections, but the remainder can contain additional spaces.
 #The returned values are strings if the values are present or `None`. Trailing
  #whitespace is removed.

 #Args:
#command: string command.
  #Returns:
  #command, arg1, remainder. Each of these can be None.


  args = command.strip().split(' ')
  command = None
  if args:
    command = args[0]
  arg1 = None
  if len(args) > 1:
    arg1 = args[1]
  remainder = None
  if len(args) > 2:
    remainder = ' '.join(args[2:])
  return command, arg1, remainder


class KeyValueStore(object):

 #A dictionary of strings keyed by strings.

  #The values can time out once they get sufficiently old. Otherwise, this
  #acts much like a dictionary.



  def __init__(self):
    self.store = {}

  def GetValue(self, key, max_age_in_sec=None):

#Gets a cached value or `None`.

#Values older than `max_age_in_sec` seconds are not returned.

#Args:
     #key: string. The name of the key to get.
      #max_age_in_sec: float. Maximum time since the value was placed in the
    #KeyValueStore. If not specified then values do not time out.
    #Returns:
      #None or the value.


    if key in self.store.keys():
        Age = (time.time() - self.store[key][1])
        if max_age_in_sec:
            if (Age <= max_age_in_sec):
                return self.store[key][0]
            else:
                del self.store[key]
        else:
            return self.store[key][0]

    return None

  def StoreValue(self, key, value):

 #Stores a value under a specific key.

 #Args:
 #key: string. The name of the value to store.
 #value: string. A value to store.


    self.store[key] = (value, time.time())

  def Keys(self):

# Returns a list of all keys in the datastore.

      return self.store.keys()