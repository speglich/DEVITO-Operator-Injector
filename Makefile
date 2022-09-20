colon := :
$(colon) := :

all: example

example: example.py
	DEVITO_OPT=advanced \
	DEVITO_LANGUAGE=openmp \
	DEVITO_ARCH=gcc-11 \
	python example.py