#!/usr/bin/env python3

from datetime import datetime

import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gio, GLib, Gtk


APP_ID = "com.jfscorreia.usersList"


class WViewerWindow(Adw.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application)
        self.set_title("Utilizadores ligados")
        self.set_default_size(480, 360)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(content)

        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="Utilizadores ligados"))
        content.append(header)

        refresh_button = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        refresh_button.set_tooltip_text("Atualizar resultado")
        refresh_button.connect("clicked", self._refresh)
        header.pack_end(refresh_button)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        content.append(scrolled_window)

        self.output_view = Gtk.TextView()
        self.output_view.set_editable(False)
        self.output_view.set_cursor_visible(False)
        self.output_view.set_monospace(True)
        self.output_view.set_wrap_mode(Gtk.WrapMode.NONE)
        self.output_view.set_left_margin(16)
        self.output_view.set_right_margin(16)
        self.output_view.set_top_margin(16)
        self.output_view.set_bottom_margin(16)
        scrolled_window.set_child(self.output_view)

        self.status_label = Gtk.Label(xalign=0)
        self.status_label.set_margin_start(16)
        self.status_label.set_margin_end(16)
        self.status_label.set_margin_top(8)
        self.status_label.set_margin_bottom(12)
        content.append(self.status_label)

        self._refresh()

    def _refresh(self, _button=None):
        try:
            bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
            sessions = bus.call_sync(
                "org.freedesktop.login1",
                "/org/freedesktop/login1",
                "org.freedesktop.login1.Manager",
                "ListSessions",
                None,
                GLib.VariantType.new("(a(susso))"),
                Gio.DBusCallFlags.NONE,
                5000,
                None,
            )
            users = set()
            for _, _, username, _, session_path in sessions.unpack()[0]:
                session_class = bus.call_sync(
                    "org.freedesktop.login1",
                    session_path,
                    "org.freedesktop.DBus.Properties",
                    "Get",
                    GLib.Variant(
                        "(ss)",
                        ("org.freedesktop.login1.Session", "Class"),
                    ),
                    GLib.VariantType.new("(v)"),
                    Gio.DBusCallFlags.NONE,
                    5000,
                    None,
                ).unpack()[0]
                if session_class == "user":
                    users.add(username)
        except GLib.Error as error:
            self._show_error(
                f"Não foi possível consultar as sessões do sistema: {error.message}"
            )
            return

        output = "\n".join(sorted(users, key=str.casefold))
        if not output:
            output = "Nenhum utilizador ligado."
        self.output_view.get_buffer().set_text(output)
        updated_at = datetime.now().astimezone().strftime("%H:%M:%S")
        self.status_label.set_text(f"Atualizado às {updated_at}")

    def _show_error(self, message):
        self.output_view.get_buffer().set_text(message)
        self.status_label.set_text("Falha ao atualizar")


class WViewerApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

    def do_activate(self):
        window = self.props.active_window
        if window is None:
            window = WViewerWindow(self)
        window.present()


def main():
    app = WViewerApplication()
    return app.run(None)


if __name__ == "__main__":
    raise SystemExit(main())
