import argparse
import json
import os
import sys

from gmltools.modimport import mod

stdout_fd = sys.stdout.fileno()
old_stdout = os.dup(stdout_fd)


def redirect_stdout():
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, stdout_fd)
    os.close(devnull)


def restore_stdout():
    os.dup2(old_stdout, stdout_fd)


def prefilter_compounds(data_path, multi_components):
    with open(data_path, 'r') as file:
        compound_data = json.load(file)

    compounds = []
    for compound in compound_data:
        cid = compound['id']
        if cid in multi_components:
            compound['smiles'] = multi_components[cid]
        if not compound['smiles']:
            continue
        compounds.append({i: j for i, j in compound.items() if i in ['id', 'name', 'smiles']})

    return compounds


def load_reactions(data_path, isomorphisms, compound_ids):
    with open(data_path, 'r') as file:
        reaction_data = json.load(file)

    reactions = []

    for reaction in reaction_data:
        if not reaction['ec']:
            continue
        if any(
                compound['id'] not in compound_ids
                for side in ['rhs', 'lhs']
                for compound in reaction['equation_decomposed'][side]
        ):
            continue
        reaction_data = {i: j for i, j in reaction.items() if i in ['id', 'equation_decomposed', 'ec']}
        reaction_data['to_lhs'] = False
        reaction_data['to_rhs'] = False
        if any(x in reaction['equation'] for x in ['<==>', '=', '<--']):
            reaction_data['to_lhs'] = True
        if any(x in reaction['equation'] for x in ['<==>', '=', '-->']):
            reaction_data['to_rhs'] = True
        reactions.append(reaction_data)

    return reactions


def get_isomorphisms(compounds):
    redirect_stdout()
    compounds = [mod.smiles(compound['smiles'], compound['id']) for compound in compounds]
    restore_stdout()
    settings = mod.LabelSettings(mod.LabelType.Term, mod.LabelRelation.Unification)
    mapping = {}
    while True:
        try:
            test = mod.DG(labelSettings=settings, graphDatabase=compounds)
            break
        except mod.LogicError as e:
            strings = str(e).split("'")
            id_one = strings[1]
            id_two = strings[3]
            if id_two in mapping.values():
                mapping[id_one] = id_two
                compounds = [x for x in compounds if x.name != id_one]
            else:
                mapping[id_two] = id_one
                compounds = [x for x in compounds if x.name != id_two]
    return mapping


def clean_data(reactions_path, compounds_path, config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)

    multi_components = {}
    if 'multi_components' in config:
        multi_components = config['multi_components']

    compounds = prefilter_compounds(compounds_path, multi_components)
    isomorphisms = get_isomorphisms(compounds)
    compounds = [compound for compound in compounds if compound['id'] not in isomorphisms]
    reactions = load_reactions(reactions_path,
                               isomorphisms,
                               [compound['id'] for compound in compounds])
    with open(reactions_path, 'w') as rfile, open(compounds_path, 'w') as cfile:
        json.dump(reactions, rfile, indent=4)
        json.dump(compounds, cfile, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Data Cleaner")
    parser.add_argument("-r", "--reacs", required=True)
    parser.add_argument("-c", "--chems", required=True)
    parser.add_argument("-cf", "--config", required=True)
    args = parser.parse_args()

    clean_data(args.reacs, args.chems, args.config)
