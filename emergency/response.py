def get_emergency_protocol(disaster_type):
    """
    Returns structured crisis response protocols, emergency instructions, 
    action checklists, and hotlines tailored to the detected hazard.
    """
    protocols = {
        "Wildfire": {
            "title": "🔥 Wildfire Crisis Response Protocol",
            "badge_color": "#EF4444",
            "summary": "Immediate containment and evacuation measures for active wildfire fronts.",
            "instructions": [
                "Evacuate downwind areas immediately upon receiving official alert warnings.",
                "Close all windows, doors, and air vents to prevent ember intrusion into structures.",
                "Wear N95 or higher respiratory protection to filter toxic PM2.5 wildfire smoke particulates.",
                "Turn off main gas lines and clear flammable vegetation within a 30-foot perimeter of buildings."
            ],
            "checklist": [
                "Emergency go-bag with medication and key documents packed",
                "Wildfire evacuation route identified and checked for closures",
                "Animals and livestock secured or transported to shelter",
                "Communication check completed with local fire department"
            ],
            "hotlines": [
                {"service": "National Emergency Fire Response", "number": "911 / 112"},
                {"service": "Wildfire Evacuation Assistance Line", "number": "1-800-555-FIRE"},
                {"service": "Air Quality Emergency Desk", "number": "1-800-555-SMOKE"}
            ]
        },

        "Flood": {
            "title": "🌊 Flood & Inundation Emergency Protocol",
            "badge_color": "#2563EB",
            "summary": "Safety instructions for rising water levels, flash floods, and storm surges.",
            "instructions": [
                "Move to higher ground or upper building stories immediately. Avoid basements.",
                "Never walk or drive through flowing floodwaters (6 inches of water can knock you down).",
                "Disconnect electrical appliances if standing in dry areas, or shut off main breaker if safe.",
                "Boil all drinking water or use sealed bottled water until supply safety is confirmed."
            ],
            "checklist": [
                "Portable waterproof flashlight and radio powered on",
                "Bottled drinking water (3 gallons per person reserve)",
                "First-aid kit and emergency thermal blankets secured",
                "High-ground evacuation point confirmed with local disaster management"
            ],
            "hotlines": [
                {"service": "National Flood Disaster Helpline", "number": "911 / 112"},
                {"service": "Water Crisis & Rescue Command", "number": "1-800-555-WTR1"},
                {"service": "Coast Guard & Water Rescue", "number": "1-800-555-RESC"}
            ]
        },

        "Deforestation": {
            "title": "🪵 Environmental Deforestation Protocol",
            "badge_color": "#D97706",
            "summary": "Intervention directives for illegal logging and canopy loss mitigation.",
            "instructions": [
                "Report coordinates of unpermitted heavy machinery to forestry authorities immediately.",
                "Establish temporary soil retention barriers along exposed slopes to prevent mudslides.",
                "Halt non-essential vehicle traffic through newly cleared forest sectors to prevent compaction.",
                "Initiate fast-growing native sapling replanting along riparian buffer zones."
            ],
            "checklist": [
                "Forestry enforcement patrol notified with GPS coordinates",
                "Slope erosion risk assessment completed",
                "Protected species survey triggered",
                "Buffer zone boundaries marked for legal protection"
            ],
            "hotlines": [
                {"service": "Forestry Enforcement Emergency Desk", "number": "1-800-555-WOOD"},
                {"service": "Environmental Protection Hotline", "number": "1-800-555-ENVI"}
            ]
        },

        "Urban Expansion": {
            "title": "🏙️ Sustainable Urban Growth Guidance",
            "badge_color": "#8B5CF6",
            "summary": "Urban heat island mitigation and sustainable infrastructure development rules.",
            "instructions": [
                "Mandate high-albedo reflective roofing materials on new industrial complexes.",
                "Incorporate permeable pavement and bioswales to manage increased urban stormwater runoff.",
                "Protect contiguous urban tree canopies to counteract microclimate temperature spikes.",
                "Enforce strict zoning buffer distances between industrial sectors and natural wetlands."
            ],
            "checklist": [
                "Stormwater runoff capacity calculation completed",
                "Urban green canopy preservation metric verified",
                "Zoning compliance review initiated"
            ],
            "hotlines": [
                {"service": "Urban Planning Advisory Desk", "number": "1-800-555-PLAN"},
                {"service": "Environmental Zoning Authority", "number": "1-800-555-ZONE"}
            ]
        },

        "Normal": {
            "title": "✅ Standard Monitoring Protocol",
            "badge_color": "#10B981",
            "summary": "Routine operational procedures for clear satellite observation sectors.",
            "instructions": [
                "Maintain automated 24-hour orbital pass monitoring schedules.",
                "Log baseline land surface temperature and spectral indices for temporal comparison.",
                "Ensure emergency alert webhooks are active and calibrated."
            ],
            "checklist": [
                "Baseline spectral indices recorded",
                "Orbital telemetry link verified",
                "System health check passed"
            ],
            "hotlines": [
                {"service": "OrbitEye Operations Desk", "number": "1-800-555-ORBIT"}
            ]
        }
    }

    return protocols.get(disaster_type, protocols["Normal"])
