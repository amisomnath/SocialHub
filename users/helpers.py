
def convert_user_gender(gender_text, is_user_friendly=False):
    if gender_text == 'Male' or gender_text == 'm':
        return 'm' if not is_user_friendly else 'Male'
    elif gender_text == 'Female' or gender_text == 'f':
        return 'f' if not is_user_friendly else 'Female'
    elif gender_text == 'Other' or gender_text == 'o':
        return 'o' if not is_user_friendly else 'Other'
    return None
