import re

with open('fuzzy_engine.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_func = '''
def get_thresholds():
    """
    Extracts the numerical boundaries [a, b, c, d] for all membership functions.
    """
    thresholds = {}
    for var_name, var in variables.items():
        if var_name == 'risk': continue
        thresholds[var_name] = {}
        for cat_name, term in var.terms.items():
            try:
                mf = term.mf
                universe = var.universe
                # Find indices where mf > 0 and mf == 1
                gt_0 = np.where(mf > 0.001)[0]
                eq_1 = np.where(mf >= 0.999)[0]
                
                if len(gt_0) == 0 or len(eq_1) == 0:
                    thresholds[var_name][cat_name] = "Unknown"
                    continue
                
                a = universe[gt_0[0]]
                b = universe[eq_1[0]]
                c = universe[eq_1[-1]]
                d = universe[gt_0[-1]]
                
                thresholds[var_name][cat_name] = [round(float(x), 1) for x in [a, b, c, d]]
            except Exception as e:
                thresholds[var_name][cat_name] = "Error"
    return thresholds
'''

if 'def get_thresholds()' not in content:
    content += '\n' + new_func + '\n'

with open('fuzzy_engine.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS")
