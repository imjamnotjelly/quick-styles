from os import system
from time import strftime

system("")

valid_args = ["color", "bgcolor", "styles"]

color_codes = {
    # color: (fg, bg),
    "black": (30, 40),
    "red": (31, 41),
    "green": (32, 42),
    "yellow": (33, 43),
    "blue": (34, 44),
    "magenta": (35, 45),
    "cyan": (36, 46),
    "lightgray": (37, 47),
    "gray": (90, 100),
    "lightred": (91, 101),
    "lightgreen": (92, 102),
    "lightyellow": (93, 43),
    "lightblue": (94, 104),
    "lightmagenta": (95, 105),
    "lightcyan": (96, 106),
    "white": (97, 107),
}

style_codes = {
    # style-name: ansi-num
    "bold": 1,
    "italic": 3,
    "underline": 4,
    "blink": 5,
    "strikethrough": 9,
}

modifiers = {
    # modifier: template
    "time_display": f"[{strftime('%H:%M:%S')}] " + "{}",
    "warning": "! {} !",
}

custom_codes = {}


def create_code(**kwargs):
    values = []

    # foreground colors
    if "color" in kwargs:
        values.append(color_codes[kwargs["color"]][0])

    # background colors
    if "bgcolor" in kwargs:
        values.append(color_codes[kwargs["bgcolor"]][1])

    # text styles
    if "styles" in kwargs:
        styles = kwargs["styles"]
        if isinstance(styles, str):
            styles = [styles]
        styles = list(map(lambda x: style_codes[x], styles))
        values.extend(styles)

    # merging styles and generating ansi escape code
    values = [str(i) for i in values]
    ansi_code = f"\033[{';'.join(sorted(values))}m"
    return ansi_code


def style_string(string, **kwargs):
    # configuring ansi code
    ansi_code = ""
    if "custom_code" in kwargs:
        if kwargs["custom_code"].startswith("\033["):
            ansi_code = kwargs["custom_code"]
        else:
            ansi_code = custom_codes[kwargs["custom_code"]]
    else:
        code_args = {k: v for k, v in kwargs.items() if k in valid_args}
        ansi_code = create_code(**code_args)

    # applying modifier if present
    if "modifier" in kwargs:
        string = modifiers[kwargs["modifier"]].format(string)

    # forming string
    return ansi_code + string + "\033[0m"


# dedicated functions for print & input styling
def cprint(string, **kwargs):
    print(style_string(string, **kwargs))


def cinput(string, **kwargs):
    return input(style_string(string, **kwargs))
