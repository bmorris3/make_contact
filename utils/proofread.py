
default_suggestions = """

Here are some suggestions that are useful for everyone:
- Please use a reliable spell-checker and grammar-checker before sending your email.
- Personalize your letter.
- Use factual evidence to support your stance.
- Be professional, courteous and concise.
- If you are sending a letter, use your letterhead if possible.
- If you are sending a letter, sign it; only one signatory per letter.
"""


class Proof(object):
    def __init__(self, text):
        self.valid = None
        self.text = text

    def gratitude(self):
        """Check that you thank the MoC"""
        test = ('thank' in self.text.lower()) or ('appreciate' in self.text.lower())
        message = 'Did you thank your member of Congress for their time?'
        return test, message

    def request_response(self):
        """Check that you asked for a response from the MoC"""
        phrases = ('will you', 'would you', 'your stance', 'are you', 'respon')
        test = any([phrase in self.text.lower() for phrase in phrases])
        message = 'Did you ask your member of Congress for a concrete response?'
        return test, message

    def get_suggestions(self):
        """Check for suggestions"""
        tests_to_run = [self.gratitude, self.request_response]

        all_suggestions = ""

        for test in tests_to_run:
            passes_test, message = test()
            if not passes_test:
                if len(all_suggestions) > 0:
                    all_suggestions += '<br><br>'
                all_suggestions += 'Suggestion: ' + message

        if len(all_suggestions) == 0:
            all_suggestions += ("Great job! You have no warnings.")

        all_suggestions += default_suggestions.replace('\n', '<br>')

        return all_suggestions

