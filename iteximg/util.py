#! /usr/bin/env python3
# -*- coding: utf-8 -*-

def confstr_cleaning(inp: str) -> str:
    '''
    Function that goes through the config string and replace the commas outside
    of the config lines to \n
    '''
    res = ""
    depth = 0
    open_pair = set(["[", "{", "("])
    close_pair = set(["]", "}", ")"])
    inquote = False
    curr = 0
    for i, c in enumerate(inp):
        # print(c, depth, inquote)
        if c in open_pair:
            depth += 1
        elif c in close_pair:
            depth -= 1
        elif c == "\"":
            if inquote:
                inquote = False
            else:
                inquote = True
        elif depth == 0 and not inquote and c == ",":
            res += inp[curr:i]
            res += '\n'
            curr = i + 1
        else:
            pass

    res += inp[curr:]
    return res
