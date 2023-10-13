from django import forms

from manger.models import Resume

from django.forms.widgets import NumberInput, RadioSelect, Select


class RangeInput(NumberInput):
    input_type = 'range'


class ResumeCreateForm(forms.ModelForm):
    # q1 = forms.CharField(label="Question 1")
    # q2 = forms.ChoiceField(label="Question 2")
    # q3 = forms.CharField(label="Question 3")
    # q4 = forms.CharField(label="Question 4", widget=RadioSelect)
    # q5 = forms.CharField(label="Question 5", widget=RadioSelect)
    # q6 = forms.CharField(label="Question 6", widget=RadioSelect)

    class Meta:
        model = Resume
        fields = [
            "fullname", "address", "mobile", "skills", "email", 'gender', 'age',
            # "openess", "neurotisum", "conscientiousness", "agreeableness", "extraversion",
            "resume",
            "q1", 'q2', 'q3', 'q4', 'q5', 'q6',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:

            if not isinstance(self.fields[field_name].widget, (RangeInput, )):
                self.fields[field_name].widget.attrs['class'] = 'form-control'
