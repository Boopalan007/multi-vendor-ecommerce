
from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            'rating',
            'comment',
        ]

        labels = {
            'rating': 'Product Rating',
            'comment': 'Your Review',
        }

        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),

            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your product review here...',
                'rows': 4
            }),
        }
