import sys
class PositionError(Exception):
    def __init__(self, position):
        self.position = position
    def __str__(self):
        return repr(self)[:-2] + ': ' + repr(self.position)
class UnknownCommandError(PositionError):
    pass
class UnmatchedBracketError(PositionError):
    pass
class PointOutOfRangeError(PositionError):
    pass

def brainfuckcommand(commandline, warnings = 'off'):
    """Interpret BrainFuck Command
    
    Warings control point out of range report
    Excepted Errors: UnknownCommandError UnmatchedBracketError \
    PointOutOfRangeError
    These Error will all report error position, UnknownCommandError \
    will also report unknown command
    """

    leftbracket = []
    bracketright = []
    rightbracket = []
    buff = [0]
    point = 0
    current = 0
    result = ''
    def brainfuck(command):
        nonlocal point
        nonlocal buff
        nonlocal current
        nonlocal result
        if command == '>':
            point += 1
            if len(buff) <= point:
                buff.append(0)
        elif command == '<':
            point -= 1
            if point < 0 and warnings == 'on':
                #print('Warning: Point escaped range', file=sys.stderr)
                raise PointOutOfRangeError(current+1)
        elif command == '+':
            buff[point] += 1
        elif command == '-':
            buff[point] -= 1
        elif command == '.':
            result += chr(buff[point]) #print(chr(buff[point]),end = '')
        elif command == ',':
            buff[point] = ord(input())
        elif command == '[':
            if buff[point] == 0:
                current = rightbracket[leftbracket.index(current)]-1
        elif command == ']':
            if buff[point] != 0:
                current = leftbracket[rightbracket.index(current)]-1
        elif command == ' ':
            current += 1
    def readcommand(line):
        nonlocal leftbracket
        nonlocal bracketright
        for current in range(len(line)):
            if line[current] == '[':
                leftbracket.append(current)
            elif line[current] == ']':
                bracketright.append(current)
            elif line[current] in ('<', '>', '+', '-', '.', ',', ' '):
                pass
            else:
                raise UnknownCommandError(current+1)
    def sortbracket():
        nonlocal rightbracket
        rightbracket = [] #[0 for i in range(len(bracketright))]
        bracketlist = []
        bracketlist.extend(bracketright)
        bracketlist.extend(leftbracket)
        bracketlist.sort()
        for left in range(len(leftbracket)):
            findright = bracketlist.index(leftbracket[left])
            bracket = 1
            while bracket != 0:
                findright += 1
                if findright >= len(bracketlist):
                    raise UnmatchedBracketError(leftbracket[left]+1)
                if bracketlist[findright] in leftbracket:
                    bracket += 1
                else:
                    bracket -= 1
            rightbracket.append(bracketlist[findright])
        for right in bracketright:
            if right not in rightbracket:
                raise UnmatchedBracketError(right+1)
    readcommand(commandline)
    sortbracket()
    while current < len(commandline):
        brainfuck(commandline[current])
        current += 1
    return result
