# -*- coding: utf-8 -*-
# Copyright (C) 2018 Juan Riquelme González
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
# Modified:
#   By: Harivinay
#   Github: https://www.github.com/m87k452b
#   Date: Jan 31, 2022
#   Modifications: To show icons for lock status

import re
import subprocess

from libqtile.widget import base


class CapsNumLockIndicator(base.ThreadPoolText):
    """Really simple widget to show the current Caps/Num Lock state."""

    defaults = [("update_interval", 0.5, "Update Time in seconds.")]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(CapsNumLockIndicator.defaults)

    def get_indicators(self):
        """Return a list with the current state of the keys."""
        try:
            output = self.call_process(["xset", "q"])
        except subprocess.CalledProcessError as err:
            output = err.output
            return []
        if output.startswith("Keyboard"):
            keyStatus = re.findall(r"(Caps|Num)\s+Lock:\s*(\w*)", output)
            capsStatus = keyStatus[0]
            numStatus = keyStatus[1]
            if numStatus[1] == "on":
                N = ""
            else:
                N = ""
            if capsStatus[1] == "on":
                C = "ﰶ"
            else:
                C = "ﰷ"
            indicators = [C, N]
            return indicators

    def poll(self):
        """Poll content for the text box."""
        indicators = self.get_indicators()
        status = str(indicators[0]) + " " + str(indicators[1])
        return status
