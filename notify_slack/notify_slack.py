#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import requests
import yaml


def lambda_handler(event, context):
    """
    Post SNS message to slack channel
    Preconditions:
    - "setting.yaml" is located in same directory.

    :param event: the lambda assumes event is related with SNS
    :param context: (not used)
    :return: (none)
    """
    settings = yaml.safe_load(open("setting.yaml"))

    # find appropriate Slack WebHook URLs
    sns_dict = event["Records"][0]["Sns"]
    topic_name = sns_dict["TopicArn"].split(":")[5]
    targets = settings["Relations"][topic_name]
    if not isinstance(targets, list):  # if target is not list, pack it
        targets = [targets]

    # post Slack WebHook URL with SNS Message
    data = parse_message(sns_dict["Message"])
    for slack_webhook in targets:
        r = requests.post(slack_webhook, data=data)


def parse_message(message: str) -> str:
    """ Adapt message to Slack WebHook JSON """
    try:
        # if message seems to Slack Webhook JSON, return it.
        message_dict = json.loads(message)
        if "text" in message_dict:
            return message
    except Exception:
        pass
    # if not, treat message as normal text.
    return json.dumps({"text": message})
