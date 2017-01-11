
import json
import sys
import os
import yaml

from .data import ContactInfo

__all__ = ['query_google_for_names', 'get_unitedstates_for_MoC', 'get_MoCs']


def query_google_for_names(address,
                           key='AIzaSyBDUwLqoWAiAS4sTfFccdaz583W060jbok'):

    py3 = sys.version_info >= (3, 0)

    url = 'https://www.googleapis.com/civicinfo/v2/representatives'

    payload = {'address': address,
               'includeOffices': 'True', 'levels': 'country',
               'key': key}

    if py3:
        import urllib.parse
        import urllib.request

        data = urllib.parse.urlencode(payload)
        req = url + '?' + data

        with urllib.request.urlopen(req) as response:
            output = json.loads(response.read().decode('ascii'))

    else:
        import urllib2

        data = urllib2.urlencode(payload)
        req = url + '?' + data

        with urllib2.urlopen(req) as response:
            output = json.loads(response.read().decode('ascii'))

    officials_list = [ContactInfo.from_google(j) for j in output['officials']]
    moc_list = [official for official in officials_list if official.is_MoC]
    name_list = [moc.name for moc in moc_list]

    return name_list


def get_unitedstates_for_MoC():
    # Get detailed data from unitedstates/congress-legislators

    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        'congress-legislators', 'legislators-current.yaml')

    with open(path, 'r') as stream:
        legislators = yaml.load(stream, Loader=yaml.Loader)

    # Make dictionary by name of current members of congress
    members_of_congress = {l['name']['official_full']: l['terms'][-1]
                           for l in legislators}

    return members_of_congress


def get_MoCs(address):
    list_of_names = query_google_for_names(address)

    mocs = []
    for name in list_of_names:
        moc_info = ContactInfo.from_unitedstates(name,
                                                 us_congress_data.data[name])
        mocs.append(moc_info)
    return mocs


class USCongress(object):
    def __init__(self):
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = get_unitedstates_for_MoC()
        return self._data

us_congress_data = USCongress()
