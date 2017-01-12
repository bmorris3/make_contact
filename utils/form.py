from wtforms import Form, validators
from wtforms.fields import RadioField, SelectField, StringField, TextAreaField

class ContactForm(Form):
    name    = StringField('Name', [validators.DataRequired()], render_kw={"placeholder": "Brett Morris"})
    title   = SelectField('Title (optional)', choices=[('', ''), ('Dr.', 'Dr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'),
                                                       ('Mr.', 'Mr.'), ('Mx.', 'Mx.')],
                          default='')
    affil   = StringField('Affiliation (optional)', render_kw={"placeholder": "University of Washington"})
    address = StringField('Address', [validators.DataRequired()], render_kw={"placeholder": "60 Garden St, Cambridge MA 02138"})
    stance  = RadioField('Stance', [validators.DataRequired()], choices=[('support', 'support'), ('oppose', 'oppose')],
                         default='support', render_kw={"style": "list-style-type:none; display:inline;"})
    subject = StringField('Subject', [validators.DataRequired()], render_kw={"placeholder": "House Bill 1234"})
    body    = TextAreaField('Body', [validators.DataRequired()], render_kw={"placeholder": "Here are my great thoughts...", "rows":"8"})