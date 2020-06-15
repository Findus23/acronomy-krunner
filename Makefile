install-config:
	mkdir -p ~/.local/share/kservices5/
	rm -f ~/.local/share/kservices5/plasma-runner-acronomy.desktop
	kquitapp5 krunner; kstart5 krunner
	cp plasma-runner-acronomy.desktop ~/.local/share/kservices5/
	kquitapp5 krunner; kstart5 krunner

create-autostart:
	mkdir -p ~/.config/autostart/
	cp astroacro.desktop ~/.config/autostart/
