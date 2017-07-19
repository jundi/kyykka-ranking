"""Common functions"""
def str2list(line):
    """Split line to list of words"""
    fields = line.split(',')
    fields = [x.strip() for x in fields]
    return fields


def str2bool(string):
    """Map string to boolean"""
    if string in ('False', '0'):
        return False
    elif string in ('True', '1'):
        return True
    else:
        raise Exception
