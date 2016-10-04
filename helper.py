# # change server file later
# from test_server import entryPositionNames

# def winner(entryPositionNames):
#     """If there is a winner, the function will return true."""

#     # top row
#     if ((entryPositionNames.get('top-left') != "    ") and
#         entryPositionNames.get('top-left') ==
#         entryPositionNames.get('top-middle') ==
#             entryPositionNames.get('top-right')):
#         return True

#     # middle row
#     if ((entryPositionNames.get('middle-left') != "    ") and
#         entryPositionNames.get('middle-left') ==
#         entryPositionNames.get('middle') ==
#             entryPositionNames.get('middle-right')):
#         return True

#     # bottom row
#     if ((entryPositionNames.get('bottom-left') != "    ") and
#         entryPositionNames.get('bottom-left') ==
#         entryPositionNames.get('bottom-middle') ==
#             entryPositionNames.get('bottom-right')):
#         return True

#     # diagonals
#     if ((entryPositionNames.get('top-left') != "    ") and
#         entryPositionNames.get('top-left') ==
#         entryPositionNames.get('middle') ==
#             entryPositionNames.get('bottom-right')):
#         return True

#     if ((entryPositionNames.get('top-right') != "    ") and
#         entryPositionNames.get('top-right') ==
#         entryPositionNames.get('middle') ==
#             entryPositionNames.get('bottom-left')):
#         return True

#     else:
#         return False
