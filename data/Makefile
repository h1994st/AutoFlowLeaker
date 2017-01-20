DIRS = nlp
CLEANDIRS = $(DIRS:%=clean-%)

.PHONY: subdirs $(CLEANDIRS)

clean: $(CLEANDIRS)
	rm -f temp.*

$(CLEANDIRS):
	$(MAKE) -C $(@:clean-%=%) clean
