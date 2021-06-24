.PHONY: patch
patch:
	bumpversion patch
	git push
	git push --tag

.PHONY: minor
minor:
	bumpversion minor
	git push
	git push --tag

.PHONY: major
major:
	bumpversion major
	git push
	git push --tag

.PHONY: build
build:
	poetry build

.PHONY: publish
publish: build
	poetry publish
