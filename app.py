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

    Billing is inclusive of both the start and end date, so a booking that
    starts and ends on the same day is 1 day, and Jan 10 -> Jan 15 is 6 days.
    """
    return (to_date - from_date).days + 1


def dates_overlap(start_a, end_a, start_b, end_b):
    """True if date range A conflicts with date range B.

    Same-day turnover is allowed: if A ends exactly when B starts (or B ends
    exactly when A starts), that single shared boundary day is not a
    conflict. Any other overlap is a conflict.

    The standard "ranges overlap" test (start_a <= end_b and
    start_b <= end_a) would treat a shared boundary day as an overlap, so we
    narrow it with strict inequalities: a conflict only exists when the
    ranges share more than a single touching day, i.e. when
    start_a < end_b and start_b < end_a.
    """
    return start_a < end_b and start_b < end_a


def find_conflicting_booking(equipment_id, from_date, to_date, bookings):
    """Return an existing, non-cancelled booking for this equipment that
    conflicts with the given dates, or None.
    """
    for booking in bookings:
        if booking["equipment_id"] != equipment_id:
            continue
        if booking.get("status") == "cancelled":
            continue
        existing_from = parse_date(booking["from_date"])
        existing_to = parse_date(booking["to_date"])
        if dates_overlap(from_date, to_date, existing_from, existing_to):
            return booking
    return None


def calculate_total(daily_rate, days):
    """Total price for a rental of this many days.

    Rentals of 7 days or more (days >= 7) get a 10% discount off the total;
    shorter rentals (1-6 days) are billed at the plain daily rate with no
    discount.
    """
    total = daily_rate * days
    if days >= 7:
        total *= 0.9
    return total


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return send_file("index.html")


@app.route("/api/equipment")
def list_equipment():
    # Equipment under maintenance should never be offered to customers, so
    # it's excluded here as well as from the availability check below.
    return jsonify([item for item in EQUIPMENT if item["status"] != "maintenance"])


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
        if item["status"] == "maintenance":
            continue
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

    if equipment["status"] == "maintenance":
        return jsonify({"error": f"{equipment['name']} is under maintenance and cannot be booked"}), 400

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
