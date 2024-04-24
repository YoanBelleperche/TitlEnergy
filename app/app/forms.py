from django import forms
from django.db import models
from .data.appliances import appliances


class DataEntry(forms.Form):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'] = forms.EmailField(required=True)
    
        for appliance in appliances:
            label = appliance.capitalize()
            self.fields[appliance] = forms.IntegerField(required=True, label=label, min_value=0, initial=0)
            
        self.fields['consumption'] = forms.FloatField(required=True, label='Consumption (kWh)', min_value=0., max_value=75., initial=0.)
            
    
    