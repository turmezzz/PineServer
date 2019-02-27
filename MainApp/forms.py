from django import forms


class ArchiveUploadForm(forms.Form):
    file = forms.FileField()

    def is_valid(self, keys=None):
        return 'archive' in keys

