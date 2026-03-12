import numpy as np

def sanitize_output(value):
    if isinstance(value, (np.generic, np.ndarray)):
        return value.item() if np.isscalar(value) or value.size == 1 else value.tolist()
    
    if hasattr(value, "item") and not isinstance(value, (list, dict, str, np.ndarray)):
        return value.item()
    
    elif isinstance(value, list):
        return [sanitize_output(v) for v in value]
    
    elif isinstance(value, dict):
        return {k: sanitize_output(v) for k, v in value.items()}
    
    return value