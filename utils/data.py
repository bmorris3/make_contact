
__all__ = ['MoCInfo']


class MoCInfo(object):
    def __init__(self, name=None, phone=None, address=None, url=None):
        self.name = name
        self.phone = phone
        self.address = address
        self.url = url
        self._is_MoC = None
        self._title = None

    @classmethod
    def from_json(cls, json_input):

        if 'line2' in json_input['address'][0]:
            json_input['address'][0]['line1'] += ', ' + json_input['address'][0]['line2']


        print(json_input['address'][0]['line1'])

        address = ', '.join([json_input['address'][0]['line1'],
                             (json_input['address'][0]['city'] + ' ' +
                              json_input['address'][0]['state']),
                             json_input['address'][0]['zip']])

        if 'urls' in json_input:
            url = json_input['urls'][0]

        return cls(name=json_input['name'], phone=json_input['phones'][0],
                   address=address, url=url)

    def letter_address(self):
        return '\n'.join([self.name,
                          '\n'.join(self.address.split(', ')),
                          self.phone])

    @property
    def is_MoC(self):
        if self._is_MoC is None:
            self._is_MoC = (('senate' in self.address.lower()) or
                            ('house' in self.address.lower() or
                             'SOB' in self.address or
                             'HOB' in self.address) and
                            not ('white' in self.address.lower()))
        return self._is_MoC

    @property
    def title(self):
        if self._title is None:
            if 'senate' in self.address.lower() or 'SOB' in self.address:
                self._title = 'Senator'
            elif 'house' in self.address.lower() or 'HOB' in self.address:
                self._title = "Representative"

        return self._title


