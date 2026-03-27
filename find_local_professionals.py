"""
find_local_professionals.py
----------------------------
Used by the listing-agent during Phase 1D to find vetted local professionals
near any property address — live from Google Places API.

No static database. Every search returns current ratings, phone numbers,
and hours pulled at the time of the listing intake.

Usage (called by listing-agent):
    python find_local_professionals.py --address "123 Oak Ave, Orange CA 92868" --categories all
    python find_local_professionals.py --address "456 Elm St, Anaheim CA 92801" --categories "photographer,inspector"
    python find_local_professionals.py --lat 33.787 --lng -117.853 --categories all

Output:
    Writes results to data/progress/professionals_[property_id].json
    Prints a formatted recommendation block for the agent to deliver to the seller

Requirements:
    pip install googlemaps requests

Setup:
    Set GOOGLE_PLACES_API_KEY in your environment or .env file.
    The API key needs Places API (New) enabled in Google Cloud Console.
    Cost: ~10,000 free Nearby Search requests/month on the Essentials tier.
    At ~8 searches per listing (one per category), that's ~1,250 free listings/month
    before any charges. At $0.04/request after free tier, each listing costs ~$0.32.
"""

import os
import json
import argparse
import requests
from datetime import datetime

# ── CONFIGURATION ─────────────────────────────────────────────────────────────

GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "")

# Radius in meters to search around the property
SEARCH_RADIUS = 25000  # 25km — covers metro area without going too far

# How many results to return per category (we show top 3)
MAX_RESULTS = 3

# Minimum rating to include in results
MIN_RATING = 4.0

# Minimum number of reviews to trust the rating
MIN_REVIEWS = 10

# ── CATEGORY DEFINITIONS ──────────────────────────────────────────────────────
# Each category has:
#   - keyword: what to search for in Google Places
#   - type: Google Places type filter (helps narrow results)
#   - why_needed: plain-English explanation for the seller
#   - when_to_recommend: logic hint for the listing agent
#   - typical_cost: what the seller should budget

CATEGORIES = {
    "photographer": {
        "keyword": "real estate photographer",
        "type": "establishment",
        "why_needed": "Professional photos are the single most impactful thing you can do for your listing. Homes with pro photos sell faster and attract more serious buyers.",
        "when_to_recommend": "Always — unless seller already has professional photos",
        "typical_cost": "$150–$400 depending on home size",
        "urgency": "Book 5–7 days before listing goes live",
    },
    "stager": {
        "keyword": "home staging real estate",
        "type": "establishment",
        "why_needed": "Staged homes sell faster and photograph better. Especially important for vacant homes or dated interiors.",
        "when_to_recommend": "If home is vacant, sparsely furnished, or seller asks about presentation",
        "typical_cost": "$500–$2,000 depending on home size and rental period",
        "urgency": "Must be done before photography shoot",
    },
    "inspector": {
        "keyword": "home inspection real estate",
        "type": "establishment",
        "why_needed": "A pre-listing inspection shows you exactly what a buyer's inspector will find — before they find it. Fixes issues proactively, prevents escrow surprises.",
        "when_to_recommend": "Always for homes 15+ years old, or when condition flags exist",
        "typical_cost": "$300–$450 for a standard single-family home",
        "urgency": "Schedule before listing goes live",
    },
    "termite": {
        "keyword": "termite pest control inspection",
        "type": "establishment",
        "why_needed": "Termite inspection is required or expected in most California transactions. Better to know now than during escrow negotiations.",
        "when_to_recommend": "Always in California",
        "typical_cost": "$75–$150 for inspection; treatment extra if needed",
        "urgency": "Can happen anytime before escrow opens",
    },
    "cleaner": {
        "keyword": "house cleaning deep clean",
        "type": "establishment",
        "why_needed": "A professional deep clean before photography makes a visible difference — especially kitchens, bathrooms, and windows.",
        "when_to_recommend": "Always before photography shoot",
        "typical_cost": "$200–$400 for a thorough pre-listing clean",
        "urgency": "Book 1–2 days before photo shoot",
    },
    "locksmith": {
        "keyword": "locksmith lockbox installation",
        "type": "locksmith",
        "why_needed": "A lockbox lets agents access your home for showings without you needing to be present or hand off keys every time.",
        "when_to_recommend": "When seller chooses lockbox access for showings",
        "typical_cost": "$25–$40 for a combo lockbox (Amazon/Home Depot); $75–$150 for professional electronic install",
        "urgency": "Install before listing goes live",
    },
    "attorney": {
        "keyword": "real estate attorney lawyer",
        "type": "lawyer",
        "why_needed": "As a FSBO seller, you're signing contracts directly. A real estate attorney can review offers before you accept — cost is $200–$500 and can save you from unfavorable terms.",
        "when_to_recommend": "First-time sellers, complex ownership situations, or when first offer arrives",
        "typical_cost": "$200–$500 for offer review; varies for full representation",
        "urgency": "Have a contact ready before offers arrive",
    },
    "escrow": {
        "keyword": "escrow title company real estate",
        "type": "establishment",
        "why_needed": "Escrow is required for all California real estate transactions. The escrow/title company holds funds and handles all closing paperwork.",
        "when_to_recommend": "As soon as an offer is accepted",
        "typical_cost": "0.5%–1% of sale price (split between buyer and seller)",
        "urgency": "Open escrow within 1–3 days of accepted offer",
    },
}

# ── GEOCODING ─────────────────────────────────────────────────────────────────

def geocode_address(address: str) -> tuple[float, float] | None:
    """Convert an address string to lat/lng coordinates."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_PLACES_API_KEY}
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    if data.get("status") == "OK" and data.get("results"):
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None


# ── PLACES SEARCH ─────────────────────────────────────────────────────────────

def search_nearby(lat: float, lng: float, keyword: str, place_type: str) -> list[dict]:
    """
    Search Google Places Nearby Search for businesses matching keyword near lat/lng.
    Returns cleaned list of results sorted by rating.
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": keyword,
        "location": f"{lat},{lng}",
        "radius": SEARCH_RADIUS,
        "key": GOOGLE_PLACES_API_KEY,
    }
    if place_type != "establishment":
        params["type"] = place_type

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if data.get("status") not in ("OK", "ZERO_RESULTS"):
        print(f"  ⚠ Places API error: {data.get('status')} — {data.get('error_message', '')}")
        return []

    results = []
    for place in data.get("results", []):
        rating = place.get("rating", 0)
        review_count = place.get("user_ratings_total", 0)

        if rating < MIN_RATING or review_count < MIN_REVIEWS:
            continue

        result = {
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "rating": rating,
            "review_count": review_count,
            "place_id": place.get("place_id"),
            "phone": None,  # requires Place Details call
            "hours": None,
            "website": None,
        }
        results.append(result)

    # Sort by combined score: rating × log(reviews) to balance quality + volume
    import math
    results.sort(key=lambda r: r["rating"] * math.log(max(r["review_count"], 1)), reverse=True)

    return results[:MAX_RESULTS * 2]  # fetch extras before detail calls


def enrich_with_details(place_id: str) -> dict:
    """
    Fetch phone, hours, and website from Place Details API.
    This is a separate API call — use sparingly.
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,opening_hours,website",
        "key": GOOGLE_PLACES_API_KEY,
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if data.get("status") != "OK":
        return {}

    result = data.get("result", {})
    hours_data = result.get("opening_hours", {})
    weekday_text = hours_data.get("weekday_text", [])

    # Condense hours to a readable summary
    hours_summary = None
    if weekday_text:
        # Try to detect if it's 7-days with same hours
        if len(set(h.split(": ", 1)[-1] for h in weekday_text)) == 1:
            hours_summary = f"Daily: {weekday_text[0].split(': ', 1)[-1]}"
        else:
            hours_summary = "; ".join(weekday_text[:3]) + ("..." if len(weekday_text) > 3 else "")

    return {
        "phone": result.get("formatted_phone_number"),
        "hours": hours_summary,
        "website": result.get("website"),
    }


# ── MAIN SEARCH ───────────────────────────────────────────────────────────────

def find_professionals(lat: float, lng: float, categories: list[str]) -> dict:
    """
    Search for all requested professional categories near the given coordinates.
    Returns structured results dict.
    """
    results = {}
    for cat_key in categories:
        if cat_key not in CATEGORIES:
            print(f"  ⚠ Unknown category: {cat_key} — skipping")
            continue

        cat = CATEGORIES[cat_key]
        print(f"\n  Searching: {cat_key} ({cat['keyword']})...")

        places = search_nearby(lat, lng, cat["keyword"], cat["type"])

        # Enrich top 3 with phone + hours
        enriched = []
        for place in places[:MAX_RESULTS]:
            details = enrich_with_details(place["place_id"])
            place.update(details)
            enriched.append(place)

        results[cat_key] = {
            "category_info": {
                "why_needed": cat["why_needed"],
                "when_to_recommend": cat["when_to_recommend"],
                "typical_cost": cat["typical_cost"],
                "urgency": cat["urgency"],
            },
            "results": enriched,
        }
        print(f"  ✓ Found {len(enriched)} results for {cat_key}")

    return results


# ── FORMAT OUTPUT FOR AGENT ────────────────────────────────────────────────────

def format_for_agent(search_results: dict, address: str) -> str:
    """
    Format the search results as a clean text block
    the listing agent can read aloud to the seller.
    """
    lines = [
        "=" * 60,
        "LOCAL PROFESSIONAL RECOMMENDATIONS",
        f"For: {address}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "Live data from Google Places — ratings current as of today",
        "=" * 60,
        "",
        "IMPORTANT: We have no financial relationship with any of",
        "these businesses. Always call 2–3, get quotes, and choose",
        "whoever you're comfortable with.",
        "",
    ]

    for cat_key, cat_data in search_results.items():
        cat_info = cat_data["category_info"]
        results = cat_data["results"]

        lines.append(f"── {cat_key.upper()} ──────────────────────────────────")
        lines.append(f"Why: {cat_info['why_needed']}")
        lines.append(f"Cost: {cat_info['typical_cost']}")
        lines.append(f"Timing: {cat_info['urgency']}")
        lines.append("")

        if not results:
            lines.append("  No results found — try a broader search or ask for a referral.")
        else:
            for i, r in enumerate(results, 1):
                stars = "⭐" * round(r["rating"])
                lines.append(f"  {i}. {r['name']}")
                lines.append(f"     {stars} {r['rating']:.1f} ({r['review_count']:,} reviews)")
                if r.get("phone"):
                    lines.append(f"     📞 {r['phone']}")
                if r.get("address"):
                    lines.append(f"     📍 {r['address']}")
                if r.get("hours"):
                    lines.append(f"     🕐 {r['hours']}")
                if r.get("website"):
                    lines.append(f"     🌐 {r['website']}")
                lines.append("")

        lines.append("")

    return "\n".join(lines)


# ── SAVE TO FILE ───────────────────────────────────────────────────────────────

def save_results(search_results: dict, property_id: str, address: str):
    """Save results to data/progress/professionals_[property_id].json"""
    output = {
        "property_id": property_id,
        "address": address,
        "generated_at": datetime.now().isoformat(),
        "source": "Google Places API — live data",
        "professionals": search_results,
    }

    path = f"data/progress/professionals_{property_id}.json"
    os.makedirs("data/progress", exist_ok=True)
    with open(path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n  ✓ Saved to {path}")
    return path


# ── MOCK MODE (no API key) ─────────────────────────────────────────────────────

def mock_results(categories: list[str], address: str) -> dict:
    """
    Returns mock results when no API key is set.
    Used for development/testing without incurring API costs.
    """
    print("\n  ⚠ No GOOGLE_PLACES_API_KEY set — running in mock mode")
    print("  Set the env variable to get live results.\n")

    mock = {}
    for cat_key in categories:
        if cat_key not in CATEGORIES:
            continue
        cat = CATEGORIES[cat_key]
        mock[cat_key] = {
            "category_info": {
                "why_needed": cat["why_needed"],
                "when_to_recommend": cat["when_to_recommend"],
                "typical_cost": cat["typical_cost"],
                "urgency": cat["urgency"],
            },
            "results": [
                {
                    "name": f"[MOCK] Top {cat_key.title()} Near {address.split(',')[1].strip() if ',' in address else address}",
                    "address": "Result requires GOOGLE_PLACES_API_KEY",
                    "rating": 4.9,
                    "review_count": 250,
                    "phone": "Set API key for live data",
                    "hours": None,
                    "website": None,
                }
            ],
        }
    return mock


# ── CLI ENTRY POINT ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Find local professionals near a property")
    parser.add_argument("--address", help="Full property address")
    parser.add_argument("--lat", type=float, help="Latitude (alternative to address)")
    parser.add_argument("--lng", type=float, help="Longitude (alternative to address)")
    parser.add_argument("--property-id", default="unknown", help="Property ID for output file naming")
    parser.add_argument(
        "--categories",
        default="all",
        help=f"Comma-separated categories or 'all'. Options: {', '.join(CATEGORIES.keys())}",
    )
    args = parser.parse_args()

    # Resolve categories
    if args.categories == "all":
        cats = list(CATEGORIES.keys())
    else:
        cats = [c.strip() for c in args.categories.split(",")]

    print(f"\nPropAgent — Local Professional Search")
    print(f"Address: {args.address or f'{args.lat},{args.lng}'}")
    print(f"Categories: {', '.join(cats)}")
    print(f"Source: Google Places API (live)\n")

    # Get coordinates
    lat, lng = None, None
    address = args.address or ""

    if args.address and GOOGLE_PLACES_API_KEY:
        print("  Geocoding address...")
        coords = geocode_address(args.address)
        if coords:
            lat, lng = coords
            print(f"  ✓ Coordinates: {lat:.4f}, {lng:.4f}")
        else:
            print("  ✗ Could not geocode address — check address format")
            return
    elif args.lat and args.lng:
        lat, lng = args.lat, args.lng
    else:
        print("  ✗ Provide --address or --lat/--lng")
        return

    # Run search (or mock if no API key)
    if GOOGLE_PLACES_API_KEY:
        results = find_professionals(lat, lng, cats)
    else:
        results = mock_results(cats, address)

    # Format and print
    formatted = format_for_agent(results, address)
    print("\n" + formatted)

    # Save
    property_id = args.property_id.replace(" ", "_").replace("/", "_")
    save_results(results, property_id, address)


if __name__ == "__main__":
    main()
