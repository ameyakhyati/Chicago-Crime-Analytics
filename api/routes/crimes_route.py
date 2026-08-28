from flask import Blueprint, jsonify, request
import sqlite3


from api.services.crimes_service import (
    add_crime,
    get_crimes,
    get_crime,
    edit_crime,
    remove_crime,
    get_options
)


crime_bp = Blueprint("crime", __name__)
DB_PATH = "database/CHICAGO_CRIMES.DB"


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


@crime_bp.route("/api/crimes", methods=["GET"])
def get_all_crimes():
    connection = get_db_connection()

    try:
        crimes = get_crimes(connection)
        return jsonify({"success": True, "count": len(crimes), "data": crimes}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        connection.close()


@crime_bp.route("/api/crimes/<case_number>", methods=["GET"])
def get_single_crime(case_number):
    connection = get_db_connection()

    try:
        crime = get_crime(connection, case_number)

        if crime is None:
            return jsonify({"success": False, "message": "Crime record not found."}), 404


        return jsonify({"success": True, "data": crime}), 200


    except Exception as e:
        return jsonify({"success": False,"message": str(e)}), 500

    finally:
        connection.close()


@crime_bp.route("/api/crimes", methods=["POST"])
def add_new_crime():
    """Create a new crime record from JSON payload."""
    connection = get_db_connection()

    try:
        crime_data = request.get_json()

        if not crime_data:
            return jsonify({"success": False, "message": "No crime data provided."}), 400

        result = add_crime(connection,crime_data)

        if not result["success"]:
            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:

        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        connection.close()


@crime_bp.route("/api/crimes/<case_number>", methods=["PUT"])
def update_crime(case_number):
    connection = get_db_connection()

    try:
        crime_data = request.get_json()

        if not crime_data:
            return jsonify({ "success": False, "message": "No update data provided."}), 400

        result = edit_crime(connection, case_number, crime_data)

        if not result["success"]:
            return jsonify(result), 404

        return jsonify(result), 200

    except Exception as e:

        return jsonify({ "success": False,"message": str(e)}), 500

    finally:
        connection.close()


@crime_bp.route("/api/crimes/<case_number>", methods=["DELETE"])
def delete_crime(case_number):
    connection = get_db_connection()

    try:
        result = remove_crime(connection,case_number )

        if not result["success"]:
            return jsonify(result), 404

        return jsonify(result), 200

    except Exception as e:

        return jsonify({"success": False,"message": str(e)}), 500

    finally:
        connection.close()

@crime_bp.route("/api/crime-options", methods=["GET"])
def get_crime_options():
    connection = get_db_connection()

    try:
        options = get_options(connection)

        return jsonify({ "success": True, "data": options}), 200

    except Exception as e:

        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        connection.close()
