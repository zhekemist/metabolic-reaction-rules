# --- IMPORTS ---
import argparse
import glob
import json
import os.path
import sys
import logging

from gmltools.modimport import mod, mod_loc
from gmltools.ruletest import RuleTest

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')


# --- MAIN PART ---

class TermColor:
    SUCCESS = '\x1b[1;32m'
    WARN = '\x1b[1;33m'
    ERROR = '\x1b[1;31m'
    RESET = '\x1b[0m'


def get_numbers(result):
    total = {'educt_missing': len(result['total']['educt_missing']),
             'product_missing': len(result['total']['product_missing'])}

    total_educt_surplus = set()
    total_product_surplus = set()
    for row in result['individual'].values():
        total_educt_surplus |= row['educt_surplus']
        total_product_surplus |= row['product_surplus']

    total['educt_surplus'] = len(total_educt_surplus)
    total['product_surplus'] = len(total_product_surplus)
    return total


def generate_report_str(result, ec_class):
    total = get_numbers(result)
    errors = sum(i for i in total.values())
    if errors > 0:
        report = TermColor.ERROR + f'ERROR - Rules for EC-class {ec_class}:\n' \
                                   f'\t> educt surplus = {total["educt_surplus"]}\n' \
                                   f'\t> educt missing = {total["educt_missing"]}\n' \
                                   f'\t> product surplus = {total["product_surplus"]}\n' \
                                   f'\t> product missing = {total["product_missing"]}' + TermColor.RESET
    else:
        report = TermColor.SUCCESS + f'SUCCESS - Rules for EC-class {ec_class} \u2714' + TermColor.RESET
    return report


def write_out(result, ec_class):
    data = {
        'total': {i: sorted(j) for i, j in result['total'].items()},
        'individual': {rn: {i: sorted(j) for i, j in r.items()} for rn, r in result['individual'].items()}
    }
    with open(f"test_out/{ec_class.replace('.', '_')}.json", "w") as file:
        json.dump(data, file, indent=4)


def run():
    parser = argparse.ArgumentParser(
        prog="Rule Test",
        description="Simple Test for GML rules"
    )
    parser.add_argument("ec_classes",
                        nargs='+',
                        type=str,
                        metavar="3rd level EC Class Code",
                        help="e.g. 1.1.1")
    parser.add_argument("-d", "--ruledir",
                        type=str,
                        help="dir/with/rules",
                        required=True)
    parser.add_argument("-r", "--reactions-data",
                        type=str,
                        required=True,
                        help="path/to/reaction_data.json"
                        )
    parser.add_argument("-c", "--compounds-data",
                        type=str,
                        required=True,
                        help="path/to/compound_data.json"
                        )
    parser.add_argument("-cf", "--config",
                        type=str,
                        help="path/to/test_config.json"
                        )
    parser.add_argument("--debug",
                        action="store_true",
                        help="enable debugging output"
                        )
    args = parser.parse_args()

    if args.debug:
        logging.root.setLevel(logging.DEBUG)

    rule_sets = {
        ec_class: glob.glob(os.path.join(args.ruledir, f'{ec_class.replace(".", "_")}_*.gml'))
        for ec_class in args.ec_classes
    }

    if not os.path.exists('./test_out'):
        os.makedirs('./test_out')

    for ec_class, rule_set in rule_sets.items():
        try:
            rule_set = [mod.Rule.fromGMLFile(path) for path in rule_set]
            rule_test = RuleTest(args.reactions_data, args.compounds_data, ec_class, args.config)
            result = rule_test.test_set_of_rules(rule_set)
            print(generate_report_str(result, ec_class))
            write_out(result, ec_class)

        except mod.InputError as e:
            print(f'Error while loading rule set for {ec_class}:', e, file=sys.stderr)
        except Exception as e:
            print(f'Unexpected error while testing rule {ec_class}:', e, file=sys.stderr)


if __name__ == '__main__':
    run()
