TS_CLARITY_PATH = src/stacy_analyzer/tree-sitter-clarity
REPO_ROOT = .

.PHONY: venv fish bash ps1 csh install test_ci
.SILENT: unittest

# ANSI escape codes for colors
GREEN = \033[0;32m
BLUE = \033[0;34m
NC = \033[0m

default: bash

venv:
	python3 -m venv venv > /dev/null 2>&1

install: venv
	@echo -e  "${GREEN}======== Removing previous install of Stacy ========${NC}"
	./venv/bin/pip uninstall stacy-analyzer -y
	@echo -e  "${GREEN}======== Cloning tree-sitter grammar for Clarity ========${NC}"
	git submodule update --recursive
	@echo -e "${GREEN}======== Installing tree-sitter grammar for Clarity ========${NC}"
	./venv/bin/pip install $(TS_CLARITY_PATH)
	@echo -e "${GREEN}======== Installing Stacy for Clarity ========${NC}"
	./venv/bin/pip install $(REPO_ROOT)

test_ci: venv
	@echo -e  "${GREEN}======== Cloning tree-sitter grammar for Clarity ========${NC}"
	git submodule update --init --remote --recursive
	@echo -e "${GREEN}======== Installing tree-sitter grammar for Clarity ========${NC}"
	./venv/bin/pip install git+https://github.com/xlittlerag/tree-sitter-clarity.git@6eb27feb606856e94bc0948b62c6ae2cb05a9700
	@echo -e "${GREEN}======== Installing Stacy for Clarity ========${NC}"
	./venv/bin/pip install $(REPO_ROOT)
	@echo -e  "${GREEN}======== Testing detectors ========${NC}"
	make unittest > $(GITHUB_WORKSPACE)/test.out 2>&1

unittest: venv
	./venv/bin/pip uninstall stacy-analyzer -y
	git submodule update --recursive
	./venv/bin/pip install $(TS_CLARITY_PATH)
	./venv/bin/pip install $(REPO_ROOT)
	cd tests/ && python3 -m unittest test_module1

fish: venv
	@echo -e "${BLUE}======== Using Fish shell ========${NC}"
	. venv/bin/activate.fish && make install

bash: venv
	@echo -e "${BLUE}======== Using Bash shell ========${NC}"
	. venv/bin/activate && make install

ps1: venv
	@echo -e "${BLUE}======== Using PowerShell ========${NC}"
	venv\Scripts\Activate.ps1; make install

csh: venv
	@echo -e "${BLUE}======== Using C shell ========${NC}"
	. venv/bin/activate.csh && make install