#
# sns-slack-association Makefile
#

SRC=$(wildcard notify_slack/*.py)

deploy: build
	sam deploy

init: build
	sam deploy --guided --no-execute-changeset

build: template.yaml $(SRC)
	cp -a setting.yaml notify_slack/
	sam build --use-container
#	sam build  # you can use this if you have not any trouble

template.yaml: setting.yaml template-base.yaml set_subscribers.py
	./set_subscribers.py setting.yaml template-base.yaml > template.yaml
