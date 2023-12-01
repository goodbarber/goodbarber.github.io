def custom_sort(key, prioritized_list):
    try:
        # Prioritize specific names by assigning them a lower index
        return prioritized_list.index(key)
    except ValueError:
        # For other names, use a high index followed by the normal key
        return len(prioritized_list), key.lower()
