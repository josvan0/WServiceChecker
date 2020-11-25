from converter import export_xml
from diff import diff_service_lists
from event import Message, WServiceCheckerException


# global
PROMPT = 'WService $ '
run = True


# commands
def get_help():
    """Print documentation file content in prompt.
    """
    with open(r'./src/doc.txt', 'r') as f:
        for line in f.readlines():
            print(line.replace('\n', ''))


def exit_prompt():
    """Exit securily from the prompt.
    """
    global run
    Message.create('Goodbye!!!',
                   Message.INFORMATION)
    run = False


# switch
exec_command = {
    'd': diff_service_lists,
    'e': exit_prompt,
    'f': export_xml,
    'h': get_help,
    'diff': diff_service_lists,
    'exit': exit_prompt,
    'format': export_xml,
    'help': get_help
}

print('WServiceChecker v1.0.0')
print('Type "exit" or "e" for finish session...', end='\n\n')

while run:
    user_input = input(PROMPT)
    args = user_input.split(' ')
    try:
        if len(args) > 1:
            exec_command[args[0]](args[1:])
        else:
            exec_command[args[0]]()

    except KeyError:
        Message.create('Command not recognized',
                       Message.WARNING)
        Message.create('Type "help" o "h" to get more info about program...',
                       Message.INFORMATION)

    except WServiceCheckerException as e:
        Message.create(e, Message.ERROR)
