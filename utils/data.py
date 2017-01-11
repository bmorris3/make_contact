

__all__ = ['ContactInfo']


class ContactInfo(object):
    def __init__(self, name=None, phone=None, address=None, url=None,
                 title=None, is_MoC=None, party=None):
        self.name = name
        self.phone = phone
        self.address = address
        self.url = url
        self._is_MoC = is_MoC
        self._title = title
        self.party = party

    @classmethod
    def from_google(cls, json_input):

        if 'line2' in json_input['address'][0]:
            json_input['address'][0]['line1'] += ', ' + json_input['address'][0]['line2']

        address = ', '.join([json_input['address'][0]['line1'],
                             (json_input['address'][0]['city'] + ' ' +
                              json_input['address'][0]['state']),
                             json_input['address'][0]['zip']])

        if 'urls' in json_input:
            url = json_input['urls'][0]
        else:
            url = None

        return cls(name=json_input['name'],
                   phone=None if 'phones' not in json_input else json_input['phones'][0],
                   address=address, url=url)

    @classmethod
    def from_unitedstates(cls, name, dict_input):

        title = 'Senator' if dict_input['type'].lower() == 'sen' else 'Representative'

        if 'contact_form' in dict_input:
            url = dict_input['contact_form']
        elif 'url' in dict_input:
            url = dict_input['url']
        else:
            url = None

        return cls(name=name, phone=dict_input['phone'],
                   address=dict_input['address'],
                   url=url, party=dict_input['party'],
                   title=title, is_MoC=True)

    def letter_address(self):
        return '\n'.join([self.name,
                          '\n'.join(self.address.split(', ')),
                          self.phone])

    @property
    def is_MoC(self):
        if self._is_MoC is None:
            self._is_MoC = (('senate' in self.address.lower()) or
                            ('house' in self.address.lower() or
                             'sob' in self.address.lower() or
                             'hob' in self.address.lower()) and
                            not ('white' in self.address.lower()))
            print(self._is_MoC)
        return self._is_MoC

    @property
    def title(self):
        if self._title is None:
            if 'senate' in self.address.lower() or 'SOB' in self.address:
                self._title = 'Senator'
            elif 'house' in self.address.lower() or 'HOB' in self.address:
                self._title = "Representative"

        return self._title
