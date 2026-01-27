def validate_vm(vm):
    required_fields = {
        "name": str,
        "CPU_Usage": (int, float),
        "Network_traffic": int,
        "days_idle": int,
        "tag": str
    }

    for field, field_type in required_fields.items():
        if field not in vm:
            raise ValueError(f"VM missing field: {field}")
        if not isinstance(vm[field], field_type):
            raise ValueError(f"Invalid type for VM field: {field}")

    if vm["CPU_Usage"] < 0:
        raise ValueError("CPU_Usage cannot be negative")


def evaluate_vm(vm):
    validate_vm(vm)

    risk_score = 0
    reasons = []

    if vm["CPU_Usage"] < 5:
        risk_score += 30
        reasons.append({"code": "LOW_CPU", "weight": 30})

    if vm["Network_traffic"] == 0:
        risk_score += 30
        reasons.append({"code": "NO_NETWORK", "weight": 30})

    if vm["days_idle"] > 7:
        risk_score += 20
        reasons.append({"code": "IDLE_7_DAYS", "weight": 20})

    if vm["tag"] == "dev":
        risk_score += 10
        reasons.append({"code": "DEV_TAG", "weight": 10})

    confidence = min(risk_score, 100)
    action = "stop" if confidence >= 75 else "keep_running"

    return {
        "name": vm["name"],
        "confidence": confidence,
        "action": action,
        "reasons": reasons
    }




# ------ Presentation Layer ----------

reason_text = {
        "LOW_CPU" : "CPU usage below 5% ",
        "NO_NETWORK" : "No inbound traffic detected",
        "IDLE_7_DAYS": "System idle for more than 7 days",
        "DEV_TAG": "Environment tagged as dev",
        "LESS_ACCESSED" : "Data not accessed for more than 30 days",
        "HIGH_STORAGE_BUT_LESS_ACCESSED" : "High storage but data is not accessed for more than 30 days",
        "BACKUP_ACTIVE" : "Old data backup is enabled",
        "LESS_CONNECTIONS" : "Less than 10 connections to the database",
        "NO_ACTIVITY" : "No read/write operations active on the database",
        "BACKUP_ACTIVE_BUT_UNUSED_DATA" : "Backup enabled but No read/write operations active and data has not been accessed for more than 30 days"

    }


# ------- Data for the system -------------
vm = [ 
    {"name" : "vm test AA", "CPU_Usage" : 4, "Network_traffic" : 0, "days_idle" : 5, "tag" : "dev"},
    {"name" : "vm test BB", "CPU_Usage" : 5, "Network_traffic" : 1, "days_idle" : 7, "tag" : "test"},
    {"name" : "vm test 123", "CPU_Usage" : 0, "Network_traffic" : 0, "days_idle" : 14, "tag" : "dev"},
    {"name" : "vm test 456", "CPU_Usage" : -1, "Network_traffic" : 1, "days_idle" : 3, "tag" : "dev"},
    {"name" : "vm test CC", "CPU_Usage" : 10, "Network_traffic" : 0, "days_idle" : 1, "tag" : "dev"},
]




