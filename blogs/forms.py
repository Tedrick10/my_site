from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update({'class': 'form-username', 'placeholder': 'Enter your name'})
        self.fields['user_email'].widget.attrs.update({'class': 'form-useremail', 'placeholder': 'Enter your email'})
        self.fields['text'].widget.attrs.update({'class': 'form-textinput', 'placeholder': 'Enter your comment'})
    
    class Meta:
        model = Comment
        exclude = ["post"]
        # labels = {
        #     "user_name": "Your Name",
        #     "user_email": "Your Email",
        #     "text": "Your Comment",
        # }
        