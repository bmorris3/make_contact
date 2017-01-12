from wtforms import Form, validators
from wtforms.fields import RadioField, SelectField, StringField, TextAreaField
from wtforms.validators import ValidationError

from utils import query_google_for_names


def address_check(form, field):
    try:
        query_google_for_names(field.data)
    except:
        raise ValidationError("We couldn't process the address you entered. Sorry.")


class ContactForm(Form):
    name    = StringField('Name', [validators.DataRequired()], render_kw={"placeholder": "Brett Morris", "icon": "user"})
    title   = SelectField('Title (optional)', choices=[('', ''), ('Dr.', 'Dr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'),
                                                       ('Mr.', 'Mr.'), ('Mx.', 'Mx.')],
                          default='', render_kw={"icon": "graduation-cap"})
    affil   = StringField('Affiliation (optional)', render_kw={"placeholder": "University of Washington", "icon": "institution"})
    address = StringField('Address', [validators.DataRequired(), address_check],
                          render_kw={"placeholder": "60 Garden St, Cambridge MA 02138", "icon": "address-card"})
    stance  = RadioField('Stance', [validators.DataRequired()], choices=[('support', 'support'), ('oppose', 'oppose')],
                         default='support', render_kw={"style": "list-style-type:none; display:inline;", "icon": "thumbs-up"})
    subject = StringField('Subject', [validators.DataRequired()], render_kw={"placeholder": "House Bill 1234", "icon": "info-circle"})
    body    = TextAreaField('Body', [validators.DataRequired()],
                            render_kw={"placeholder": "Here are my great thoughts...", "rows":"8", "icon": "commenting"})
