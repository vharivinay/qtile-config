#######################################################
#    ____  __  _ __        ______            _____
#   / __ \/ /_(_) /__     / ____/___  ____  / __(_)___ _
#  / / / / __/ / / _ \   / /   / __ \/ __ \/ /_/ / __ `/
# / /_/ / /_/ / /  __/  / /___/ /_/ / / / / __/ / /_/ /
# \___\_\__/_/_/\___/   \____/\____/_/ /_/_/ /_/\__, /
#                                              /____/
#######################################################
# Author: Harivinay V (github.com/vharivinay)
# Link: https://github.com/vharivinay/qtile-config
# Date: 14 March, 2022
# Last Modified: 28 June, 2022
#######################################################

# IMPORTS
import os
import re
import socket
import subprocess
from typing import List
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer

# Custom Widget
import keyIndicator
# Import for mouse callbacks
from libqtile import qtile

# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser("~")

# Functions to move windows to neighboring workspaces
@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

# Define keys array
keys = []

# SUPER + KEYS
super_keys = [
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
        ]
keys.extend(super_keys)

# SUPER + SHIFT + KEYS
super_shift_keys = [
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    ]
keys.extend(super_shift_keys)

# QTILE LAYOUT KEYS
qtile_layout_keys = [
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),
    ]
keys.extend(qtile_layout_keys)

# QTILE CHANGE FOCUS
qtile_change_focus = [
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    ]
keys.extend(qtile_change_focus)

# RESIZE QTILE WINDOW
qtile_resize_window = [
Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    ]
keys.extend(qtile_resize_window)

# QTILE LAYOUT CONTROLS
qtile_layout_controls= [
    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),
    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    ]

keys.extend(qtile_layout_controls)

# CREATE EMPLT GROUPS LIST
groups = []

# CREATE A LIST CONTAINING GROUP NAMES
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
]

# CREATE A LIST CONTAINING GROUP LABELS
group_labels = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

# CREATE A LIST DEFINING LAYOUTS FOR EACH GROUP
group_layouts = [
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
]

# CREATE A DGROUP OBJECT FOR EACH GROUP
for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

# ADDITIONAL KEYBINDINGS FOR NAVIGATION WITHIN GROUPS
for i in groups:
    keys.extend(
        [
            # CHANGE WORKSPACES - MOVE TO GROUP
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            # MOVE TO NEXT GROUP
            Key([mod], "Tab", lazy.screen.next_group()),
            Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
            # MOVE TO PREVIOUS GROUP
            Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
            Key(["mod1"], "Tab", lazy.screen.next_group()),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-i AND STAY ON WORKSPACE
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-i AND FOLLOW
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                lazy.group[i.name].toscreen(),
            ),
        ]
    )

# SCRATCH PAD CONFIG
groups.append(ScratchPad('scratchpad',[
            DropDown('term', 'alacritty', width=0.4, height=0.6, x=0.3, y=0.2, opacity=1),
            DropDown('mixer', 'pavucontrol', width=0.4, height=0.6, x=0.3, y=0.2, opacity=1),
            DropDown('files', 'dolphin', width=0.8, height=0.8, x=0.1, y=0.1, opacity=1)
        ])
    )

# SCRATCH PAD KEYBINDINGS
scratch_keys = [
    Key([mod2], "1", lazy.group["scratchpad"].dropdown_toggle("term")),
    Key([mod2], "2", lazy.group["scratchpad"].dropdown_toggle("files")),
    Key([mod2], "3", lazy.group["scratchpad"].dropdown_toggle("mixer")),
    ]
keys.extend(scratch_keys)

# DEFINE COLORS
def init_colors():
    return [
        ["#2e3440", "#2e3440"],  # 0 background
        ["#d8dee9", "#d8dee9"],  # 1 foreground
        ["#3b4252", "#3b4252"],  # 2 background lighter
        ["#bf616a", "#bf616a"],  # 3 red
        ["#a3be8c", "#a3be8c"],  # 4 green
        ["#ebcb8b", "#ebcb8b"],  # 5 yellow
        ["#81a1c1", "#81a1c1"],  # 6 blue
        ["#b48ead", "#b48ead"],  # 7 magenta
        ["#88c0d0", "#88c0d0"],  # 8 cyan
        ["#e5e9f0", "#e5e9f0"],  # 9 white
        ["#4c566a", "#4c566a"],  # 10 grey
        ["#d08770", "#d08770"],  # 11 orange
        ["#8fbcbb", "#8fbcbb"],  # 12 super cyan
        ["#5e81ac", "#5e81ac"],  # 13 super blue
        ["#242831", "#242831"],  # 14 super dark background
    ]


colors = init_colors()

# INITIATE DEFAULT THEME
def init_layout_theme():
    return {
        "margin": 5,
        "border_width": 2,
        "border_focus": colors[1],
        "border_normal": colors[13],
    }


layout_theme = init_layout_theme()

# LIST OF LAYOUTS
layouts = [
    # MASTER STACK VERTICAL SPLIT
    layout.MonadTall(**layout_theme),
    # MASTER STACK HORIZONTAL SPLIT
    layout.MonadWide(**layout_theme),
    # FLOATING
    layout.Floating(**layout_theme),
    # MAXIMUM WIDTH
    layout.Max(**layout_theme),
]

# MOUSE CALLBACKS FOR CLICK EVENTS
# spawn calendar widget
def openCalendar():
    qtile.cmd_spawn("gsimplecal")


# Open htop
def openHtop():
    qtile.cmd_spawn("alacritty -e htop")


# Open rofi app menu
def openMenu():
    qtile.cmd_spawn(
        "rofi -show drun -theme ~/.config/rofi/applauncher/velocity_launcher.rasi"
    )


# Open archlinux logout menu
def powerMenu():
    qtile.cmd_spawn("archlinux-logout")

#INITIATE WIDGET DEFAULTS
def init_widgets_defaults():
    return dict(font="Noto Sans Bold", fontsize=12, padding=2, background=colors[2], foreground=colors[14])


widget_defaults = init_widgets_defaults()

# DEFINE QTILE BAR GLYPHS
left = ""
right = ""

# INITIATE EMPTY WIDGET LIST
main_widgets_list = []

# APP MENU WIDGET
app_menu_widget = [
        widget.Spacer(
            background=colors[2],
            length=10,
        ),
        widget.Image(
            background=colors[2],
            filename="~/.config/qtile/icons/flash.png",
            mouse_callbacks={"Button1": openMenu},
        ),
        widget.Spacer(
            background=colors[2],
            length=10,
        )
    ]

main_widgets_list.extend(app_menu_widget)

# GRUOP BOX WIDGET (WORKSPACES)
group_box_widget = [
        widget.TextBox(
            font="MesloLGS NF",
            text=left,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.GroupBox(
            font="FontAwesome",
            fontsize=18,
            margin_y=2,
            margin_x=0,
            padding_y=6,
            padding_x=4,
            disable_drag=True,
            use_mouse_wheel=True,
            active=colors[13],
            inactive=colors[10],
            rounded=True,
            highlight_color=colors[2],
            block_highlight_text_color=colors[6],
            highlight_method="text",
            this_current_screen_border=colors[4],
            this_screen_border=colors[4],
            other_current_screen_border=colors[14],
            other_screen_border=colors[14],
            foreground=colors[1],
            background=colors[14],
            urgent_border=colors[3],
        ),
        widget.TextBox(
            font="MesloLGS NF",
            text=right,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.Spacer(
            background=colors[2],
            length=20,
        ),
    ]

main_widgets_list.extend(group_box_widget)

# WINDOW NAME WIDGET
window_name_widget = [
        widget.TextBox(
            font="MesloLGS NF",
            text=left,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.WindowName(
            font="Noto Sans Bold",
            fontsize=12,
            foreground=colors[1],
            background=colors[14],
            width=bar.CALCULATED,
            empty_group_string="Desktop",
            max_chars=80,
        ),
        widget.TextBox(
            font="MesloLGS NF",
            text=right,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.Spacer(
            background=colors[2],
        ),
    ]

main_widgets_list.extend(window_name_widget)

# CURRENT LAYOUT ICON
current_layout_icon_widget = [
        widget.TextBox(
            font="MesloLGS NF",
            text=left,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.CurrentLayoutIcon(
            foreground=colors[1], background=colors[14], scale=0.75
        ),
        widget.TextBox(
            font="MesloLGS NF",
            text=right,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.Spacer(
            background=colors[2],
            length=5,
        ),
    ]

main_widgets_list.extend(current_layout_icon_widget)

# CAPS AND NUM LOCK INDICATOR
key_indicator_widget = [
        widget.TextBox(
            font="MesloLGS NF",
            text=left,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        keyIndicator.CapsNumLockIndicator(
            foreground=colors[1], background=colors[14], padding=6, fontsize=24
        ),
        widget.TextBox(
            font="MesloLGS NF",
            text=right,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.Spacer(
            background=colors[2],
            length=5,
        ),
    ]

main_widgets_list.extend(key_indicator_widget)

# SYSTEM MONITERING WIDGET
system_moniter_widget = [
        widget.TextBox(
            font="MesloLGS NF",
            text=left,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.TextBox(
            font="FontAwesome",
            text="  ",
            foreground=colors[13],
            background=colors[14],
            padding=0,
            fontsize=16,
            mouse_callbacks={"Button1": openHtop},
        ),
        widget.TextBox(
            font="Noto Sans Bold",
            text=" CPU ",
            foreground=colors[1],
            background=colors[14],
            padding=0,
            fontsize=12,
            mouse_callbacks={"Button1": openHtop},
        ),
        # # do not activate in Virtualbox - will break qtile
        widget.ThermalSensor(
            foreground=colors[1],
            foreground_alert=colors[11],
            background=colors[14],
            metric=True,
            padding=3,
            tag_sensor="Package id 0",
            threshold=80,
            mouse_callbacks={"Button1": openHtop},
        ),
        widget.TextBox(
            font="Noto Sans Bold",
            text=" GPU ",
            foreground=colors[1],
            background=colors[14],
            padding=0,
            fontsize=12,
            mouse_callbacks={"Button1": openHtop},
        ),
        widget.ThermalSensor(
            foreground=colors[1],
            foreground_alert=colors[11],
            background=colors[14],
            metric=True,
            padding=3,
            tag_sensor="GPU",
            threshold=80,
            mouse_callbacks={"Button1": openHtop},
        ),
        widget.Sep(
            foreground=colors[1],
            background=colors[14],
            linewidth=2,
            padding=2,
            size_percent=50,
        ),
        widget.TextBox(
            font="FontAwesome",
            text="  ",
            foreground=colors[13],
            background=colors[14],
            padding=0,
            mouse_callbacks={"Button1": openHtop},
            fontsize=16,
        ),
        widget.Memory(
            font="Noto Sans Bold",
            measure_mem="G",
            format="{MemUsed: .1f}G/{MemTotal: .1f}G ",
            update_interval=5,
            fontsize=12,
            foreground=colors[1],
            background=colors[14],
            mouse_callbacks={"Button1": openHtop},
        ),
        widget.TextBox(
            font="MesloLGS NF",
            text=right,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.Spacer(
            background=colors[2],
            length=5,
        ),
    ]

main_widgets_list.extend(system_moniter_widget)

# CALENDER AND CLOCK
calendar_clock_widget = [
         widget.TextBox(
            font="MesloLGS NF",
            text=left,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.TextBox(
            font="FontAwesome",
            text="",
            foreground=colors[13],
            background=colors[14],
            mouse_callbacks={"Button1": openCalendar},
            padding=1,
            fontsize=24,
        ),
        widget.Clock(
            font="Noto Sans Bold",
            foreground=colors[1],
            background=colors[14],
            fontsize=12,
            mouse_callbacks={"Button1": openCalendar},
            format=" %a-%d | %H:%M ",
        ),
        widget.TextBox(
            font="MesloLGS NF",
            text=right,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.Spacer(
            background=colors[2],
            length=5,
        ),
    ]

main_widgets_list.extend(calendar_clock_widget)

# BRIGHTNESS INDICATOR
brightness_widget = [
        widget.TextBox(
            font="MesloLGS NF",
            text=left,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.TextBox(
            font="FontAwesome",
            text="",
            foreground=colors[1],
            background=colors[14],
            padding=0,
            fontsize=32,
        ),
        widget.Backlight(
            backlight_name="intel_backlight",
            background=colors[14],
            foreground=colors[1],
        ),
        widget.Sep(
            foreground=colors[1],
            background=colors[14],
            linewidth=0,
            padding=2,
            size_percent=50,
        ),
        widget.Sep(
            foreground=colors[1],
            background=colors[14],
            linewidth=0,
            padding=2,
            size_percent=50,
        ),
    ]

main_widgets_list.extend(brightness_widget)

# BATTERY INDICATOR
battery_widget = [
        widget.Battery(
            font="Noto Sans Bold",
            format="{char} {percent:2.0%}",
            charge_char="",
            discharge_char="",
            full_char="",
            update_interval=10,
            fontsize=14,
            foreground=colors[1],
            background=colors[14],
        ),
    ]

main_widgets_list.extend(battery_widget)

# SYSTEM TRAY
system_tray = [
        widget.Systray(background=colors[14], icon_size=22, padding=4),
        widget.TextBox(
            font="MesloLGS NF",
            text=right,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.Spacer(
            background=colors[2],
            length=10,
        ),
    ]

main_widgets_list.extend(system_tray)

# POWER BUTTON
power_button = [
        widget.TextBox(
            font="MesloLGS NF",
            text=left,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.TextBox(
            font="FontAwesome",
            text="",
            foreground=colors[13],
            background=colors[14],
            padding=0,
            fontsize=18,
            mouse_callbacks={"Button1": powerMenu},
        ),
        widget.TextBox(
            font="MesloLGS NF",
            text=right,
            foreground=colors[14],
            background=colors[2],
            padding=0,
            fontsize=18,
        ),
        widget.Spacer(
            background=colors[2],
            length=5,
        ),
    ]

main_widgets_list.extend(power_button)

# SETUP WIDGETS & QTILE BAR
def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = main_widgets_list
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


widgets_screen1 = init_widgets_screen1()


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen1(),
                size=25,
                background=colors[2],
                border_color=["#3b4252","#3b4252","#3b4252","#3b4252"],
                border_width=[4, 4, 4, 4],
                opacity=1,
                margin=[4, 8, 0, 8],
            )
        ),
   ]


screens = init_screens()

# MOUSE INTERACTION FOR FLOATING WINDOWS
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
]

# REMAIN FROM DEFAULT CONFIG
dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO GROUPS
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
    d[group_names[0]] = ["Chromium", "chromium"]
    d[group_names[1]] = ["Alacritty", "Alacritty"]
    d[group_names[2]] = ["emacs","Emacs"]
    d[group_names[3]] = ["vscodium", "VSCodium"]
    d[group_names[4]] = []
    d[group_names[5]] = ["Vlc", "vlc"]
    d[group_names[6]] = ["Navigator", "firefox"]

    wm_class = client.window.get_wm_class()[0]

    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen(toggle=False)


main = None

# ONE TIME / STARTUP FUNCTIONS
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True

# CURSOR BEHAVIOR
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

# FLOATING WINDOW RULES
floating_types = ["notification", "toolbar", "splash", "dialog"]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="Arcolinux-welcome-app.py"),
        Match(wm_class="Arcolinux-tweak-tool.py"),
        Match(wm_class="Arcolinux-calamares-tool.py"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="Arandr"),
        Match(wm_class="feh"),
        Match(wm_class="Galculator"),
        Match(wm_class="archlinux-logout.py"),
        Match(wm_class="xfce4-terminal"),
        Match(wm_class="Yad"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="Bluetooth"),
    ],
    fullscreen_border_width=0,
    border_width=0,
)

# FINISH UP
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
