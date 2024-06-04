PATH1 = stacks_analyzer/tree-sitter-clarity
PATH2 = .

.PHONY: venv fish bash ps1 csh install

default: bash

# ANSI escape codes for colors
GREEN = \033[0;32m
BLUE = \033[0;34m
NC = \033[0m

default: bash

venv:
	python3 -m venv venv

action: venv
	@echo -e  "${GREEN}======== Cloning tree-sitter grammar for Clarity ========${NC}"
	git submodule update --recursive
	@echo -e "${GREEN}======== Installing tree-sitter ========${NC}"
	cd $(PATH1)
	npm install tree-sitter-cli
	@echo -e "${GREEN}======== Installing tree-sitter grammar for Clarity ========${NC}"
	cd $(PATH1) && npx tree-sitter generate
	rm -fr node_modules
	./venv/bin/pip install $(PATH1)
	@echo -e "${GREEN}======== Installing Stacy for Clarity ========${NC}"
	./venv/bin/pip install $(PATH2)
	@echo -e "${GREEN}======== Running Stacy for Clarity ========${NC}"
	echo "\`\`\`" >  $(GITHUB_WORKSPACE)/report.out
	./venv/bin/stacy-analyzer lint $(INPUT_TARGET) >> $(GITHUB_WORKSPACE)/report.out
	echo "\`\`\`" >>  $(GITHUB_WORKSPACE)/report.out


install: venv
	@echo -e  "${GREEN}======== Cloning tree-sitter grammar for Clarity ========${NC}"
	git submodule update --recursive
	@echo -e "${GREEN}======== Installing tree-sitter grammar for Clarity ========${NC}"
	./venv/bin/pip install $(PATH1)
	@echo -e "${GREEN}======== Installing Stacy for Clarity ========${NC}"
	./venv/bin/pip install $(PATH2)

test: venv install
	@echo -e  "${GREEN}======== Testing detectors ========${NC}"
	./tests.sh

test_ci: venv
	@echo -e  "${GREEN}======== Cloning tree-sitter grammar for Clarity ========${NC}"
	git pull --recurse-submodules && git submodule update
	@echo -e "${GREEN}======== Installing tree-sitter ========${NC}"
	cd $(PATH1)
	npm install tree-sitter-cli
	@echo -e "${GREEN}======== Installing tree-sitter grammar for Clarity ========${NC}"
	cd $(PATH1) && npx tree-sitter generate
	rm -fr node_modules
	./venv/bin/pip install $(PATH1)
	@echo -e "${GREEN}======== Installing Stacy for Clarity ========${NC}"
	./venv/bin/pip install $(PATH2)
	@echo -e  "${GREEN}======== Testing detectors ========${NC}"
	./tests.sh > $(GITHUB_WORKSPACE)/test.out

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