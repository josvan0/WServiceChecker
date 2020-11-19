from converter import export_xml
from event import Message, WServiceCheckerException


# global
PROMPT = 'WService $ '
run = True


# commands
def get_help():
    pass


def exit_prompt():
    global run
    run = False


# switch
exec_command = {
    'e': exit_prompt,
    'f': export_xml,
    'h': get_help,
    'exit': exit_prompt,
    'format': export_xml,
    'help': get_help
}

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
    except WServiceCheckerException as e:
        Message.create(e, Message.ERROR)
