#!/usr/bin/env python

from __future__ import unicode_literals
import logging
import traceback

from roundwared import daemon
from roundwared import roundgetopt
from roundwared.stream import RoundStream
from roundwared import rounddbus


def listofint(s):
    return map(int, s.split(','))

options_data = [
    ("session_id", int),
    ("foreground",),
    ("project_id", int, 0),
    ("latitude", float, False),
    ("longitude", float, False),
    ("audio_format", str, "MP3"),
    ("audio_stream_bitrate", int, 128),
]

# Set specifically since __name__ is __main__
logger = logging.getLogger('roundwared.rwstreamd')


def main():
    opts = roundgetopt.getopts(options_data)
    request = cmdline_opts_to_request(opts)

    def thunk():
        logger.debug(request)
        start_stream(opts["session_id"], opts["audio_format"], request)

    if opts["foreground"]:
        thunk()
    else:
        daemon.create_daemon(thunk)


def start_stream(sessionid, audio_format, request):
    try:
        logger.info("Starting stream " + str(sessionid))
        current_stream = RoundStream(
            sessionid, audio_format, request)
        rounddbus.add_stream_signal_receiver(current_stream)
        current_stream.start()
    except:
        logger.error(traceback.format_exc())


def cmdline_opts_to_request(opts):
    request = {}
    for p in ['project_id', 'session_id', 'latitude', 'longitude', 'audio_stream_bitrate']:
        request[p] = opts[p]
    # logger.debug("cmdline_opts_to_request - session: " + str(request['session_id']))
    return request

main()