all: gui.py

clean:
	rm -f gui.py
	rm -f *.pyc

gui.py:gui.ui
	pyuic5 gui.ui  > gui.py
