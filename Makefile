install-config:
	mkdir -p ~/.local/share/krunner/dbusplugins
	cp plasma-runner-acronomy.desktop ~/.local/share/krunner/dbusplugins/plasma-runner-acronomy.desktop
	kquitapp6 krunner

create-autostart:
	echo "[D-BUS Service]\nName=at.lw1.acronomy\nExec=\"/home/lukas/PycharmProjects/acronomy-krunner/acronomy.py\"" > ~/.local/share/dbus-1/services/lw1.at.acronomy.service
