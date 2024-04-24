appliances = {
    'fridge': { 'category': 'F', 'power': 2000 },
    'washing machine': { 'category': 'A', 'power': 1500 },
    'tv': { 'category': 'L', 'power': 500 },
    'freezer': { 'category': 'F', 'power': 2500 },
    'dishwahser': { 'category': 'A', 'power': 2500 },
    'induction stove': { 'category': 'A', 'power': 3000 },
    'small light': { 'category': 'L', 'power': 100 },
    'big light': { 'category': 'L', 'power': 800 }
}

categories_duration_interval = {
    'F': (6, 8),
    'A': (1, 4),
    'L': (4, 24)
}

minimum_consumption = {
    appliance_name: {
        'power': appliances_data['power']*categories_duration_interval[appliances_data['category']][0],
        'category': appliances_data['category']
    } for appliance_name, appliances_data in appliances.items()
}