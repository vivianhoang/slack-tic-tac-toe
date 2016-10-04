# change server file later
from test-server import entryPositionNames

def winner(entryPositionNames):
    """If there is a winner, the function will return true."""

    # top row
    if ((entryPositionNames.get('top-left') != "    ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('top-middle') ==
            entryPositionNames.get('top-right')):
        currentState['in_progress'] = False
        return True

    # middle row
    if ((entryPositionNames.get('middle-left') != "    ") and
        entryPositionNames.get('middle-left') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('middle-right')):
        currentState['in_progress'] = False
        return True

    # bottom row
    if ((entryPositionNames.get('bottom-left') != "    ") and
        entryPositionNames.get('bottom-left') ==
        entryPositionNames.get('bottom-middle') ==
            entryPositionNames.get('bottom-right')):
        currentState['in_progress'] = False
        return True

    # diagonals
    if ((entryPositionNames.get('top-left') != "    ") and
        entryPositionNames.get('top-left') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-right')):
        currentState['in_progress'] = False
        return True

    if ((entryPositionNames.get('top-right') != "    ") and
        entryPositionNames.get('top-right') ==
        entryPositionNames.get('middle') ==
            entryPositionNames.get('bottom-left')):
        currentState['in_progress'] = False
        return True

    else:
        return False
