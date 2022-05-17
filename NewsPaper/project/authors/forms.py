from django.forms import ModelForm, BooleanField
from news.models import Author


class AuthorForm(ModelForm):
    check_box = BooleanField(label='Подтвердить!')


    class Meta:
        model = Author
        fields = ['descriptionAuthor',
                  'nameAuthor',
                  'authorUser',
                  ]

