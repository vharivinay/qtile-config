# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
import arcobattery
import keyIndicator

# IMPORT FOR MOUSE CALLBACKS
from libqtile import qtile

# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser("~")


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


keys = [
    # Most of our keybindings are in sxhkd file - except these
    # SUPER + FUNCTION KEYS
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    # SUPER + SHIFT KEYS
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),
    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    # RESIZE UP, DOWN, LEFT, RIGHT
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

groups = []

# FOR QWERTY KEYBOARDS
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
]


group_labels = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

group_layouts = [
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # CHANGE WORKSPACES
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            Key([mod], "Tab", lazy.screen.next_group()),
            Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
            Key(["mod1"], "Tab", lazy.screen.next_group()),
            Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-i AND STAY ON WORKSPACE
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-i AND FOLLOW MOVED WINDOW TO WORKSPACE
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                lazy.group[i.name].toscreen(),
            ),
        ]
    )


def init_layout_theme():
    return {
        "margin": 5,
        "border_width": 2,
        "border_focus": "#4c566a",
        "border_normal": "#3b4252",
    }


layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(
        margin=8, border_width=2, border_focus="#4c566a", border_normal="#3b4252"
    ),
    layout.MonadWide(
        margin=8, border_width=2, border_focus="#4c566a", border_normal="#3b4252"
    ),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
]

# COLORS FOR THE BAR
# Theme name : ArcoLinux Default


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
        ["#242831", "#242831"],
    ]  # 14 super dark background


colors = init_colors()


# WIDGETS FOR THE BAR


def init_widgets_defaults():
    return dict(font="Noto Sans Bold", fontsize=12, padding=2, background=colors[1])


widget_defaults = init_widgets_defaults()

# Qtile bar glyphs

# left = ""
left = ""
right = ""

# MOUSE CALLBACKS


def openCalendar():  # spawn calendar widget
    qtile.cmd_spawn("gsimplecal")


def openHtop():
    qtile.cmd_spawn("alacritty -e htop")


def openMenu():
    qtile.cmd_spawn(
        "rofi -show drun -theme ~/.config/rofi/applauncher/velocity_launcher.rasi"
    )


def powerMenu():
    qtile.cmd_spawn("arcolinux-logout")


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
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
        ),
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
            font="Noto Sans Bold Bold",
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
        # widget.Spacer(
        #     background=colors[2],
        #     length=10,
        # ),
        # arcobattery.BatteryIcon(
        #     padding=0,
        #     scale=0.7,
        #     y_poss=2,
        #     theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
        #     update_interval=5,
        #     background=colors[14],
        # ),
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
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2


widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen1(),
                size=25,
                background="#3b4252",
                border_color=["#3b4252", "#3b4252", "#3b4252", "#3b4252"],
                border_width=[4, 4, 4, 4],
                opacity=1,
                margin=[4, 8, 0, 8],
            )
        ),
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen2(),
                size=26,
                opacity=1,
                margin=[2, 8, 0, 8],
            )
        ),
    ]


screens = init_screens()


# MOUSE CONFIGURATION
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

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################
# assgin apps to groups #
#########################


# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #################################################################################
#     # Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient #
#     #################################################################################
#     d[group_names[0]] = [
#         "Navigator",
#         "Firefox",
#         "Vivaldi-stable",
#         "Vivaldi-snapshot",
#         "Chromium",
#         "Google-chrome",
#         "Brave",
#         "Brave-browser",
#         "navigator",
#         "firefox",
#         "vivaldi-stable",
#         "vivaldi-snapshot",
#         "chromium",
#         "google-chrome",
#         "brave",
#         "brave-browser",
#     ]
#     d[group_names[1]] = [
#         "Atom",
#         "Subl",
#         "Geany",
#         "Brackets",
#         "Code-oss",
#         "Code",
#         "TelegramDesktop",
#         "Discord",
#         "atom",
#         "subl",
#         "geany",
#         "brackets",
#         "code-oss",
#         "code",
#         "telegramDesktop",
#         "discord",
#     ]
#     d[group_names[2]] = [
#         "Inkscape",
#         "Nomacs",
#         "Ristretto",
#         "Nitrogen",
#         "Feh",
#         "inkscape",
#         "nomacs",
#         "ristretto",
#         "nitrogen",
#         "feh",
#     ]
#     d[group_names[3]] = ["Gimp", "gimp"]
#     d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld"]
#     d[group_names[5]] = ["Vlc", "vlc", "Mpv", "mpv"]
#     d[group_names[6]] = [
#         "VirtualBox Manager",
#         "VirtualBox Machine",
#         "Vmplayer",
#         "virtualbox manager",
#         "virtualbox machine",
#         "vmplayer",
#     ]
#     d[group_names[7]] = [
#         "Thunar",
#         "Nemo",
#         "Caja",
#         "Nautilus",
#         "org.gnome.Nautilus",
#         "Pcmanfm",
#         "Pcmanfm-qt",
#         "thunar",
#         "nemo",
#         "caja",
#         "nautilus",
#         "org.gnome.nautilus",
#         "pcmanfm",
#         "pcmanfm-qt",
#     ]
#     d[group_names[8]] = [
#         "Evolution",
#         "Geary",
#         "Mail",
#         "Thunderbird",
#         "evolution",
#         "geary",
#         "mail",
#         "thunderbird",
#     ]
#     d[group_names[9]] = [
#         "Spotify",
#         "Pragha",
#         "Clementine",
#         "Deadbeef",
#         "Audacious",
#         "spotify",
#         "pragha",
#         "clementine",
#         "deadbeef",
#         "audacious",
#     ]
#
#
#####################################################################################
#
# wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME


main = None


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


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
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
        Match(wm_class="arcolinux-logout"),
        Match(wm_class="xfce4-terminal"),
        Match(wm_class="Yad"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="Bluetooth"),
    ],
    fullscreen_border_width=0,
    border_width=0,
)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
