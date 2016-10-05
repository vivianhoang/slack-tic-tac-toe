from server import entryPositionNames, channels


def new_state(channels, channel_id):
    """Creating a new key item in channels."""

    return {
        "in_progress": False,
        "creator": " ",
        "invited_user_name": " ",
        "accepted_invite": False,
        "players": {},
        "current_player": " ",
        "winner": False,
        'top-left': " ",
        'top-middle': " ",
        'top-right': " ",
        'middle-left': " ",
        'middle': " ",
        'middle-right': " ",
        'bottom-left': " ",
        'bottom-middle': " ",
        'bottom-right': " ",
    }


def restart_board(channels, channel_id):
    """Restarting the board when the game ends or stops."""

    in_channel = channels[channel_id]
    in_channel['in_progress'] = False
    in_channel['winner'] = False
    in_channel['channel_id'] = " "
    in_channel['players'] = {}
    in_channel['accepted_invite'] = False
    in_channel['top-left'] = " "
    in_channel['top-middle'] = " "
    in_channel['top-right'] = " "
    in_channel['middle-left'] = " "
    in_channel['middle'] = " "
    in_channel['middle-right'] = " "
    in_channel['bottom-left'] = " "
    in_channel['bottom-middle'] = " "
    in_channel['bottom-right'] = " "


def winner(entryPositionNames):
    """If there is a winner, the function will return true."""

    # top row
    if ((entryPositionNames.get('top-left') != " ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('top-middle') ==
            entryPositionNames.get('top-right')):
        return True

    # middle row
    if ((entryPositionNames.get('middle-left') != " ") and
        entryPositionNames.get('middle-left') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('middle-right')):
        return True

    # bottom row
    if ((entryPositionNames.get('bottom-left') != " ") and
        entryPositionNames.get('bottom-left') ==
        entryPositionNames.get('bottom-middle') ==
            entryPositionNames.get('bottom-right')):
        return True

    # left
    if ((entryPositionNames.get('top-left') != " ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('middle-left') ==
            entryPositionNames.get('bottom-left')):
        return True

    # middle
    if ((entryPositionNames.get('top-middle') != " ") and
        entryPositionNames.get('top-middle') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-middle')):
        return True

    # right
    if ((entryPositionNames.get('top-right') != " ") and
        entryPositionNames.get('top-right') ==
        entryPositionNames.get('middle-right') ==
            entryPositionNames.get('bottom-right')):
        return True

    # diagonals
    if ((entryPositionNames.get('top-left') != " ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-right')):
        return True

    if ((entryPositionNames.get('top-right') != " ") and
        entryPositionNames.get('top-right') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-left')):
        return True

    else:
        return False
