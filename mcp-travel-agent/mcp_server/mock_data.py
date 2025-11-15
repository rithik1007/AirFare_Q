# mcp_server/mock_data.py
from datetime import datetime

FLIGHTS = [
    {
        "flight_id": "F-IND-101",
        "origin": "BOM",
        "destination": "DXB",
        "depart_time": "2025-12-05T02:30:00",
        "arrive_time": "2025-12-05T05:30:00",
        "duration_minutes": 240,
        "airline": "AirExample",
        "price_inr": 22000,
        "stops": 0
    },
    {
        "flight_id": "F-IND-102",
        "origin": "BOM",
        "destination": "DXB",
        "depart_time": "2025-12-05T09:00:00",
        "arrive_time": "2025-12-05T12:45:00",
        "duration_minutes": 225,
        "airline": "FlyMock",
        "price_inr": 25500,
        "stops": 1
    },
    {
        "flight_id": "F-IND-103",
        "origin": "BOM",
        "destination": "DXB",
        "depart_time": "2025-12-06T01:00:00",
        "arrive_time": "2025-12-06T04:05:00",
        "duration_minutes": 185,
        "airline": "BudgetAir",
        "price_inr": 19800,
        "stops": 0
    },
    # Add additional flights for testing/comparison
    {
        "flight_id": "F-IND-104",
        "origin": "BOM",
        "destination": "DXB",
        "depart_time": "2025-12-05T21:00:00",
        "arrive_time": "2025-12-06T00:05:00",
        "duration_minutes": 185,
        "airline": "LateNightAir",
        "price_inr": 20500,
        "stops": 0
    }
]

HOTELS = [
    {
        "hotel_id": "H-001",
        "city": "Dubai",
        "name": "Mock Inn Downtown",
        "nightly_price_inr": 5000,
        "rating": 4.1,
        "distance_km": 1.2
    },
    {
        "hotel_id": "H-002",
        "city": "Dubai",
        "name": "Budget Stay",
        "nightly_price_inr": 3200,
        "rating": 3.8,
        "distance_km": 3.5
    },
    {
        "hotel_id": "H-003",
        "city": "Dubai",
        "name": "Comfort Suites",
        "nightly_price_inr": 6500,
        "rating": 4.5,
        "distance_km": 0.8
    }
]
