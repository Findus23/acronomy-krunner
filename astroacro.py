#!/bin/env python3
import webbrowser

import dbus.service
import requests
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DBusGMainLoop(set_as_default=True)

objpath = "/astroacro"

iface = "org.kde.krunner1"

s = requests.Session()


class Runner(dbus.service.Object):
    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName("net.astroacro", dbus.SessionBus()), objpath)

    @dbus.service.method(iface, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        """This method is used to get the matches and it returns a list of lists/tupels"""
        if " " in query:
            return []

        runners = []
        r = s.get("http://127.0.0.1:8000/api/acronym/", params={"search": query})
        icon = "internet-web-browser"
        type = 100  # (Plasma::QueryType)
        relevance = 1.0  # 0-1

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

    # @dbus.service.method(iface, out_signature='a(sss)')
    # def Actions(self):
    #     # id, text, icon
    #     return [("id", "Tooltip", "planetkde")]

    @dbus.service.method(iface, in_signature='ss')
    def Run(self, data: str, action_id: str):
        print(data, action_id)
        webbrowser.open("http://127.0.0.1:8000/acro/" + data)


runner = Runner()
loop = GLib.MainLoop()
loop.run()
