#!/usr/bin/env python3
# -*- encoding: UTF-8 -*-
import json
from ircbot import ircbot
from teeserver import teeserver

def players_list(srv):
    return '{0}/{1} people(s) in {2}: {3}'.format(
            srv.cur_player_num,
            srv.max_player_num,
            srv.alias,
            ', '.join([ '{0}({1})'.format(p['name'], p['score']) for p in srv.players])
            )


def player_info(srv, name):
    for p in srv.players:
        if p['name'] == name:
            return '{0}, clan: {1}, region: {2}, score: {3}, stat: {4}'.format(
                    p['name'],
                    p['clan'],
                    p['region'],
                    p['score'],
                    p['stat']
                    )
    return 'player `{0}` not found <(=﹁"﹁=)>'.format(name)


def server_info(srv):
    return '{0}, version: {1}, address: {2}:{3} gamemode: {4}, map: {5}, players: {6}/{7}'.format(
            srv.name,
            srv.version,
            srv.ip,
            srv.port,
            srv.mode,
            srv.map_name,
            srv.cur_player_num,
            srv.max_player_num
            )


def help():
    return ('Usage: `.tee` => get players list, '
            '`.tee server` => get server info, '
            '`.tee player <playername>` => get player info, '
            '`.tee help` => get this message.'
            )


def main():
    with open('./config.json') as f:
        conf = json.loads(f.read())
        irc_host = conf['irc_host']
        irc_port = conf['irc_port']
        irc_chans = conf['irc_channels']
        irc_nick = conf['irc_nick']
        tee_server = conf['tee_server']
        tee_alias = conf['tee_alias']
        tee_port = conf['tee_port']

    bot = ircbot(irc_host, irc_port, irc_nick)
    srv = teeserver(tee_server, tee_port, tee_alias)

    for chan in irc_chans:
        bot.join_chan(chan)

    while (True):
        try:
            man, chan, msg = bot.recv_msg()
            if msg and msg.startswith('.tee'):
                print('[teebot]', 'recv command `.tee`')

                if not srv.update():
                    bot.send_msg(chan, man + ': ' + 'failed to update server info')
                    continue

                reply = ''
                msg = [ x for x in msg.split(' ') if x]

                if msg[1:]:
                    if msg[1] == 'server':
                        reply = server_info(srv)
                    if msg[1] == 'player' and msg[2:]:
                        reply = player_info(srv, msg[2])
                    if msg[1] == 'help':
                        reply = help()
                else:
                    reply = players_list(srv)

                if reply:
                    bot.send_msg(chan, man + ': ' + reply)
        except KeyboardInterrupt:
            bot.stop()
            srv.stop()
            print('[teebot]', 'exit')
            exit(0)


if __name__ == '__main__':
    main()
