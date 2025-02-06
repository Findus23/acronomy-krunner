#!/bin/env python3
import argparse
import webbrowser
from datetime import datetime, timedelta

import dbus.service
import requests
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DBusGMainLoop(set_as_default=True)

objpath = "/acronomy"

iface = "org.kde.krunner1"
s = requests.Session()
s.headers.update({'User-Agent': 'Acronomy Krunner'})


class LocalData:
    acronyms = {}
    last_updated = datetime.now()

    def __init__(self):
        self.fetch_data()

    def fetch_data(self):
        print("fetching data")
        r = s.get("https://acronomy.lw1.at/api/acronym/")
        self.acronyms = {}
        self.last_updated = datetime.now()
        for acro in r.json():
            self.acronyms[acro["name"].lower()] = acro

    def search(self, query: str):
        age = datetime.now() - self.last_updated
        if age > timedelta(hours=48):
            self.fetch_data()

        query = query.lower()
        for name, acro in self.acronyms.items():
            if query in name:
                yield acro


class Runner(dbus.service.Object):
    def __init__(self, args):
        self.args = args
        self.data = LocalData()
        dbus.service.Object.__init__(self, dbus.service.BusName("at.lw1.acronomy", dbus.SessionBus()), objpath)

    @dbus.service.method(iface, in_signature="s", out_signature="a(sssida{sv})")
    def Match(self, query: str):
        runners = []

        icon = "plasmagik"
        type = 100  # (Plasma::QueryType)
        relevance = 0.2  # 0-1

        for result in self.data.search(query):
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

    args = parser.parse_args()

    runner = Runner(args)
    loop = GLib.MainLoop()
    loop.run()


if __name__ == "__main__":
    main()
