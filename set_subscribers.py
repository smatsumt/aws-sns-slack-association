#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Add "Events:" description. Print new template to stdout.
"""

import argparse
import yaml

TEMPLATE_HEAD = """      Events:
"""

TEMPLATE = """        {}:
          Type: SNS
          Properties:
            Topic: !Sub arn:aws:sns:${{AWS::Region}}:${{AWS::AccountId}}:{}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('setting_filename', type=str, help='setting.toml filename')
    parser.add_argument('template_base_filename', type=str, help='template-base.yaml filename')
    args = parser.parse_args()

    # Print template-base.yaml first
    for l in open(args.template_base_filename).readlines():
        print(l, end="")
    print(TEMPLATE_HEAD, end="")

    # Print "Events:" section based on the setting.yaml
    setting = yaml.safe_load(open(args.setting_filename))
    for sns_topic in setting["Relations"]:
        print(TEMPLATE.format(sns_topic, sns_topic))


if __name__ == '__main__':
    main()
