# TangoBot
[Ryan Brand](https://github.com/UNA8211) and [Ethan Peterson](https://github.com/blackbelt238)'s work from the Montana State University robotics lab.

The Tango bot is made up of a Raspberry Pi and Android that work together to control numerous servos and speech functionality. Currently, our bot can be:
- controlled via keyboard (either directly connected or via SSH)
- given commands to execute via a GUI on its' face
- verbally told commands via STT functionality on an Android

### File Breakdown
The [Controller](https://github.com/blackbelt238/TangoBot/maestro.py) class is used to directly control the servos.

[Bot](https://github.com/blackbelt238/TangoBot/bot.py) provides an interface to the servo controller in the form of commands that define the base functionality of the Tango bot.

[Tango](https://github.com/blackbelt238/TangoBot/tango.py) utilizes the base functionalities defined in the Bot class to create behaviors. This is where driving, head movement, speech, and other actions are actually defined. The Tango bot is controlled via interaction with the Tango class.

[keyboard-control](https://github.com/blackbelt238/TangoBot/keyboard-control.py) leverages the Tango class to enable control of the Tango bot from a keyboard (either directly connected or via SSH). Consult the file for details on the specific key bindings.

[gui-control](https://github.com/blackbelt238/TangoBot/gui-control.py) also leverages the Tango class, allowing users to program the Tango bot with commands via a graphical user interface. Once added, commands can be either executed in series or removed from the [execution queue](https://github.com/blackbelt238/TangoBot/actionq.py).
