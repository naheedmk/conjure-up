from __future__ import unicode_literals
from urwid import WidgetWrap, Text, Pile, ListBox, BoxAdapter, Divider, Columns
from ubuntui.widgets.buttons import (cancel_btn, menu_btn)
from ubuntui.utils import Color, Padding
from ubuntui.ev import EventLoop
from ubuntui.lists import SimpleList


class WelcomeView(WidgetWrap):
    def __init__(self, common, cb):
        self.common = common
        self.cb = cb
        self.current_focus = 2
        _pile = [
            Padding.center_90(Text("Choose a solution to get started:")),
            Padding.center_90(Divider("\N{BOX DRAWINGS LIGHT HORIZONTAL}")),
            Padding.center_90(self.build_menuable_items()),
            Padding.line_break(""),
            Padding.center_20(self.buttons())
        ]
        super().__init__(ListBox(_pile))

    def _swap_focus(self):
        import q
        q(self._w)
        if self._w.focus_position == 2:
            self._w.focus_position = 4
        else:
            self._w.focus_position = 2

    def keypress(self, size, key):
        if key in ['tab', 'shift tab']:
            self._swap_focus()
        return super().keypress(size, key)

    def buttons(self):
        cancel = cancel_btn(on_press=self.cancel)

        buttons = [
            Color.button_secondary(cancel, focus_map='button_secondary focus')
        ]
        return Pile(buttons)

    def build_menuable_items(self):
        """ Builds a list of bundles available to install
        """
        bundles = self.common['config']['bundles']
        cols = []
        for bundle in bundles:
            cols.append(
                Columns(
                    [
                        ("weight", 0.2, Color.body(
                            menu_btn(label=bundle['name'],
                                     on_press=self.done),
                            focus_map="button_primary focus")),
                        ("weight", 0.3, Text(bundle['summary'],
                                             align="left"))
                    ],
                    dividechars=1
                )
            )
            cols.append(Padding.line_break(""))
        return BoxAdapter(SimpleList(cols),
                          height=len(cols)+2)

    def cancel(self, button):
        EventLoop.exit(0)

    def done(self, result):
        self.cb(result.label)
