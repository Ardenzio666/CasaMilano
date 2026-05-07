from django import forms
from .models import DishComment

class DishCommentForm(forms.ModelForm):
    class Meta:
        model = DishComment
        fields = ["text"]

        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Scrivi il tuo commento..."
            }),
        }