from gmltools.kegg import KEGGInterface
import json
import argparse
import multiprocessing as mp


def kegg_id_exists(kegg_id: str):
    print(kegg_id)
    result = {'id': kegg_id, 'exists': False}
    try:
        KEGGInterface.get(kegg_id)
    except RuntimeError:
        return result
    result['exists'] = True
    return result


def run(kegg_ids: list):
    with mp.Pool(processes=10) as pool:
        results = pool.map(kegg_id_exists, kegg_ids)
    with open('literature/henry_2010_KEGG_IDs_rules_exist.json', 'w') as _f:
        json.dump(results, _f, indent=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--kegg_ids', type=str, required=True,
                        help='KEGG reaction IDs (.json)')
    args = parser.parse_args()
    with open(args.kegg_ids, 'r') as _file:
        these_ids: list = json.load(_file)
    run(these_ids)
