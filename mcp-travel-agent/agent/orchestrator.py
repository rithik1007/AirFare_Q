# agent/orchestrator.py
import asyncio
from datetime import datetime, timedelta
from agent.tools_client import ToolsClient

# ---- Simple parsing helper (replace with LLM later) ----
def parse_user_request(user_text: str) -> dict:
    # VERY simple: expects keywords. Replace this with LLM extraction for production.
    # Example user_text: "Plan a 5-day trip to Dubai in December under 60000 including flights + hotel"
    parsed = {
        "origin": "BOM",
        "destination": "Dubai",
        "date": "2025-12-05",
        "nights": 5,
        "budget_inr": 60000,
        "passenger_name": "Test User",
        "email": "you@example.com"
    }
    return parsed

# ---- High-level planning / orchestrator ----
async def plan_and_book(user_text: str, do_book: bool=False):
    parsed = parse_user_request(user_text)
    client = ToolsClient()
    origin = parsed["origin"]
    dest = parsed["destination"]
    date = parsed["date"]
    nights = parsed["nights"]
    budget = parsed["budget_inr"]

    # run flight + hotel searches in parallel
    hotels_checkin = date
    # compute checkout date
    d0 = datetime.fromisoformat(date)
    checkout_date = (d0 + timedelta(days=nights)).date().isoformat()

    flights_task = asyncio.create_task(client.search_flights(origin, dest, date))
    hotels_task = asyncio.create_task(client.search_hotels(dest, date, checkout_date, max_price=budget//nights))

    flights = await flights_task
    hotels = await hotels_task

    # pick cheapest flight + cheapest hotel for baseline
    best_flight = min(flights, key=lambda f: f["price_inr"])
    best_hotel = min(hotels, key=lambda h: h["nightly_price_inr"])

    # compare fares among top 3 flights (if available)
    top_flight_ids = [f["flight_id"] for f in flights[:3]]
    compare = await client.compare_fares(top_flight_ids) if top_flight_ids else {}

    total_estimated = best_flight["price_inr"] + best_hotel["nightly_price_inr"] * nights
    plan = {
        "flight_choice": best_flight,
        "hotel_choice": best_hotel,
        "nights": nights,
        "total_estimated_inr": total_estimated,
        "within_budget": total_estimated <= budget,
        "fare_comparison": compare
    }

    # If user asked to book and within budget, perform mock booking(s)
    bookings = {}
    if do_book and plan["within_budget"]:
        flight_booking = await client.book_flight(best_flight["flight_id"], parsed["passenger_name"], parsed["email"])
        hotel_booking = await client.book_hotel(best_hotel["hotel_id"], parsed["passenger_name"], parsed["email"])
        bookings = {"flight_booking": flight_booking, "hotel_booking": hotel_booking}

    return {"plan": plan, "bookings": bookings}

# CLI test run
if __name__ == "__main__":
    user = "Plan a 5-day trip to Dubai in December under 60000 including flights + hotel"
    res = asyncio.run(plan_and_book(user, do_book=False))
    import json
    print(json.dumps(res, indent=2))
