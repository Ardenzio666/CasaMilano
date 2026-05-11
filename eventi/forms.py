from django import forms

from eventi.models import EventComment

class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ["text"]

        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Scrivi il tuo commento..."
            }),
        }