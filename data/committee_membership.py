import json
import numpy as np

committees_file = 'congressional_committees.json'


def load_committees(fname):
    """load json file into dictionary"""
    with open(fname, 'r') as inp:
        cdict = json.load(inp)
    return cdict


def committee_membership(member, congress='114'):
    """Supply member name "first last" and retreive membships from committees_file"""
    member = member.upper()
    committees = []
    cdict = load_committees(committees_file)
    chambers = cdict['congress'][congress]['chamber']
    for chamber, committees_dict in chambers.items():
        for committee_dict in committees_dict.values():
            for committee in committee_dict.keys():
                chairs = committee_dict[committee]['members']
                msg = 'in'
                if member in chairs:
                    msg = 'chair of'
                    print('{} is {} {} commitee on {}'.format(member, msg, chamber, committee))
                    committees.append(committee)
                for sub, members in committee_dict[committee]['subcommittee'].items():
                    if member in members['members']:
                        print('{} is {} {} {} subcommitee {}'.format(member, msg, chamber, committee, sub))
                        committees.append('{}: {}'.format(committee, sub))
    if len(committees) == 0:
        print('{} is not in any currently tracked committee')
    return committees
