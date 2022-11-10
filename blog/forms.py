from django import forms
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from blog.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        form_class = 'animate__animated animate__fadeInLeft'
        self.helper.add_input(Submit('submit', 'Submit'))