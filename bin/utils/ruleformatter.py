import os
import argparse
from gmltools.modimport import mod

parser = argparse.ArgumentParser(prog="GML Rule Formatter",
                                 description="Properly formats all the GML rules in the given directory.")
parser.add_argument("-d", "--directory", required=True)
args = parser.parse_args()
rdir = args.directory
rules = [f for f in os.listdir(rdir)]


def format_template(raw_string):
    start = raw_string.find('{Template}') + 10
    end = raw_string.find('{Group:', start)
    end = end if end != -1 else len(raw_string)
    rule_str = mod.ruleGMLString(raw_string[start:end]).getGMLString()
    new_str = '{Template}\n\n' + rule_str + '\n\n'
    if end != len(raw_string):
        new_str += raw_string[end:]
    return new_str


for rule_path in rules:
    try:
        with open(f"{rdir}/" + rule_path, 'r') as f:
            raw_string = f.read()
        if '{Template}' in raw_string:
            rule_str = format_template(raw_string)
        else:
            rule = mod.ruleGMLString(raw_string)
            rule_str = rule.getGMLString()
        with open(f"{rdir}/{rule_path}", "w") as f:
            f.write(rule_str)
    except Exception as e:
        print(f"Error with {rule_path}: {e}")
