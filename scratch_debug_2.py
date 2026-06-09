import fuzzy_engine

lab_data = {
    'hb': 15.0,
    'wbc': 7.6,
    'plt': 275.0,
    'neu': 57.5,
    'mcv': 88.0,
    'rdw': 13.4,
    'egfr': 110.0,
    'creat': 85.0
}

try:
    print("Run 1:")
    score = fuzzy_engine.assess_patient(lab_data)
    print("Score 1:", score)
    
    print("Run 2:")
    score = fuzzy_engine.assess_patient(lab_data)
    print("Score 2:", score)
    
    print("Run 3 (with different data):")
    lab_data['hb'] = 9.0
    score = fuzzy_engine.assess_patient(lab_data)
    print("Score 3:", score)

except Exception as e:
    import traceback
    traceback.print_exc()
