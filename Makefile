.PHONY: clean release

clean:
	python scripts/release.py clean

release:
	python scripts/release.py release
