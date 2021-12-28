import gdb
import os
import json

file_name = "address_note.json"
notes = {}


class note_command(gdb.Command):
    def __init__(self):
        super(note_command, self).__init__("note", gdb.COMMAND_RUNNING)

        if os.path.exists(file_name):
            print("json note file found.")
            with open(file_name, "r") as f:
                notes = json.loads(f.read())
        else:
            notes = {}

    def invoke(self, arg, from_tty):
        if arg == "":
            print("No arguments were given")
            return

        argv = arg.split(" ")

        if len(argv) == 1:
            name = argv[0]
            print("save stack pointer as {}".format(name))
            rsp = gdb.newest_frame().read_register("rsp")

            notes[name] = int("{}".format(rsp), 16)
        elif len(argv) == 2:
            name = argv[0]
            value_str = argv[1]

            if value_str[0:2] == "0x":
                value = int(value_str, 16)
                print("save {} as {}".format(hex(value), name))
            else:
                value = int(value_str)
                print("save {} as {}".format(value, name))

            notes[name] = value


class save_note_command(gdb.Command):
    def __init__(self):
        super(save_note_command, self).__init__("save_note", gdb.COMMAND_RUNNING)

    def invoke(self, arg, from_tty):
        with open(file_name, "w") as f:
            f.write(json.dumps(notes))
        print("dump success")


class show_note_command(gdb.Command):
    def __init__(self):
        super(show_note_command, self).__init__("show_note", gdb.COMMAND_RUNNING)

    def invoke(self, arg, from_tty):
        print(notes)


note_command()
save_note_command()
show_note_command()
