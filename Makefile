define release
$1:
	bump2version $$@
	git push --tag
endef


$(foreach part,patch minor major,$(eval $(call release,$(part))))


.PHONY: build
build:
	poetry build


.PHONY: publish
publish: build
	poetry publish
