# Codeforces Mashup Listener

Codeforces Mashup Listener is a Discord bot primarily designed to monitor private gym contests (but can also monitor public gyms and contests). The idea for this project stemmed from the need to track tester's real-time performance in their virtual participation for future Codeforces rounds. Rather than manually checking Codeforces every minute, this bot automates the process.

## Overview

### Usage

Codeforces Mashup Listener features 3 commands:
- `addwatch <name> <mashup link> <channelid>`: Adds a new watch named `name` that points to `mashup link` and sends submission notifications in `channelid`. Accessible only to administrators.
- `remwatch <name>`: Removes the watch named `name`. Accessible only to administrators.
- `watches`: Displays all active watches. Accessible to anyone.

### Prerequisites

To run the bot, you'll need:
- Python 3
- PostgreSQL
- Selenium

### Configuration

The repository includes a configuration file `config.json` with the following entries:
- `token`: The bot's token from the Discord developer portal.
- `prefix`: The prefix used for commands.
- `dbname`: The database name.
- `user`: The database user.
- `password`: The corresponding password for `user`.
- `host`: The database host.
- `port`: The connection port (default is 5432).
- `login`: Must be true if you want to monitor private gyms.
- `cfHandle`: If `login` is true, provide the handle for the Codeforces account.
- `cfPassword`: Similarly, the password for the Codeforces account.

## Note

The bot's current version might not support large-scale monitoring due to its reliance on the host's IP address. However, the addition of proxies can bypass Codeforces rate limiting.

Feel free to enhance the bot further based on your needs and usage scenarios.
