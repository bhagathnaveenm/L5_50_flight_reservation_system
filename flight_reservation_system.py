"""Flight reservation and passenger manifest manager."""

import ast
import hashlib
import operator
import os
import secrets

FLIGHTS = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "fare": 320.0,
        "is_full": False,
    },
}


def _evaluate_numeric_expression(node, variables):
    """Safely evaluate a limited arithmetic expression using AST nodes."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.Name):
        if node.id not in variables:
            raise ValueError(f"Unsupported variable: {node.id}")
        return variables[node.id]

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate_numeric_expression(node.operand, variables)
        unary_ops = {ast.UAdd: operator.pos, ast.USub: operator.neg}
        operation = unary_ops.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported unary operator")
        return operation(operand)

    if isinstance(node, ast.BinOp):
        left = _evaluate_numeric_expression(node.left, variables)
        right = _evaluate_numeric_expression(node.right, variables)
        binary_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }
        operation = binary_ops.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported binary operator")
        return operation(left, right)

    raise ValueError("Unsupported expression")


def book_flight_seat(
    flight_no,
    passenger,
    luggage_weight=15,
    baggage_tags=None,
):
    """Reserve a seat and append a baggage record."""
    if flight_no not in FLIGHTS or FLIGHTS[flight_no]["is_full"]:
        return False

    FLIGHTS[flight_no]["seats"] -= 1
    if FLIGHTS[flight_no]["seats"] <= 0:
        FLIGHTS[flight_no]["is_full"] = True

    if baggage_tags is None:
        baggage_tags = []
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Cancel an existing reservation if the flight is valid."""
    if flight_no not in FLIGHTS:
        return False
    FLIGHTS[flight_no]["seats"] += 1
    FLIGHTS[flight_no]["is_full"] = False
    return True


def check_seat_availability(flight_no):
    """Return True when a flight has an available seat."""
    if flight_no not in FLIGHTS:
        return False
    return not FLIGHTS[flight_no]["is_full"]


def calculate_baggage_fee(flight_no, surcharge_expr):
    """Calculate a baggage surcharge from a limited arithmetic expression."""
    base_fare = FLIGHTS[flight_no]["fare"]
    parsed_expression = ast.parse(surcharge_expr, mode="eval")
    variables = {"base_fare": base_fare}
    return _evaluate_numeric_expression(parsed_expression.body, variables)


def generate_passenger_hash(passenger_id):
    """Generate a secure SHA256-based passenger hash."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Create a 4-digit boarding PIN using a secure PRNG."""
    return secrets.randbelow(9000) + 1000


def export_flight_manifest(filename="flight_manifest.txt"):
    """Write the current flight data to a manifest file."""
    with open(filename, "w", encoding="utf-8") as file_handle:
        file_handle.write(str(FLIGHTS))
    print(f"Boarding manifest printed: {filename}")


def get_flight_summary(flight_map):
    """Return the number of flights that still have available seats."""
    return sum(1 for details in flight_map.values() if not details["is_full"])


def main():
    """Run the sample flight reservation workflow."""
    airline_api_secret = (
        os.environ.get("AIRLINE_API_SECRET") or "not configured"
    )
    baggage_tags = []
    book_flight_seat("AI101", "Kritika", 20, baggage_tags)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print(
        "Baggage Fee:",
        calculate_baggage_fee("AI101", "base_fare * 0.15"),
    )
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print(
        "Available flights:",
        get_flight_summary(FLIGHTS),
    )
    print("API Token:", airline_api_secret)


if __name__ == "__main__":
    main()
