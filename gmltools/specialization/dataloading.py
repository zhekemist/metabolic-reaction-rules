import json

from gmltools.ruletest.ruletest import redirect_stdout, restore_stdout
from common import *


# --- DATA LOADING ---

class DataLoader:
    def __init__(self, reactions_path, compounds_path, ec_class, config_path=None):
        if config_path and False: # TODO: only temporary fix
            with open(config_path, 'r') as file:
                config = json.load(file)
        else:
            config = {'cofactors': [], 'cofactor_ids': []}

        cofactor_ids = set(config['cofactor_ids'])

        redirect_stdout()
        self.cofactors = [convert_modgraph_to_ig_graph(mod.graphDFS(i, i)) for i in config['cofactors']]
        self.cofactor_ids = set(config['cofactors'])
        self.load_compounds(compounds_path, cofactor_ids)
        self.load_reactions(reactions_path, ec_class, cofactor_ids)
        restore_stdout()

    def load_compounds(self, data_path, cofactor_ids):
        with open(data_path, 'r') as file:
            compound_data = json.load(file)

        compounds = {}
        for compound in compound_data:
            cid = compound['id']
            if cid in cofactor_ids:
                continue
            compounds[cid] = convert_modgraph_to_ig_graph(
                mod.Graph.fromSMILES(compound['smiles'], cid)
            )
        self.compounds = compounds

    def load_reactions(self, data_path, ec_class, cofactor_ids):
        with open(data_path, 'r') as file:
            reaction_data = json.load(file)

        reactions = []

        for reaction in reaction_data:
            if any(i.startswith(ec_class) for i in reaction['ec']):
                side_data = {
                    side: {i['id']
                           for i in reaction['equation_decomposed'][side]
                           if i['id'] not in cofactor_ids}
                    for side in ['lhs', 'rhs']
                }
                for side in ['rhs', 'lhs']:
                    other = 'rhs' if side == 'lhs' else 'lhs'
                    if reaction['to_' + side]:
                        reactions.append({
                            'educts': side_data[other],
                            'products': side_data[side]
                        })

        self.reactions = reactions
