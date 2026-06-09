import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Define Variables
variables = {
    'hb': ctrl.Antecedent(np.arange(0, 25.1, 0.1), 'hb'),
    'wbc': ctrl.Antecedent(np.arange(0, 50.1, 0.1), 'wbc'),
    'plt': ctrl.Antecedent(np.arange(0, 1001, 1), 'plt'),
    'neu': ctrl.Antecedent(np.arange(0, 100.1, 0.1), 'neu'),
    'mcv': ctrl.Antecedent(np.arange(50, 131, 1), 'mcv'),
    'rdw': ctrl.Antecedent(np.arange(10, 30.1, 0.1), 'rdw'),
    'egfr': ctrl.Antecedent(np.arange(0, 151, 1), 'egfr'),
    'creat': ctrl.Antecedent(np.arange(0, 401, 1), 'creat')
}

hb = variables['hb']
wbc = variables['wbc']
plt = variables['plt']
neu = variables['neu']
mcv = variables['mcv']
rdw = variables['rdw']
egfr = variables['egfr']
creat = variables['creat']

risk = ctrl.Consequent(np.arange(0, 101, 1), 'risk')

# 2. Define Membership Functions
# Standard Variables (Clinical Reference Ranges)
hb['Low'] = fuzz.trapmf(hb.universe, [0, 0, 11.0, 13.0])
hb['Normal'] = fuzz.trapmf(hb.universe, [11.0, 13.0, 17.5, 19.5])
hb['High'] = fuzz.trapmf(hb.universe, [17.5, 19.5, 25, 25])

wbc['Low'] = fuzz.trapmf(wbc.universe, [0, 0, 3.0, 4.0])
wbc['Normal'] = fuzz.trapmf(wbc.universe, [3.0, 4.0, 11.2, 13.0])
wbc['High'] = fuzz.trapmf(wbc.universe, [11.2, 13.0, 50, 50])

plt['Low'] = fuzz.trapmf(plt.universe, [0, 0, 100, 150])
plt['Normal'] = fuzz.trapmf(plt.universe, [100, 150, 400, 450])
plt['High'] = fuzz.trapmf(plt.universe, [400, 450, 1000, 1000])

neu['Low'] = fuzz.trapmf(neu.universe, [0, 0, 35.0, 40.0])
neu['Normal'] = fuzz.trapmf(neu.universe, [35.0, 40.0, 75.0, 80.0])
neu['High'] = fuzz.trapmf(neu.universe, [75.0, 80.0, 100, 100])

mcv['Low'] = fuzz.trapmf(mcv.universe, [50, 50, 75, 80])
mcv['Normal'] = fuzz.trapmf(mcv.universe, [75, 80, 96, 100])
mcv['High'] = fuzz.trapmf(mcv.universe, [96, 100, 130, 130])

rdw['Normal'] = fuzz.trapmf(rdw.universe, [0, 0, 14.8, 16.0])
rdw['High'] = fuzz.trapmf(rdw.universe, [14.8, 16.0, 30, 30])

# Data-Driven Variables (FCM Cluster Centers)
egfr['Severe'] = fuzz.trapmf(egfr.universe, [0, 0, 32.15, 60.78])
egfr['Moderate'] = fuzz.trimf(egfr.universe, [32.15, 60.78, 100.35])
egfr['Normal'] = fuzz.trapmf(egfr.universe, [60.78, 100.35, 150, 150])

creat['Normal'] = fuzz.trapmf(creat.universe, [0, 0, 96.15, 163.63])
creat['Moderate'] = fuzz.trimf(creat.universe, [96.15, 163.63, 219.93])
creat['Severe'] = fuzz.trapmf(creat.universe, [163.63, 219.93, 400, 400])

# Risk Score
risk['Normal'] = fuzz.trapmf(risk.universe, [0, 0, 20, 40])
risk['Mild'] = fuzz.trimf(risk.universe, [20, 40, 60])
risk['Moderate'] = fuzz.trimf(risk.universe, [40, 60, 80])
risk['Severe'] = fuzz.trapmf(risk.universe, [60, 80, 100, 100])

# 3. The Knowledge Base and Execution Context
risk_sim = None

def build_system():
    global risk_sim
    rules = [
        # 1. Baseline
        ctrl.Rule(hb['Normal'] & wbc['Normal'] & plt['Normal'] & neu['Normal'] & mcv['Normal'] & rdw['Normal'] & egfr['Normal'] & creat['Normal'], risk['Normal']),
        
        # 2-16. Single Variable Deviations
        ctrl.Rule(hb['Low'] & rdw['Normal'], risk['Mild']),
        ctrl.Rule(hb['High'] & mcv['Normal'], risk['Normal']),
        ctrl.Rule(wbc['Low'] & neu['Low'], risk['Severe']),
        ctrl.Rule(wbc['High'] & neu['High'], risk['Moderate']),
        ctrl.Rule(plt['Low'] & wbc['Normal'], risk['Mild']),
        ctrl.Rule(plt['High'] & wbc['Normal'], risk['Normal']),
        ctrl.Rule(neu['Low'] & wbc['Normal'], risk['Mild']),
        ctrl.Rule(neu['High'], risk['Mild']),
        ctrl.Rule(mcv['Low'], risk['Mild']),
        ctrl.Rule(mcv['High'], risk['Mild']),
        ctrl.Rule(rdw['High'], risk['Mild']),
        ctrl.Rule(egfr['Moderate'], risk['Mild']),
        ctrl.Rule(egfr['Severe'], risk['Severe']),
        ctrl.Rule(creat['Moderate'], risk['Mild']),
        ctrl.Rule(creat['Severe'], risk['Severe']),
        
        # 17-19. Infection Variations
        ctrl.Rule(wbc['High'] & neu['High'], risk['Moderate']),
        ctrl.Rule(wbc['High'] & neu['Low'], risk['Moderate']),
        ctrl.Rule(wbc['Low'] & neu['Low'], risk['Severe']),
        
        # 20-23. Anemia Subtypes
        ctrl.Rule(hb['Low'] & mcv['Low'], risk['Moderate']),
        ctrl.Rule(hb['Low'] & mcv['High'], risk['Moderate']),
        ctrl.Rule(hb['Low'] & rdw['High'], risk['Moderate']),
        ctrl.Rule(hb['Normal'] & mcv['Low'] & rdw['High'], risk['Mild']),
        
        # 24-31. Renal Decline & Complications
        ctrl.Rule(egfr['Moderate'] & creat['Moderate'], risk['Moderate']),
        ctrl.Rule(egfr['Severe'] & creat['Moderate'], risk['Severe']),
        ctrl.Rule(egfr['Moderate'] & creat['Severe'], risk['Severe']),
        ctrl.Rule(egfr['Moderate'] & hb['Low'], risk['Moderate']),
        ctrl.Rule(creat['Moderate'] & hb['Low'], risk['Moderate']),
        ctrl.Rule(egfr['Severe'] & hb['Low'], risk['Severe']),
        ctrl.Rule(egfr['Severe'] & creat['Normal'], risk['Severe']),
        ctrl.Rule(egfr['Normal'] & creat['Severe'], risk['Severe']),
        
        # 32-39. Hematology Combinations
        ctrl.Rule(hb['Low'] & plt['Low'], risk['Severe']),
        ctrl.Rule(wbc['High'] & plt['Low'], risk['Severe']),
        ctrl.Rule(wbc['Low'] & plt['Low'], risk['Severe']),
        ctrl.Rule(plt['High'] & wbc['High'], risk['Moderate']),
        ctrl.Rule(hb['Low'] & wbc['High'], risk['Moderate']),
        ctrl.Rule(hb['High'] & plt['High'], risk['Moderate']),
        ctrl.Rule(hb['Low'] & plt['High'], risk['Moderate']),
        ctrl.Rule(plt['High'] & rdw['High'], risk['Moderate']),
        
        # 40-50. Combinatorial Edge Cases
        ctrl.Rule(hb['Low'] & wbc['High'] & egfr['Moderate'], risk['Severe']),
        ctrl.Rule(wbc['Low'] & egfr['Moderate'], risk['Moderate']),
        ctrl.Rule(plt['Low'] & creat['Moderate'], risk['Severe']),
        ctrl.Rule(wbc['High'] & neu['High'] & egfr['Normal'], risk['Moderate']),
        ctrl.Rule(wbc['High'] & neu['High'] & creat['Normal'], risk['Moderate']),
        ctrl.Rule(hb['Normal'] & wbc['High'] & plt['Low'] & egfr['Normal'], risk['Moderate']),
        ctrl.Rule(hb['Low'] & wbc['Low'] & plt['Low'], risk['Severe']),
        ctrl.Rule(hb['High'] & wbc['High'] & plt['High'], risk['Moderate']),
        ctrl.Rule(egfr['Moderate'] & rdw['High'], risk['Moderate']),
        ctrl.Rule(creat['Moderate'] & rdw['High'], risk['Moderate']),
        ctrl.Rule(egfr['Severe'] & hb['Normal'] & wbc['Normal'] & plt['Normal'], risk['Severe'])
    ]

    risk_ctrl = ctrl.ControlSystem(rules)
    risk_sim = ctrl.ControlSystemSimulation(risk_ctrl)

# Build initially
build_system()

def adjust_fis_thresholds(variable_name: str, category: str, new_range: list) -> str:
    """
    Dynamically update a membership function for a given variable.
    Example: adjust_fis_thresholds('plt', 'Low', [0, 0, 180, 200])
    """
    if variable_name not in variables:
        return f"Error: Variable {variable_name} not found."
    
    var = variables[variable_name]
    
    # Check if the shape is trapezoidal or triangular
    if len(new_range) == 4:
        var[category] = fuzz.trapmf(var.universe, new_range)
    elif len(new_range) == 3:
        var[category] = fuzz.trimf(var.universe, new_range)
    else:
        return f"Error: new_range must have 3 or 4 points, got {len(new_range)}."
        
    # Rebuild system so changes take effect
    build_system()
    return f"Successfully updated '{variable_name}' category '{category}' to {new_range}."

def assess_patient(lab_dict: dict) -> float:
    if risk_sim is None:
        build_system()
        
    for key, val in lab_dict.items():
        if key in risk_sim.input.keys():
            try:
                risk_sim.input[key] = float(val)
            except (ValueError, TypeError):
                pass
    try:
        risk_sim.compute()
        if 'risk' in risk_sim.output:
            return risk_sim.output['risk']
        else:
            print("No rules fired, risk not calculated.")
            return -1.0
    except Exception as e:
        print(f"Error computing risk for patient: {e}")
        return -1.0

# 5. Validation Execution
if __name__ == '__main__':
    print("=== Fuzzy Inference System Engine Initialized ===")
    
    # Test Cases
    patient_critical = {
        'hb': 9.5, 'wbc': 15.0, 'plt': 90, 'neu': 85.0, 
        'mcv': 70, 'rdw': 18.0, 'egfr': 30, 'creat': 220
    }
    
    patient_healthy = {
        'hb': 15.2, 'wbc': 7.6, 'plt': 275, 'neu': 57.5, 
        'mcv': 88, 'rdw': 13.4, 'egfr': 105, 'creat': 88
    }
    
    patient_borderline = {
        'hb': 12.5, 'wbc': 11.5, 'plt': 145, 'neu': 76.0, 
        'mcv': 97, 'rdw': 15.0, 'egfr': 85, 'creat': 100
    }
    
    score_critical = assess_patient(patient_critical)
    score_healthy = assess_patient(patient_healthy)
    score_borderline = assess_patient(patient_borderline)
    
    print("\n--- Clinical Risk Assessments ---")
    print(f"Critically Ill Patient Risk Score: {score_critical:.2f} / 100.00")
    print(f"Perfectly Healthy Patient Risk Score: {score_healthy:.2f} / 100.00")
    print(f"Borderline Edge-Case Patient Risk Score: {score_borderline:.2f} / 100.00")
