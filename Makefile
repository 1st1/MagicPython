.PHONY: all test release devenv

all: devenv release

test: release
# Run python syntax tests
	./node_modules/.bin/syntaxdev test --tests test/**/*.py \
				--syntax grammars/src/MagicPython.syntax.yaml \
				--default-vars grammars/src/flags.json

# Run regex syntax tests
	./node_modules/.bin/syntaxdev test --tests test/**/*.re \
				--syntax grammars/src/MagicRegExp.syntax.yaml

# Check if the version specified in "package.json" matches the latest git tag
	@if [ \
		`cat package.json | grep -e '^[[:space:]]*"version":' | sed -e 's/[[:space:]]*"version":[[:space:]]*"\(.*\)",/\1/'` \
		!= \
		`git describe --tags --abbrev=0 | sed -e 's/v\([[:digit:]]\{1,\}\.[[:digit:]]\{1,\}\.[[:digit:]]\{1,\}\).*/\1/'` \
	] ; \
		then echo "Error: package.version != git.tag" && exit 1 ; fi

devenv:
	npm install syntaxdev@0.0.9

release:
# tmLanguages
	./node_modules/.bin/syntaxdev build-plist \
				--in grammars/src/MagicPython.syntax.yaml \
				--out grammars/MagicPython.tmLanguage \
				--default-vars grammars/src/flags.json

	./node_modules/.bin/syntaxdev build-plist \
				--in grammars/src/MagicPython.syntax.yaml \
				--out grammars/tpl/MagicPython.tmLanguage.tpl \
				--keep-conditions

	./node_modules/.bin/syntaxdev build-plist \
				--in grammars/src/MagicRegExp.syntax.yaml \
				--out grammars/MagicRegExp.tmLanguage

# CSON
	./node_modules/.bin/syntaxdev build-cson \
				--in grammars/src/MagicPython.syntax.yaml \
				--out grammars/MagicPython.cson \
				--default-vars grammars/src/flags.json

	./node_modules/.bin/syntaxdev build-cson \
				--in grammars/src/MagicPython.syntax.yaml \
				--out grammars/tpl/MagicPython.cson.tpl \
				--keep-conditions

	./node_modules/.bin/syntaxdev build-cson \
				--in grammars/src/MagicRegExp.syntax.yaml \
				--out grammars/MagicRegExp.cson

# SCOPES
	./node_modules/.bin/syntaxdev scopes \
				--syntax grammars/src/MagicPython.syntax.yaml > misc/scopes
