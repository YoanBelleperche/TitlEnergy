from django.shortcuts import render
from .forms import DataEntry
from .data.appliances import appliances, categories_duration_interval, minimum_consumption
import numpy as np
import json

def consumption(request):
    
    context = dict()
    context['minimum_consumption'] = minimum_consumption
    context['appliances'] = appliances
    print('minimum_consumption:', minimum_consumption)
    
    if request.method != 'POST':
        form = DataEntry()
    else:
        form = DataEntry(request.POST)
        if form.is_valid():
            
            # cleaning data from user
            cleaned_data = form.cleaned_data
            email = cleaned_data.pop('email')
            T = cleaned_data.pop('consumption') * 1000.
            
            print(email)
            category_consumption = dict()            
            for appliance_name, appliance_number in cleaned_data.items():
                appliance_category = appliances[appliance_name]['category']
                appliance_consumption = appliances[appliance_name]['power']
                
                toAdd = [appliance_consumption] * appliance_number
                category_consumption[appliance_category] = category_consumption.setdefault(appliance_category, []) + toAdd
                print(appliance_number, appliance_name, appliance_category, appliance_consumption)
            print(category_consumption)

            # intermediate calculations
            Ef = np.mean(category_consumption['F']) if category_consumption['F'] else 0.
            Ea = np.mean(category_consumption['A']) if category_consumption['A'] else 0.
            El = np.mean(category_consumption['L']) if category_consumption['L'] else 0.
        
            Fmin, Fmax = categories_duration_interval['F']
            Amin, Amax = categories_duration_interval['A']
            Lmin, Lmax = categories_duration_interval['L']
                        
            # minimization
            min = 75000.
            selectedDurations = {'F': None, 'A': None, 'L': None}
            for f in range(Fmin, Fmax+1):
                for a in range(Amin, Amax+1):
                    for l in range(Lmin, Lmax+1):
                        Ex = Ef*f + Ea*a + El*l
                        if Ex <= T:
                            if T - Ex < min:
                                min = Ex
                                selectedDurations['F'] = f
                                selectedDurations['A'] = a
                                selectedDurations['L'] = l
            
            min = int(min)
            print(T, Ef, Ea, El)
            print('minimized parameters:', min, selectedDurations['F'], selectedDurations['A'], selectedDurations['L'])
            print(cleaned_data)
            results = dict()
            for appliance_name, appliance_number in cleaned_data.items():
                if appliance_number == 0:
                    continue
                
                appliance_category = appliances[appliance_name]['category']   
                nbr_appliance = cleaned_data.get(appliance_name)            
                appliance_consumption = appliances[appliance_name]['power'] / len(category_consumption[appliance_category])
                appliance_watt_consumption = np.round(appliance_consumption * selectedDurations[appliance_category]) * nbr_appliance
                
                print(f'{appliance_name}: {appliance_watt_consumption}')
                results[appliance_name.capitalize()] = appliance_watt_consumption
            results['Total'] = T
            context['results'] = results
            
    context['form'] = form
    
    return render(request, 'consumption.html', context)