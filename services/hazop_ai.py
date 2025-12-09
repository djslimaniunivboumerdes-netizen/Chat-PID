
def generate_hazop_suggestions(tag):
    # MOCK AI RESPONSE: In production, this calls Gemini/OpenAI/Local LLM
    if "P-" in tag:
        return [
            "**Deviation:** No Flow (Pump trip). **Consequence:** Vessel overpressure (E-201). **Safeguard:** High Pressure Switch (PSH).",
            "**Deviation:** Low Flow (Cavitation). **Consequence:** Pump damage. **Safeguard:** Low Level Trip on Suction Vessel (T-100 LSL)."
        ]
    elif "E-" in tag:
        return [
            "**Deviation:** High Temperature. **Consequence:** Product degradation. **Safeguard:** Temperature Indicator/Alarm (TIA).",
        ]
    else:
        return ["AI analysis complete. No immediate HAZOP concerns identified for this component."]
