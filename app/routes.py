from flask import Blueprint, jsonify, request, current_app, g
from .utils.validators import validate_params

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return jsonify({"message": "Ratetask Default API"})

@routes.route('/rates', methods=['GET'])
def get_rates():
    try:
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        
        current_app.logger.info(f"date_from: {date_from}, date_to: {date_to}, origin: {origin}, destination: {destination}")

        validation_error = validate_params(date_from, date_to, origin, destination)
        if validation_error:
            return validation_error

        conn = g.db
        if not conn:
            return jsonify({"error": "Failed to connect to the database."}), 500

        return jsonify({ "message": "Successfully fetched rates" }), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching rates: {e}")
        return jsonify({"error": "Error fetching rates."}), 500