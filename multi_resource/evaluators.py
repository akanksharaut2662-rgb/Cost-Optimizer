from evaluate_vm import evaluate_vm
from evaluate_storage import evaluate_storage
from evaluate_database import evaluate_database


def evaluate_resources(data):
    results = {
        "vm": [],
        "storage": [],
        "database": []
    }

    if "vm" in data:
        for vm in data["vm"]:
            results["vm"].append(evaluate_vm(vm))

    if "storage" in data:
        for s in data["storage"]:
            results["storage"].append(evaluate_storage(s))

    if "database" in data:
        for d in data["database"]:
            results["database"].append(evaluate_database(d))

    return results
