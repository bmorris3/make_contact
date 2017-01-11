
import json
import sys

from .data import MoCInfo

__all__ = ['query_for_reps']


def vet_official_data(official):
    if (('phones' in official) and ('address' in official) and
            ('urls' in official)):
        return True
    return False


def get_members_of_congress(json_input):

    vetted_officials = [official for official in json_input['officials']
                        if vet_official_data(official)]

    officials_list = [MoCInfo.from_json(j) for j in vetted_officials]
    moc_list = [official for official in officials_list if official.is_MoC]

    return moc_list


def query_for_reps(address, key='AIzaSyBDUwLqoWAiAS4sTfFccdaz583W060jbok'):

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

        return get_members_of_congress(output)

    else:
        import urllib2

        data = urllib2.urlencode(payload)
        req = url + '?' + data

        with urllib2.urlopen(req) as response:
            output = json.loads(response.read().decode('ascii'))

        return get_members_of_congress(output)
