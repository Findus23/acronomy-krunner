#!/bin/env python3
import argparse
import webbrowser

import dbus.service
import requests
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DBusGMainLoop(set_as_default=True)

objpath = "/acronomy"

iface = "org.kde.krunner1"

s = requests.Session()


class Runner(dbus.service.Object):
    def __init__(self, args):
        self.args = args
        dbus.service.Object.__init__(self, dbus.service.BusName("net.acronomy", dbus.SessionBus()), objpath)

    @dbus.service.method(iface, in_signature="s", out_signature="a(sssida{sv})")
    def Match(self, query: str):

        if not self.args.less_privacy:
            if not query.startswith(self.args.keyword):
                return []
            query = query.replace(self.args.keyword + " ", "")

        if " " in query:
            return []

        runners = []
        r = s.get("https://acronomy.lw1.at/api/acronym/", params={"search": query})
        icon = "plasmagik"
        type = 100  # (Plasma::QueryType)
        relevance = 0.2  # 0-1

        for result in r.json():
            data = result["slug"]
            display_text = result["name"] + ": " + result["full_name"]
            properties = {
                "subtext": ", ".join(result["tags"]),
                # "category": "",
                # "urls": ""
            }
            runners.append((data, display_text, icon, type, relevance, properties))
        return runners

    # @dbus.service.method(iface, out_signature="a(sss)")
    # def Actions(self):
    #     # id, text, icon
    #     return [("id", "Tooltip", "planetkde")]

    @dbus.service.method(iface, in_signature="ss")
    def Run(self, data: str, action_id: str) -> None:
        webbrowser.open("https://acronomy.lw1.at/acronym/" + data)


def main():
    parser = argparse.ArgumentParser(description="acrronomy krunner background task")
    parser.add_argument("-k", "--keyword", action="store", default="acr")
    parser.add_argument("-l", "--less-privacy", action="store_true", default=False)

    args = parser.parse_args()

    runner = Runner(args)
    loop = GLib.MainLoop()
    loop.run()


if __name__ == "__main__":
    main()
