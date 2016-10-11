# Slash Command Integration for Slack: Tic-Tac-Toe

This is a slash command integration of tic-tac-toe that is playable for users within a Slack Team. There can be multiple games being played simultaneously within a team, but there can only be one game being played per channel. A player can only invite a person who exists within the team and cannot initiate a game by inviting themselves. If a player makes an invalid move or submits ___/ttt-help___, a Slack bot will display more information that is only visible to that user. Every other command is visible. 

Currently, the tic-tac-toe board displays normally on mobile and desktop, but not within mobile notifications. API tokens are currently stored in Heroku and the server automatically deploys when it is pushed to GitHub.


## Commands

Slack commands:

- ___/ttt [@username]___ - Start a new game by inviting someone.
- ___/ttt-accept___ - Accept the game invitation.
- ___/ttt-decline___ - Decline the game invitation.
- ___/ttt-board___ - Show game board.
- ___/ttt-move [position]___ - Place a letter on an empty square. Positions include'top-left', 'top-middle', 'top-right', 'middle-left', 'middle', 'middle-right','bottom-left', 'bottom-middle', 'bottom-right'.
- ___/ttt-end___ - End the game.
- ___/ttt-help___ - Displays all descriptions of each slash command availible for the game.


### Technology Stack

**Application:** Python, Flask, Jinja2

**APIs:** Slack: Slack Bots, Slash Commands

**Host Service:** Heroku


