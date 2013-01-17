#
# Original credits go to:
#
# Sublime Shrink Whitespaces
# Copyright (C) 2011-2012 David Capello
#
# http://github.com/dacap/sublime-shrink-whitespaces

import sublime
import sublime_plugin


def expand_region_in_white_chars(view, reg):
    a = reg.a
    b = reg.b

    # kill backwards
    while True:
        c = view.substr(sublime.Region(a - 1, a))
        if c in (" ", "\t", "\r", "\n"):
            a -= 1
        else:
            break

    # kill forward
    while True:
        c = view.substr(sublime.Region(b + 1, b))
        if c in (" ", "\t", "\r", "\n"):
            b += 1
        else:
            break

    return sublime.Region(a, b)


class KillWhitespaceCommand(sublime_plugin.TextCommand):
    """Removes whitespaces and blank lines."""

    def run(self, edit):
        regions = []
        for r in self.view.sel():
            newreg = expand_region_in_white_chars(self.view, r)
            regions.append(newreg)

        self.view.sel().clear()
        for r in regions:
            self.view.sel().add(r)

        for r in self.view.sel():
            self.view.erase(edit, r)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(regions[0].a, regions[0].a))
