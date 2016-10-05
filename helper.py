from server import entryPositionNames, currentState


def restart_board(currentState):
    """Restarting the board when the game ends or stops."""

    currentState['in_progress'] = False
    currentState['winner'] = False
    currentState['channel_id'] = " "
    currentState['players'] = {}
    currentState['accepted_invite'] = False


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
