import re
import numpy as np

def extract_features(password):
    features = {
        'length': len(password),
        'has_digits': any(c.isdigit() for c in password),
        'has_upper': any(c.isupper() for c in password),
        'has_lower': any(c.islower() for c in password),
        'has_symbol': any(not c.isalnum() for c in password),
        'is_year': bool(re.search(r'(19|20)\d{2}', password)),
        'is_qwerty': 'qwerty' in password.lower(),
        'is_name_digit': bool(re.match(r'[a-zA-Z]{3,}\d{2,}', password)),
        'only_digits': password.isdigit()
    }
    return np.array(list(features.values()), dtype=int).reshape(1, -1)

def classify_password(password):
    X = extract_features(password)
    # Если шаблон "опасный" — вернём True
    score = X[0][6] or X[0][7] or X[0][8]
    return bool(score)
