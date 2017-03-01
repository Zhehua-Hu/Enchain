# ex: set ts=8 noet:

#_________________________________________
all: qt5

qt4: qt4py2

qt5: qt5py2

qt4py2:
	pyrcc4 -py2 -o resources.py resources.qrc

qt4py3:
	pyrcc4 -py3 -o resources.py resources.qrc

qt5py2:
	pyrcc5 -o resources.py resources.qrc

qt5py3:
	pyrcc5 -o resources.py resources.qrc

#_________________________________________
test: testpy2

testpy2:
	python -m unittest discover utest


testpy3:
	python3 -m unittest discover utest
.PHONY: test
