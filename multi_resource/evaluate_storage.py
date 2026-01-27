def validate_storage(storage):
    required_fields = {
        "name": str,
        "last_accessed_days": int,
        "storage_size_tb": (int, float),
        "old_backup_data": bool,
        "tag": str
    }

    for field, field_type in required_fields.items():
        if field not in storage:
            raise ValueError(f"Storage missing field: {field}")
        if not isinstance(storage[field], field_type):
            raise ValueError(f"Invalid type for storage field: {field}")

    if storage["last_accessed_days"] < 0:
        raise ValueError("last_accessed_days cannot be negative")


def evaluate_storage(storage):
    validate_storage(storage)

    risk_score = 0
    reasons = []

    if storage["last_accessed_days"] >= 30:
        risk_score += 30
        reasons.append({"code": "LESS_ACCESSED", "weight": 30})

    if storage["last_accessed_days"] >= 30 and storage["storage_size_tb"] >= 50:
        risk_score += 20
        reasons.append({"code": "HIGH_STORAGE_BUT_LESS_ACCESSED", "weight": 20})

    if storage["old_backup_data"]:
        risk_score += 10
        reasons.append({"code": "BACKUP_ACTIVE", "weight": 10})

    if storage["tag"] == "dev":
        risk_score += 10
        reasons.append({"code": "DEV_TAG", "weight": 10})

    confidence = min(risk_score, 100)
    action = "cleanup" if confidence >= 75 else "keep_running"

    return {
        "name": storage["name"],
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


# -------- Data for the system ----------
storage = [
     {"name" : "storage A1", "last_accessed_days" : 180, "storage_size_tb" : 250, "old_backup_data" : True, "tag" : "dev"},
     {"name" : "storage B2", "last_accessed_days" : 365, "storage_size_tb" : 100, "old_backup_data" : False, "tag" : "dev"},
     {"name" : "storage C3", "last_accessed_days" : 0, "storage_size_tb" : 10, "old_backup_data" : True, "tag" : "test"},
     {"name" : "storage D4", "last_accessed_days" : 30, "storage_size_tb" : 50, "old_backup_data" : False, "tag" : "dev"},
     {"name" : "storage E5", "last_accessed_days" : 1, "storage_size_tb" : 200, "old_backup_data" : False, "tag" : "test"},
     {"name" : "storage F6", "last_accessed_days" : 7, "storage_size_tb" : 5, "old_backup_data" : True, "tag" : "dev"},

]
