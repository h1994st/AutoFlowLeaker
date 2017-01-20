DIRS = auto_flow comb_coder ec_coder
CLEANDIRS = $(DIRS:%=clean-%)

.PHONY: subdirs $(CLEANDIRS)

clean: $(CLEANDIRS)
	rm -f *.pyc

$(CLEANDIRS):
	$(MAKE) -C $(@:clean-%=%) clean
