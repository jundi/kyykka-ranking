def str2list(line):
                fields = line.split(',')
                fields = [x.strip() for x in fields]


def str2bool(string):
    if string in ('False', '0'):
        return False
    elif string in ('True', '1'):
        return True
    else:
        raise Exception
