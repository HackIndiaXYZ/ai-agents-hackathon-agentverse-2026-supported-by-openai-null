import json
import os
from langchain_core.tools import tool

# Helper function to safely read local database.json
DB_PATH = os.path.join(os.path.dirname(__file__), "database.json")

def load_db():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("database.json not found in root directory!")
    with open(DB_PATH, "r") as f:
        return json.load(f)


@tool
def verify_drug_batch(batch_number: str) -> str:
    """Checks the authenticity, recall status, and expiration date of a medication batch code."""
    db = load_db()
    drugs = db.get("drugs", {})
    
    batch_key = batch_number.strip().upper()
    if batch_key in drugs:
        info = drugs[batch_key]
        if info["recalled"]:
            return f"🚨 CRITICAL ALERT: Batch '{batch_key}' ({info['name']}) is RECALLED/COUNTERFEIT! Notes: {info['notes']}"
        return f"✅ VERIFIED: Batch '{batch_key}' ({info['name']} {info['dosage']}) is Authentic. Status: {info['status']}. Expires: {info['expiry_date']}. Notes: {info['notes']}"
    
    return f"⚠️ UNKNOWN BATCH: '{batch_number}' is not in the official registry. Potential counterfeit or unverified stock."


@tool
def check_clinic_inventory(medicine_name: str) -> str:
    """Checks current stock levels, cabinet locations, and reorder warnings for a medication at the rural clinic."""
    db = load_db()
    inventory = db.get("inventory", {})
    
    # Simple case-insensitive lookup
    for item, data in inventory.items():
        if item.lower() == medicine_name.strip().lower():
            stock = data["stock_count"]
            location = data["location"]
            reorder = data["reorder_level"]
            
            status = "In Stock" if stock > reorder else "LOW STOCK WARNING"
            return f"📦 INVENTORY REPORT for {item}: Status = {status} | Stock = {stock} units | Location = {location} | Reorder Level = {reorder}"
            
    return f"❌ NOT FOUND: '{medicine_name}' is not currently listed in the clinic's inventory registry."


@tool
def evaluate_patient_triage(spo2: int, heart_rate: int, temperature_f: float, symptoms: str) -> str:
    """Evaluates patient vital signs and symptoms to assign an emergency triage urgency level (RED/YELLOW/GREEN)."""
    db = load_db()
    thresholds = db.get("vital_thresholds", {})
    
    urgency_reasons = []
    
    # Check vital parameters
    if spo2 < thresholds.get("spo2_danger_below", 92):
        urgency_reasons.append(f"Low Oxygen Saturation (SpO2: {spo2}%)")
        
    if heart_rate > thresholds.get("heart_rate_high_above", 110):
        urgency_reasons.append(f"Tachycardia / High Heart Rate ({heart_rate} bpm)")
        
    if temperature_f > thresholds.get("temp_f_fever_above", 100.4):
        urgency_reasons.append(f"Fever ({temperature_f}°F)")

    # Assign Triage Risk Level
    if spo2 < 90 or "chest pain" in symptoms.lower() or "unconscious" in symptoms.lower():
        color = "🔴 RED (IMMEDIATE EMERGENCY)"
        action = "Transfer to intensive care / Immediate medical intervention required."
    elif len(urgency_reasons) >= 2 or "severe" in symptoms.lower():
        color = "🟡 YELLOW (URGENT)"
        action = "Prioritize medical observation within 30 minutes."
    else:
        color = "🟢 GREEN (STABLE / STANDARD)"
        action = "Standard clinical checkup and routine treatment."

    reasons_str = ", ".join(urgency_reasons) if urgency_reasons else "Vitals within normal baseline."
    return f"LOCAL TRIAGE ASSESSMENT: Priority = {color} | Concerns = [{reasons_str}] | Action = {action}"