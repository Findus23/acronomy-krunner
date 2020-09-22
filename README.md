## Acronomy Krunner plugin

![screenshot](screenshot.png)

This plugin allows to quickly look up an acronym on [Acronomy](https://acronomy.lw1.at/) directly from the Krunner KDE plasma search.

#### Installation

- copy the `plasma-runner-acronomy.desktop` file to `~/.loc al/share/kservices5/`
- restart krunner: `kquitapp5 krunner; kstart5 krunner`

The `acronomy.py` script needs to run permanently in the background to fetch the results.

One easy way to accomplish this is to copy the `acronomy.desktop` to `~/.config/autostart/`.

No search queries are sent to the Acronomy server. Instead a list of all acronyms is fetched and searched locally.

This plugin uses the [Astroacro API](https://acronomy.lw1.at/api/). ([Privacy Policy](http://lw1.at/i))


--------------------

based on [Krunner Python Plugin](https://store.kde.org/p/1333634/) by Alexander Lohnau licenced under  GPLv2 or later 
