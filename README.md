# teebot
a bot uesd to get information of teeworlds server and forward it to irc channels.

* require python >= 3
* support teeworlds server-0.6.x

### Usage
fill `config.json` as follow (exclude commments) and run `python ./teebot.py`

    {
        "irc_host": "ip or domian name of irc server",
        "irc_port": 6666,   // port number of irc server
        "irc_channels": ["a list of irc channels you want this bot join in", "..."],
        "irc_nick": "teebot",
        "tee_server": "ip of the teeworlds server",
        "tee_alias": "alias of teeworlds server, you can leave it empty",
        "tee_port": 8303    // port number of teeworlds server
    }

### IRC Commmands
* `.tee`: get players list
* `.tee server`: get server info
* `.tee player <playername>`: get player info
* `.tee help`: get help message

### LICENSE
MIT

**FOR `teeserver.py`:** CC BY-NC-SA 3.0
