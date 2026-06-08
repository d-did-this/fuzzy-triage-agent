from fuzzy_engine import assess_patient

def check_symptoms(egfr_value: float) -> str:
    """
    Returns common symptoms based on eGFR thresholds.
    """
    if egfr_value < 30:
        return "Severe symptoms: nausea, muscle cramps, loss of appetite, swelling in feet/ankles, and unexplained fatigue."
    elif egfr_value < 60:
        return "Mild/Moderate symptoms: fatigue, fluid retention (swelling), and changes in urination frequency."
    else:
        return "No major kidney-related symptoms are typically present at this level."

def check_drug_safety(medication_name: str, egfr_value: float) -> str:
    """
    Returns warnings if nephrotoxic drugs (like NSAIDs/Ibuprofen) are mentioned when eGFR < 60.
    """
    nephrotoxic_drugs = ["nsaid", "ibuprofen", "advil", "motrin", "naproxen", "aleve", "diclofenac"]
    med_lower = medication_name.lower()
    
    if egfr_value < 60:
        for drug in nephrotoxic_drugs:
            if drug in med_lower:
                return f"WARNING: {medication_name} is nephrotoxic. With an eGFR of {egfr_value} (<60), this can worsen kidney function. Consult a doctor before use."
        return f"{medication_name} is not on our immediate nephrotoxic watchlist, but verify with a pharmacist given the reduced eGFR ({egfr_value})."
    else:
        return f"eGFR is {egfr_value} (>=60). Standard dosing guidelines for {medication_name} apply, but always read the label."
