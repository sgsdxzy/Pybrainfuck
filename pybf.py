import brainfuck
import sys    

def ErrorHandle(command, warn = 'off'):
    try:
        result = brainfuck.brainfuckcommand(command, warn)
    except (brainfuck.UnknownCommandError, \
        brainfuck.UnmatchedBracketError, \
        brainfuck.PointOutOfRangeError) as err:
        print('TraceBack ( Most recent call last):', file=sys.stderr)
        print(' ', command, file=sys.stderr)
        blank = err.position - 1
        print(' ', ' '*blank + '^', file=sys.stderr)
        print('  ', err, ': ' + command[blank], sep='', file=sys.stderr)
    except:
        print('Unexpected error during command excecution', file=sys.stderr)
        raise
    else:
        print(result)  

if len(sys.argv) == 1:
    print('<<<<<< Welcome to pybrainfuck interactive shell! >>>>>>')
    print("""HELP: Use prompt= to change the left prompt, 
    warnings=on/off to toggle PointOutOfRange warnings""")
    brainfuckprompt = '>>>'
    warn = 'off'
    while 1:
        command = input(brainfuckprompt).replace(' ','')
        if command[:7] == 'prompt=':
            brainfuckprompt = command[7:]
        elif command[:9] == 'warnings=':
            if command[9:11] == 'on':
                warn = 'on'
            elif command[9:12] == 'off':
                warn = 'off'
            else:
                print('Unknown warnings toggle, please use "on" or "off"')
        else:
            ErrorHandle(command, warn)

elif len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        for line in f:
            ErrorHandle(line.replace('\n',''))
else:
    print("""Too many arguments!
    Usage: pybf [file]
    If file is not given, it will start the interactive shell""")
