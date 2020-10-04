#!/usr/bin/env python3
#
# Depends:
# -- i3ipc - pip install
#
#
# How to use:
# -- Download this script, I'll assume ~/.config/i3/scripts
# -- Put "exec_always python ~/.config/i3/scripts/nameWorkspaces.py &" in your i3 config
# -- Restart i3
#
# For polybar:
# -- Make sure 'strip-wsnumbers' is true
# -- labels should not use %icon%, only %name%



from pprint import pprint
from i3ipc import Event, Connection


# Create main connection to i3wm
i3 = Connection()


# Setup icon lists, regular and negative. 10+ are because I have more than 1-9 workspaces
# but there seems to only be "circled digit [0-9]"
icons = ["⓪","①","②","③","④","⑤","⑥","⑦","⑧","⑨","10","11","12","13","14"]
iconsNeg = ["⓿","❶","❷","❸","❹","❺","❻","❼","❽","❾","10","11","12","13","14"]


# focused = i3.get_tree().find_focused()
# print(f'Focused window {focused.name} is on workspace {focused.workspace().name}')


def on_workspace_focus(self, e):
    workspaces = i3.get_workspaces()
    for ws in workspaces:
        # Simply checks if workspace is visible, this easily makes it work for multimonitor setups
        if ws.visible:
            newName = f'{ws.num}: {icons[ws.num]}'
        else:
            newName = f'{ws.num}: {iconsNeg[ws.num]}'

        # Avoid renaming to the same name, causes weird behavior when renaming multiple workspaces
        if ws.name == newName:
            continue

        # Notice the quotes, this is the same as $ i3-msg 'rename workspace "1: ①" to "1: ❶"'
        # No quotes, no worky
        i3.command(f'rename workspace "{ws.name}" to "{newName}"')


# workspaces = i3.get_workspaces()
# for workspace in workspaces:
#     print(f'workspace: {workspace.name} :: num: {workspace.num} :: output: {workspace.output} :: focused: {workspace.focused} :: visible: {workspace.visible}')

# pprint(vars(workspaces[0]))

# i3.command(f'rename workspace "{workspaces[5].name}" to "1: {icons[1]}"')



i3.on(Event.WORKSPACE_FOCUS, on_workspace_focus)

i3.main()
