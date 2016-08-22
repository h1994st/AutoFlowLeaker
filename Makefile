DIRS = data
CLEANDIRS = $(DIRS:%=clean-%)

.PHONY: subdirs $(CLEANDIRS)

clean: $(CLEANDIRS)
	rm -f *.pyc
	rm -f temp.*

$(CLEANDIRS):
	$(MAKE) -C $(@:clean-%=%) clean

init:
	mkdir -pv data

clean-log:
	rm -f *.log
