from datetime import date
from app import rental_days, dates_overlap, find_conflicting_booking, calculate_total

# --- rental_days ---
assert rental_days(date(2026, 1, 10), date(2026, 1, 10)) == 1  # same day
assert rental_days(date(2026, 1, 10), date(2026, 1, 15)) == 6  # inclusive
print("rental_days OK")

# --- dates_overlap ---
# Existing booking Jan 10-15 (Canon DSLR)
existing_from, existing_to = date(2026, 1, 10), date(2026, 1, 15)

# Clearly overlapping (inside)
assert dates_overlap(date(2026, 1, 12), date(2026, 1, 13), existing_from, existing_to) is True
# Clearly overlapping (spans whole range)
assert dates_overlap(date(2026, 1, 5), date(2026, 1, 20), existing_from, existing_to) is True
# Same-day turnover: new booking starts the day the old one ends -> allowed
assert dates_overlap(date(2026, 1, 15), date(2026, 1, 18), existing_from, existing_to) is False
# Same-day turnover: new booking ends the day the old one starts -> allowed
assert dates_overlap(date(2026, 1, 5), date(2026, 1, 10), existing_from, existing_to) is False
# Fully before, no contact -> allowed
assert dates_overlap(date(2026, 1, 1), date(2026, 1, 9), existing_from, existing_to) is False
# Fully after, no contact -> allowed
assert dates_overlap(date(2026, 1, 16), date(2026, 1, 20), existing_from, existing_to) is False
print("dates_overlap OK")

# --- find_conflicting_booking ---
bookings = [
    {"id": 1, "equipment_id": 1, "from_date": "2026-01-10", "to_date": "2026-01-15", "status": "confirmed"},
    {"id": 2, "equipment_id": 2, "from_date": "2026-01-12", "to_date": "2026-01-14", "status": "cancelled"},
]
# Overlaps equipment 1 -> conflict found
assert find_conflicting_booking(1, date(2026, 1, 12), date(2026, 1, 13), bookings) is not None
# Same-day turnover on equipment 1 -> no conflict
assert find_conflicting_booking(1, date(2026, 1, 15), date(2026, 1, 18), bookings) is None
# Equipment 2 booking is cancelled -> should not block new booking even if dates overlap
assert find_conflicting_booking(2, date(2026, 1, 12), date(2026, 1, 14), bookings) is None
print("find_conflicting_booking OK")

# --- calculate_total ---
# 6 days, no discount (below 7-day threshold)
assert calculate_total(1500.0, 6) == 1500.0 * 6
# exactly 7 days -> discount applies
assert calculate_total(1500.0, 7) == round(1500.0 * 7 * 0.9, 2) or abs(calculate_total(1500.0, 7) - 1500.0 * 7 * 0.9) < 1e-9
# 1 day, no discount
assert calculate_total(480.0, 1) == 480.0
print("calculate_total OK")

print("ALL TESTS PASSED")
