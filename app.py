"""
Equipment Rental — a small booking app.

Run it with:
    python app.py
Then open http://localhost:5000 in your browser.

Business rules:
  - A booking reserves one piece of equipment for a date range.
  - Rentals are billed *inclusively*: both the start day and the end day count.
    (A pick-up-and-return-same-day rental is therefore 1 day.)
  - You cannot book a piece of equipment for dates that overlap an existing booking,
    EXCEPT for same-day turnover: a new booking may start on the same day an
    existing booking for that equipment ends (or end on the day another booking
    starts). That single shared day is not a conflict; any other overlap still is.
  - Rentals of 7 days or more get a 10% discount off the total.
"""

from datetime import date
from flask import Flask, request, jsonify, send_file
import json
import os

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

EQUIPMENT = [
    {"id": 1, "name": "Canon DSLR Camera", "daily_rate": 1500.0, "status": "available"},
    {"id": 2, "name": "Cordless Drill",     "daily_rate": 480.0,  "status": "available"},
    {"id": 3, "name": "HD Projector",       "daily_rate": 900.0, "status": "maintenance"},
    {"id": 4, "name": "PA Speaker System",  "daily_rate": 1800.0, "status": "available"},
]

BOOKINGS_FILE = "bookings.json"


def load_bookings():
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE) as f:
            return json.load(f)
    return []


def save_bookings(bookings):
    with open(BOOKINGS_FILE, "w") as f:
        json.dump(bookings, f, indent=2)


def get_equipment(equipment_id):
    for item in EQUIPMENT:
        if item["id"] == equipment_id:
            return item
    return None


# ---------------------------------------------------------------------------
# Booking logic
# ---------------------------------------------------------------------------

def parse_date(value):
    return date.fromisoformat(value)


def rental_days(from_date, to_date):
    """Number of days this rental covers (see business rules above).

    TODO (Task 1): implement.
    """
    raise NotImplementedError


def dates_overlap(start_a, end_a, start_b, end_b):
    """True if date range A conflicts with date range B (see the
    same-day-turnover rule above).

    TODO (Task 1): implement.
    """
    raise NotImplementedError


def find_conflicting_booking(equipment_id, from_date, to_date, bookings):
    """Return an existing, non-cancelled booking for this equipment that
    conflicts with the given dates, or None.

    TODO (Task 1): implement.
    """
    raise NotImplementedError


def calculate_total(daily_rate, days):
    """Total price for a rental of this many days (see the long-rental
    discount rule above).

    TODO (Task 2): implement.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return send_file("index.html")


@app.route("/api/equipment")
def list_equipment():
    return jsonify(EQUIPMENT)


@app.route("/api/bookings")
def list_bookings():
    return jsonify(load_bookings())


@app.route("/api/availability")
def availability():
    from_date = parse_date(request.args["from"])
    to_date = parse_date(request.args["to"])
    bookings = load_bookings()

    available = []
    for item in EQUIPMENT:
        conflict = find_conflicting_booking(item["id"], from_date, to_date, bookings)
        if conflict is None:
            available.append(item)
    return jsonify(available)


@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.get_json(force=True)

    equipment = get_equipment(data.get("equipment_id"))
    if equipment is None:
        return jsonify({"error": "Unknown equipment"}), 400

    from_date = parse_date(data["from_date"])
    to_date = parse_date(data["to_date"])
    if to_date < from_date:
        return jsonify({"error": "End date cannot be before start date"}), 400

    bookings = load_bookings()
    conflict = find_conflicting_booking(equipment["id"], from_date, to_date, bookings)
    if conflict is not None:
        return jsonify({
            "error": f"{equipment['name']} is already booked from "
                     f"{conflict['from_date']} to {conflict['to_date']}"
        }), 409

    days = rental_days(from_date, to_date)
    total = calculate_total(equipment["daily_rate"], days)

    booking = {
        "id": (max([b["id"] for b in bookings]) + 1) if bookings else 1,
        "equipment_id": equipment["id"],
        "equipment_name": equipment["name"],
        "customer": data.get("customer", ""),
        "from_date": data["from_date"],
        "to_date": data["to_date"],
        "total": total,
        "status": "confirmed",
    }
    bookings.append(booking)
    save_bookings(bookings)
    return jsonify(booking), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
