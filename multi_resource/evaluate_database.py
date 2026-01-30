def validate_database(db):
    required_fields = {
        "name": str,
        "connection_count": int,
        "CPU_usage_percentage": (int, float),
        "has_read_write_activity": bool,
        "backup_enabled": bool,
        "tag": str
    }

    for field, field_type in required_fields.items():
        if field not in db:
            raise ValueError(f"Database missing field: {field}")
        if not isinstance(db[field], field_type):
            raise ValueError(f"Invalid type for database field: {field}")


def evaluate_database(db):
    validate_database(db)

    risk_score = 0
    reasons = []

    if db["connection_count"] < 10:
        risk_score += 30
        reasons.append({"code": "LESS_CONNECTIONS", "weight": 30})

    if db["CPU_usage_percentage"] < 5:
        risk_score += 30
        reasons.append({"code": "LOW_CPU", "weight": 30})

    if not db["has_read_write_activity"]:
        risk_score += 20
        reasons.append({"code": "NO_ACTIVITY", "weight": 20})

    if (
        db["CPU_usage_percentage"] < 5
        and db["backup_enabled"]
        and not db["has_read_write_activity"]
    ):
        risk_score += 20
        reasons.append({"code": "BACKUP_ACTIVE_BUT_UNUSED_DATA", "weight": 20})

    if db["tag"] == "dev":
        risk_score += 10
        reasons.append({"code": "DEV_TAG", "weight": 10})

    confidence = min(risk_score, 100)
    action = "clean" if confidence >= 75 else "keep_running"

    return {
        "name": db["name"],
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

# ------ Data for the system ----------


database = [
     {"name" : "database set 111", "connection_count" : 5, "CPU_usage_percentage" : 3, "has_read_write_activity" : False, "backup_enabled" : True, "tag" : "dev"}, 
     {"name" : "database set 222", "connection_count" : 50, "CPU_usage_percentage" : 99, "has_read_write_activity" : False, "backup_enabled" : True, "tag" : "dev"}, 
     {"name" : "database set 5423", "connection_count" : 0, "CPU_usage_percentage" : 0, "has_read_write_activity" : False, "backup_enabled" : True, "tag" : "test"}, 
     {"name" : "database set as34", "connection_count" : 112, "CPU_usage_percentage" : -12, "has_read_write_activity" : True, "backup_enabled" : False, "tag" : "dev"}, 
     {"name" : "database set 700", "connection_count" : 10, "CPU_usage_percentage" : 20, "has_read_write_activity" : True, "backup_enabled" : False, "tag" : "dev"}, 

]