import requests
from urllib.parse import urljoin
import re
import json
import logging

def extract_lines(data: str, block: str):
    collected = []
    start = False
    pat = r'^' + block
    for line in data.splitlines():
        if start is True and re.search(r'^[A-Z]', line) is not None:
            # reset start to False if the block has been read
            # All the blocks are in capital letters
            start = False
        if start is True and line == '///':
            # reset start to False if the and of the data is reached
            start = False
        if re.search(pat, line) is not None:
            # put start to True once the block has been encountered
            start = True
        if start is True:
            collected.append(line)
    if len(collected) == 0:
        return []
    # remove block name from first line
    collected[0] = re.sub(pat, '', collected[0])
    # strip leading and trailing white spaces
    collected = [_.strip() for _ in collected]
    return collected


class KEGGReaction:
    def __init__(self, flat_file_data: str):
        self.raw = flat_file_data
        self.entry = extract_lines(flat_file_data, 'ENTRY')[0].split()[0]
        self.name = extract_lines(flat_file_data, 'NAME')
        self.definition = extract_lines(flat_file_data, 'DEFINITION')
        self.equation = extract_lines(flat_file_data, 'EQUATION')[0]  # there should only be one
        self.rclass = {_e.split()[0]: _e.split()[1].split('_')
                       for _e in extract_lines(flat_file_data, 'RCLASS')}
        self.enzyme = extract_lines(flat_file_data, 'ENZYME')
        self.pathway = extract_lines(flat_file_data, 'PATHWAY')
        self.ontology = extract_lines(flat_file_data, 'ORTHOLOGY')
        self.dblinks = extract_lines(flat_file_data, 'DBLINKS')
        self.comment = extract_lines(flat_file_data, 'COMMENT')
        self.remark = extract_lines(flat_file_data, 'REMARK')

    def __str__(self):
        return self.raw

    def extract_eq_cpds(self):
        items = self.equation.replace('+', '').split()
        arrow = next((_i for _i, _v in enumerate(items) if re.search(r'C\d\d\d\d\d', _v) is None), None)
        return {'lhs': items[:arrow], 'rhs': items[arrow + 1:]}


class KEGGInterface:
    @staticmethod
    def get(kegg_id: str) -> str:
        base_url = 'https://rest.kegg.jp/get/'
        url = urljoin(base_url, kegg_id)
        logging.info(f'Downloading KEGG data from {url}')
        result = requests.get(url)
        if result.status_code != 200:
            raise RuntimeError("Reaction Not Found.")
        return result.text

    @staticmethod
    def to_smiles(kegg_id: str) -> str:
        # convert KEGG to PubCHEM SID
        logging.info(f"Getting PubCHEM SID for {kegg_id}.")
        request_url = urljoin("https://rest.kegg.jp/conv/pubchem/", kegg_id)
        result_str = requests.get(request_url).text
        pc_sid = result_str.split("\t")[1][8:-1]

        # convert PubChem SID to PubChem CID
        logging.info(f"Getting PubCHEM CID for SID {pc_sid}.")
        request_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance" \
                      f"/sid/{pc_sid}/cids/json"
        result_str = requests.get(request_url).text
        pc_cid = json.loads(result_str)[
            "InformationList"]["Information"][0]["CID"][0]

        # get SMILES-String
        logging.info(f"Getting SMILES-String for CID {pc_cid}.")
        request_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound" \
                      f"/cid/{pc_cid}/property/CanonicalSmiles/json"
        result_str = requests.get(request_url).text
        smiles = json.loads(result_str)["PropertyTable"]["Properties"][0]["CanonicalSMILES"]
        return smiles
