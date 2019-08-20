#!/usr/bin/env python

from apicalls.pinterest import Pinterest

def get_pins_on_board(user, username, board):
    postfix = 'v1/boards/' + username + '/' + board + '/pins/'
    args = {
        'endpoint_postfix': postfix,
        'request_type': 'GET',
        'params': {
            'fields': ['link', 'note', 'counts', 'metadata']
        }
    }
    api_call = Pinterest(user, args)
    api_call.place_call()
    if (api_call.error):
        return
    else:
        return api_call.data

