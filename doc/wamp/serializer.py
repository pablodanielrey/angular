###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from __future__ import absolute_import

import six
import struct

from autobahn.wamp.interfaces import IObjectSerializer, ISerializer
from autobahn.wamp.exception import ProtocolError
from autobahn.wamp.utils import serializer_loads, MySerializer
from autobahn.wamp import message

# note: __all__ must be a list here, since we dynamically
# extend it depending on availability of more serializers
__all__ = ['Serializer',
           'JsonObjectSerializer',
           'JsonSerializer']


class Serializer(object):
    """
    Base class for WAMP serializers. A WAMP serializer is the core glue between
    parsed WAMP message objects and the bytes on wire (the transport).
    """

    # WAMP defines the following 24 message types
    MESSAGE_TYPE_MAP = {
        message.Hello.MESSAGE_TYPE: message.Hello,
        message.Welcome.MESSAGE_TYPE: message.Welcome,
        message.Abort.MESSAGE_TYPE: message.Abort,
        message.Challenge.MESSAGE_TYPE: message.Challenge,
        message.Authenticate.MESSAGE_TYPE: message.Authenticate,
        message.Goodbye.MESSAGE_TYPE: message.Goodbye,
        message.Error.MESSAGE_TYPE: message.Error,
        message.Publish.MESSAGE_TYPE: message.Publish,
        message.Published.MESSAGE_TYPE: message.Published,
        message.Subscribe.MESSAGE_TYPE: message.Subscribe,
        message.Subscribed.MESSAGE_TYPE: message.Subscribed,
        message.Unsubscribe.MESSAGE_TYPE: message.Unsubscribe,
        message.Unsubscribed.MESSAGE_TYPE: message.Unsubscribed,
        message.Event.MESSAGE_TYPE: message.Event,
        message.Call.MESSAGE_TYPE: message.Call,
        message.Cancel.MESSAGE_TYPE: message.Cancel,
        message.Result.MESSAGE_TYPE: message.Result,
        message.Register.MESSAGE_TYPE: message.Register,
        message.Registered.MESSAGE_TYPE: message.Registered,
        message.Unregister.MESSAGE_TYPE: message.Unregister,
        message.Unregistered.MESSAGE_TYPE: message.Unregistered,
        message.Invocation.MESSAGE_TYPE: message.Invocation,
        message.Interrupt.MESSAGE_TYPE: message.Interrupt,
        message.Yield.MESSAGE_TYPE: message.Yield
    }
    """
    Mapping of WAMP message type codes to WAMP message classes.
    """

    def __init__(self, serializer):
        """
        Constructor.

        :param serializer: The object serializer to use for WAMP wire-level serialization.
        :type serializer: An object that implements :class:`autobahn.interfaces.IObjectSerializer`.
        """
        self._serializer = serializer

    def serialize(self, msg):
        """
        Implements :func:`autobahn.wamp.interfaces.ISerializer.serialize`
        """
        return msg.serialize(self._serializer), self._serializer.BINARY

    def unserialize(self, payload, isBinary=None):
        """
        Implements :func:`autobahn.wamp.interfaces.ISerializer.unserialize`
        """
        if isBinary is not None:
            if isBinary != self._serializer.BINARY:
                raise ProtocolError("invalid serialization of WAMP message (binary {0}, but expected {1})".format(isBinary, self._serializer.BINARY))

        try:
            raw_msgs = self._serializer.unserialize(payload)
        except Exception as e:
            raise ProtocolError("invalid serialization of WAMP message ({0})".format(e))

        msgs = []

        for raw_msg in raw_msgs:

            if type(raw_msg) != list:
                raise ProtocolError("invalid type {0} for WAMP message".format(type(raw_msg)))

            if len(raw_msg) == 0:
                raise ProtocolError(u"missing message type in WAMP message")

            message_type = raw_msg[0]

            if type(message_type) not in six.integer_types:
                # CBOR doesn't roundtrip number types
                # https://bitbucket.org/bodhisnarkva/cbor/issues/6/number-types-dont-roundtrip
                raise ProtocolError("invalid type {0} for WAMP message type".format(type(message_type)))

            Klass = self.MESSAGE_TYPE_MAP.get(message_type)

            if Klass is None:
                raise ProtocolError("invalid WAMP message type {0}".format(message_type))

            # this might again raise `ProtocolError` ..
            msg = Klass.parse(raw_msg)

            msgs.append(msg)

        return msgs


# JSON serialization is always supported
try:
    # try import accelerated JSON implementation
    #
    # fallback to stdlib implementation
    #
    import json

    _json = json

    #_loads = json.loads
    _loads = lambda x: json.loads(x, object_hook=serializer_loads)

    def _dumps(obj):
        return json.dumps(obj, separators=(',', ':'), ensure_ascii=False, cls=MySerializer)
finally:
    class JsonObjectSerializer(object):

        JSON_MODULE = _json
        """
        The JSON module used (either stdib builtin or ujson).
        """

        BINARY = False

        def __init__(self, batched=False):
            """
            Ctor.

            :param batched: Flag that controls whether serializer operates in batched mode.
            :type batched: bool
            """
            self._batched = batched

        def serialize(self, obj):
            """
            Implements :func:`autobahn.wamp.interfaces.IObjectSerializer.serialize`
            """
            s = _dumps(obj)
            if isinstance(s, six.text_type):
                s = s.encode('utf8')
            if self._batched:
                return s + b'\30'
            else:
                return s

        def unserialize(self, payload):
            """
            Implements :func:`autobahn.wamp.interfaces.IObjectSerializer.unserialize`
            """
            if self._batched:
                chunks = payload.split(b'\30')[:-1]
            else:
                chunks = [payload]
            if len(chunks) == 0:
                raise Exception("batch format error")
            return [_loads(data.decode('utf8')) for data in chunks]


IObjectSerializer.register(JsonObjectSerializer)


class JsonSerializer(Serializer):

    SERIALIZER_ID = u"json"
    """
    ID used as part of the WebSocket subprotocol name to identify the
    serializer with WAMP-over-WebSocket.
    """

    RAWSOCKET_SERIALIZER_ID = 1
    """
    ID used in lower four bits of second octet in RawSocket opening
    handshake identify the serializer with WAMP-over-RawSocket.
    """

    MIME_TYPE = u"application/json"
    """
    MIME type announced in HTTP request/response headers when running
    WAMP-over-Longpoll HTTP fallback.
    """

    def __init__(self, batched=False):
        """
        Ctor.

        :param batched: Flag to control whether to put this serialized into batched mode.
        :type batched: bool
        """
        Serializer.__init__(self, JsonObjectSerializer(batched=batched))
        if batched:
            self.SERIALIZER_ID = u"json.batched"


ISerializer.register(JsonSerializer)