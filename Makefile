colon := :
$(colon) := :

all: example

example: example.py
	DEVITO_OPT=advanced \
	DEVITO_LANGUAGE=openmp \
	DEVITO_ARCH=gcc-11 \
	DEVITO_LOGGING=DEBUG \
	python example.py