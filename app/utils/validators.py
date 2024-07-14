from datetime import datetime

def validate_params(date_from, date_to, origin, destination):
    # If any one of the params missing, return error
    if not all([date_from, date_to, origin, destination]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Validation checks on date
    try:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')

        if date_from > date_to:
            return jsonify({"error": "date_from must be earlier than date_to"}), 400
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    
    return date_from, date_to

# Port code validation function (assuming each code is of 5 length)
def is_valid_port_code(code): return len(code) == 5

