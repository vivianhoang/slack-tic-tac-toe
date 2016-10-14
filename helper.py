from server import channels


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
    # in_channel['channel_id'] = " "
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


def winner(channels, channel_id):
    """If there is a winner, the function will return true."""

    # top row
    if ((channels.get(channel_id).get('middle-left') != " ") and
        channels.get(channel_id).get('middle-left') ==
        channels.get(channel_id).get('middle') ==
            channels.get(channel_id).get('middle-right')):
        return True

    # middle row
    if ((channels.get(channel_id).get('middle-left') != " ") and
        channels.get(channel_id).get('middle-left') ==
        channels.get(channel_id).get('middle') ==
            channels.get(channel_id).get('middle-right')):
        return True

    # bottom row
    if ((channels.get(channel_id).get('bottom-left') != " ") and
        channels.get(channel_id).get('bottom-left') ==
        channels.get(channel_id).get('bottom-middle') ==
            channels.get(channel_id).get('bottom-right')):
        return True

    # left
    if ((channels.get(channel_id).get('top-left') != " ") and
        channels.get(channel_id).get('top-left') ==
        channels.get(channel_id).get('middle-left') ==
            channels.get(channel_id).get('bottom-left')):
        return True

    # middle
    if ((channels.get(channel_id).get('top-middle') != " ") and
        channels.get(channel_id).get('top-middle') ==
        channels.get(channel_id).get('middle') ==
            channels.get(channel_id).get('bottom-middle')):
        return True

    # right
    if ((channels.get(channel_id).get('top-right') != " ") and
        channels.get(channel_id).get('top-right') ==
        channels.get(channel_id).get('middle-right') ==
            channels.get(channel_id).get('bottom-right')):
        return True

    # diagonals
    if ((channels.get(channel_id).get('top-left') != " ") and
        channels.get(channel_id).get('top-left') ==
        channels.get(channel_id).get('middle') ==
            channels.get(channel_id).get('bottom-right')):
        return True

    if ((channels.get(channel_id).get('top-right') != " ") and
        channels.get(channel_id).get('top-right') ==
        channels.get(channel_id).get('middle') ==
            channels.get(channel_id).get('bottom-left')):
        return True

    else:
        return False
