"""Utility functions"""

def to_listlist(inlist:list):
    """Ensures element is a list of lists even if single inner list"""
    return [inlist] if type(inlist[0]) is not list else inlist