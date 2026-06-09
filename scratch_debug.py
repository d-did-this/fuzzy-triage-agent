import fuzzy_engine

lab_data = {
    'hb': '15',
    'wbc': '7.6',
    'plt': '275',
    'neu': '57.5',
    'mcv': '88',
    'rdw': '13.4',
    'egfr': '110',
    'creat': '85'
}

try:
    fuzzy_engine.build_system()
    for key, val in lab_data.items():
        fuzzy_engine.risk_sim.input[key] = val
    fuzzy_engine.risk_sim.compute()
    print("Score:", fuzzy_engine.risk_sim.output['risk'])
except Exception as e:
    import traceback
    traceback.print_exc()
