def custom_sort(item):
    # Define key priority
    priority_keys = ['goodbarber-custom-features', 'goodbarber-api-integrations', 'goodbarber-internal-librairies']

    if item in priority_keys:
        # Priority higher 
        return priority_keys.index(item)
    else:
        # Priority lower
        return len(priority_keys)