# mcp_server/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date
from uuid import uuid4
from .mock_data import FLIGHTS, HOTELS

app = FastAPI(title="MCP Travel Tools (Mock)")

# ---------- Schemas ----------
class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    date: date
    passengers: int = 1
    cabin: Optional[str] = "economy"

class FlightOption(BaseModel):
    flight_id: str
    airline: str
    origin: str
    destination: str
    depart_time: str
    arrive_time: str
    duration_minutes: int
    price_inr: int
    stops: int

class HotelSearchRequest(BaseModel):
    city: str
    checkin: date
    checkout: date
    guests: int = 1
    max_price_inr: Optional[int] = None

class HotelOption(BaseModel):
    hotel_id: str
    city: str
    name: str
    nightly_price_inr: int
    rating: float
    distance_km: float

class BookFlightRequest(BaseModel):
    flight_id: str
    passenger_name: str
    email: str

class BookHotelRequest(BaseModel):
    hotel_id: str
    guest_name: str
    email: str

class BookResponse(BaseModel):
    booking_id: str
    status: str
    details: Dict[str, Any]

# ---------- In-memory store for bookings ----------
BOOKINGS: Dict[str, Dict] = {}

# ---------- Endpoints ----------
@app.post("/search_flights", response_model=List[FlightOption])
async def search_flights(req: FlightSearchRequest):
    results = [
        f for f in FLIGHTS
        if f["destination"].lower() == req.destination.lower()
        and f["origin"].lower() == req.origin.lower()
    ]
    if not results:
        raise HTTPException(status_code=404, detail="No flights found")
    results_sorted = sorted(results, key=lambda x: x["price_inr"])[:10]
    return [FlightOption(**r) for r in results_sorted]

@app.post("/search_hotels", response_model=List[HotelOption])
async def search_hotels(req: HotelSearchRequest):
    results = [
        h for h in HOTELS
        if h["city"].lower() == req.city.lower()
    ]
    if req.max_price_inr:
        results = [h for h in results if h["nightly_price_inr"] <= req.max_price_inr]
    if not results:
        raise HTTPException(status_code=404, detail="No hotels found")
    results_sorted = sorted(results, key=lambda x: (x["nightly_price_inr"], -x["rating"]))[:10]
    return [HotelOption(**h) for h in results_sorted]

@app.post("/compare_fares")
async def compare_fares(flight_ids: List[str]):
    matches = [f for f in FLIGHTS if f["flight_id"] in flight_ids]
    if not matches:
        raise HTTPException(status_code=404, detail="No matching flights")
    # build comparison summary
    summary = []
    for f in matches:
        summary.append({
            "flight_id": f["flight_id"],
            "airline": f["airline"],
            "price_inr": f["price_inr"],
            "duration_minutes": f["duration_minutes"],
            "stops": f["stops"],
            "value_score": max(0, 100 - f["price_inr"] // 300) - f["stops"] * 5
        })
    best = min(matches, key=lambda x: x["price_inr"])
    return {"count": len(matches), "flights": summary, "cheapest_flight_id": best["flight_id"]}

@app.post("/book_flight", response_model=BookResponse)
async def book_flight(req: BookFlightRequest):
    flight = next((f for f in FLIGHTS if f["flight_id"] == req.flight_id), None)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    booking_id = str(uuid4())
    booking = {
        "type": "flight",
        "booking_id": booking_id,
        "flight": flight,
        "passenger": {"name": req.passenger_name, "email": req.email},
        "status": "CONFIRMED"
    }
    BOOKINGS[booking_id] = booking
    return BookResponse(booking_id=booking_id, status="CONFIRMED", details=booking)

@app.post("/book_hotel", response_model=BookResponse)
async def book_hotel(req: BookHotelRequest):
    hotel = next((h for h in HOTELS if h["hotel_id"] == req.hotel_id), None)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    booking_id = str(uuid4())
    booking = {
        "type": "hotel",
        "booking_id": booking_id,
        "hotel": hotel,
        "guest": {"name": req.guest_name, "email": req.email},
        "status": "CONFIRMED"
    }
    BOOKINGS[booking_id] = booking
    return BookResponse(booking_id=booking_id, status="CONFIRMED", details=booking)

@app.get("/booking/{booking_id}")
async def get_booking(booking_id: str):
    booking = BOOKINGS.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.get("/health")
async def health():
    return {"ok": True, "bookings": len(BOOKINGS)}
