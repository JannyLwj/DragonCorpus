#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class New_Project_Form(forms.Form):
    project_name = forms.CharField(max_length=35,required=True)
    project_description = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        project_description = self.cleaned_data['project_description']
        num_words = len(project_description.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return project_description