# Codeforces Contest/Gym Monitor

This application is designed to monitor Codeforces contests and gyms in real-time, providing users with the ability to add, remove, and track these events on their server while receiving timely notifications.

## Overview

Codeforces Contest/Gym Monitor is a Discord bot that assists in tracking Codeforces contests and gyms effortlessly. It allows users to manage a watchlist of these events and receive notifications in specified channels whenever there are updates or changes.

## Features

- **Add Watch:** Add a new Codeforces contest/gym page to the watch list for your server.
- **Remove Watch:** Remove a Codeforces contest/gym page from the watch list of your server.
- **List Watches:** Display all watches with their current channel ID and contest/gym link.

## Commands

### Add Watch

Adds a new Codeforces contest/gym page to the watch list for your server.

#The command format is: addwatch <name> <contest link> <channelid>, where:
- `<name>`: Name for the contest/gym being watched.
- `<contest link>`: Link to the Codeforces contest or gym page.
- `<channelid>`: ID of the channel where notifications will be sent.

### Remove Watch

Removes a Codeforces contest/gym page from the watch list of your server.

#The command format is: remwatch <name>, where:
- `<name>`: Name of the contest/gym to be removed from the watchlist.

### List Watches

Displays all watches with their current channel ID and contest/gym link.

## Usage

1. Clone the repository.
2. Install dependencies using `npm install`.
3. Set up the required configurations.
4. Run the application using `node app.js`.

## Configuration

Ensure you set up the following configurations:

- **Token:** Add your Discord bot token.
- **Permissions:** Ensure the bot has the necessary permissions to send messages in specified channels.

## Contributing

Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request for any enhancements or fixes.

