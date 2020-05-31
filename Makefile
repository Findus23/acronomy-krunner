install-config:
	mkdir -p ~/.local/share/kservices5/
	rm ~/.local/share/kservices5/plasma-runner-astroacro.desktop
	kquitapp5 krunner; kstart5 krunner
	cp plasma-runner-astroacro.desktop ~/.local/share/kservices5/
	kquitapp5 krunner; kstart5 krunner

create-autostart:
	# Configure the path in the .desktop file first
	mkdir -p ~/.config/autostart/
	cp astroacro_autostart.desktop ~/.config/autostart/
