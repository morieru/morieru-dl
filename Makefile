.PHONY: all
all:

.PHONY: env
env:
	pip install -r requirements.txt -r requirements-dev.txt

.PHONY: lock
lock: cleanenv
	pip install -r requirements.txt
	pip freeze > requirements.lock

.PHONY: cleanenv
cleanenv:
	pip freeze > freeze.tmp
	if [ -s freeze.tmp ]; then \
		pip uninstall -y -r freeze.tmp; \
	fi
	$(RM) freeze.tmp

# git archive HEAD
.PHONY: archive
archive:
	git archive HEAD -o sources.zip
