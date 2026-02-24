"""
Management command to seed the database with sample property data
matching the FindQo API format.

Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from properties.models import (
    County, CountyArea, SellerType, Seller,
    Section, Aisle, Property, PropertyImage, PropertySizeUnit
)

# Using real Unsplash property images that reliably load
HOUSE_IMGS = [
    "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800",
    "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800",
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800",
    "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800",
    "https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?w=800",
    "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
    "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800",
    "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800",
]

APT_IMGS = [
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800",
    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800",
    "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800",
    "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
    "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800",
    "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800",
    "https://images.unsplash.com/photo-1617103996702-96ff29b1c467?w=800",
    "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800",
]

STUDIO_IMGS = [
    "https://images.unsplash.com/photo-1598928636135-d146006ff4be?w=800",
    "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
    "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
]

SAMPLE_DATA = [
    # ── DUBLIN ────────────────────────────────────────────────────────────────
    {
        "id": 8333,
        "title": "2 Bedroom Apartment for Rent in Blackrock, Dublin",
        "description": "Stunning modern apartment in the heart of Blackrock. Fully furnished with high-end finishes, private balcony with sea views, secure parking and access to a residents gym.",
        "bedroom_count": 2, "bathroom_count": 2,
        "property_type": "apartment", "price": 2800, "ber": "B2", "size": 81,
        "county": "Dublin (County)", "county_area": "Blackrock, Dublin (County)",
        "address": "Apt 41, Booterstown Wood, Booterstown Avenue, Blackrock, Co. Dublin, A94 W673",
        "eir_code": "A94 W673",
        "seller_name": "Brigid Whitehead", "seller_email": "brigidwhitehead@gmail.com",
        "seller_phone": "876196750", "is_private": True,
        "images": APT_IMGS[:3],
    },
    {
        "id": 8198,
        "title": "2 Bedroom Apartment for Rent in Dublin 2",
        "description": "Luxury city-centre apartment in Trinity Square. Minutes from Trinity College, Grafton Street and Dublins top restaurants. Concierge service, gym and rooftop terrace included.",
        "bedroom_count": 2, "bathroom_count": 1,
        "property_type": "apartment", "price": 2800, "ber": "C3", "size": 72,
        "county": "Dublin - All", "county_area": "Dublin 2",
        "address": "Apt 65, Trinity Square, Townsend Street, Dublin 2, D02 X981",
        "eir_code": "D02 X981",
        "seller_name": "Kevin Cassidy", "seller_email": "kevincassidy313@gmail.com",
        "seller_phone": "863995202", "is_private": True,
        "images": APT_IMGS[3:6],
    },
    {
        "id": 8101,
        "title": "3 Bedroom Semi-Detached House for Rent in Swords, Dublin",
        "description": "Spacious family home in a quiet cul-de-sac in Swords. Close to Dublin Airport, the M1 motorway and Swords town centre. Large rear garden, two parking spaces.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "semi-detached", "price": 2400, "ber": "B3", "size": 110,
        "county": "Dublin (County)", "county_area": "Swords, Dublin (County)",
        "address": "14 Applewood Heights, Swords, Co. Dublin, K67 F2P4",
        "eir_code": "K67 F2P4",
        "seller_name": "Sherry FitzGerald", "seller_email": "swords@sherryfitz.ie",
        "seller_phone": "018401000", "is_private": False,
        "images": HOUSE_IMGS[:3],
    },
    {
        "id": 8102,
        "title": "1 Bedroom Apartment for Rent in Rathmines, Dublin 6",
        "description": "Bright ground-floor apartment on tree-lined road in Rathmines. Open-plan living, modern kitchen, own patio area. Walking distance to Ranelagh and the Grand Canal.",
        "bedroom_count": 1, "bathroom_count": 1,
        "property_type": "apartment", "price": 1900, "ber": "D1", "size": 55,
        "county": "Dublin - All", "county_area": "Dublin 6",
        "address": "Apt 3, Leinster Road, Rathmines, Dublin 6, D06 K279",
        "eir_code": "D06 K279",
        "seller_name": "DNG Estate Agents", "seller_email": "rathmines@dng.ie",
        "seller_phone": "014972000", "is_private": False,
        "images": APT_IMGS[1:4],
    },
    {
        "id": 8103,
        "title": "4 Bedroom Detached House for Rent in Malahide, Dublin",
        "description": "Exceptional detached family home in prestigious Malahide village. South-facing garden, double garage, and walking distance to the beach, marina and DART station.",
        "bedroom_count": 4, "bathroom_count": 3,
        "property_type": "detached", "price": 3800, "ber": "A3", "size": 185,
        "county": "Dublin (County)", "county_area": "Malahide, Dublin (County)",
        "address": "7 Strand Road, Malahide, Co. Dublin, K36 EK28",
        "eir_code": "K36 EK28",
        "seller_name": "Lisney Estate Agents", "seller_email": "malahide@lisney.com",
        "seller_phone": "018451000", "is_private": False,
        "images": HOUSE_IMGS[2:5],
    },
    {
        "id": 8104,
        "title": "Studio Apartment for Rent in Dublin 1",
        "description": "Modern studio apartment in the heart of Dublin city centre. Fully furnished, high-speed broadband, minutes from O Connell Street, LUAS and bus routes. Ideal for professionals.",
        "bedroom_count": 1, "bathroom_count": 1,
        "property_type": "studio", "price": 1450, "ber": "C1", "size": 38,
        "county": "Dublin - All", "county_area": "Dublin 1",
        "address": "Apt 12, City Quarter, Parnell Street, Dublin 1, D01 R2P3",
        "eir_code": "D01 R2P3",
        "seller_name": "Patricia Nolan", "seller_email": "patricia.nolan@gmail.com",
        "seller_phone": "871234567", "is_private": True,
        "images": STUDIO_IMGS,
    },
    {
        "id": 8105,
        "title": "3 Bedroom Terraced House for Rent in Clondalkin, Dublin 22",
        "description": "Well-presented mid-terraced home in a mature residential estate in Clondalkin. New kitchen, gas central heating, enclosed rear garden, one parking space. Near Red Cow LUAS.",
        "bedroom_count": 3, "bathroom_count": 1,
        "property_type": "terraced-house", "price": 1950, "ber": "D2", "size": 95,
        "county": "Dublin - All", "county_area": "Dublin 22",
        "address": "23 Lealand Road, Clondalkin, Dublin 22, D22 XP58",
        "eir_code": "D22 XP58",
        "seller_name": "REA McGreal Burke", "seller_email": "clondalkin@reamcgreal.ie",
        "seller_phone": "014573000", "is_private": False,
        "images": HOUSE_IMGS[4:7],
    },

    # ── CORK ──────────────────────────────────────────────────────────────────
    {
        "id": 8200,
        "title": "2 Bedroom Apartment for Rent in Cork City Centre",
        "description": "Contemporary apartment in the heart of Cork city. Floor-to-ceiling windows, juliet balcony, underground parking. Steps from Patrick Street, English Market and the River Lee.",
        "bedroom_count": 2, "bathroom_count": 2,
        "property_type": "apartment", "price": 1850, "ber": "B1", "size": 78,
        "county": "Cork", "county_area": "Cork City",
        "address": "Apt 8, Navigation Square, Albert Quay, Cork City, T12 XK54",
        "eir_code": "T12 XK54",
        "seller_name": "Sherry FitzGerald Cork", "seller_email": "cork@sherryfitz.ie",
        "seller_phone": "214277000", "is_private": False,
        "images": APT_IMGS[2:5],
    },
    {
        "id": 8201,
        "title": "4 Bedroom Detached House for Rent in Ballincollig, Cork",
        "description": "Magnificent detached family home in sought-after Ballincollig. Generous room sizes throughout, landscaped gardens, double garage and quiet cul-de-sac location.",
        "bedroom_count": 4, "bathroom_count": 3,
        "property_type": "detached", "price": 2600, "ber": "A2", "size": 200,
        "county": "Cork", "county_area": "Ballincollig, Cork",
        "address": "12 The Oaks, Coolroe Meadows, Ballincollig, Co. Cork, P31 XD92",
        "eir_code": "P31 XD92",
        "seller_name": "Savills Cork", "seller_email": "cork@savills.ie",
        "seller_phone": "214277500", "is_private": False,
        "images": HOUSE_IMGS[0:3],
    },
    {
        "id": 8203,
        "title": "3 Bedroom Semi-Detached for Rent in Douglas, Cork",
        "description": "Bright and spacious semi-detached home in the popular village of Douglas. South-facing garden, recently refurbished kitchen and bathrooms, excellent transport links to city.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "semi-detached", "price": 2100, "ber": "C2", "size": 118,
        "county": "Cork", "county_area": "Douglas, Cork",
        "address": "45 Maryborough Hill, Douglas, Cork, T12 F8YK",
        "eir_code": "T12 F8YK",
        "seller_name": "O Brien Keane", "seller_email": "info@obrienkeane.ie",
        "seller_phone": "214891200", "is_private": False,
        "images": HOUSE_IMGS[3:6],
    },
    {
        "id": 8204,
        "title": "1 Bedroom Apartment for Rent in Mahon, Cork",
        "description": "Modern one-bedroom apartment in Mahon Point. Open-plan living area, private balcony, one parking space. Close to Mahon Point Shopping Centre and easy access to N25.",
        "bedroom_count": 1, "bathroom_count": 1,
        "property_type": "apartment", "price": 1400, "ber": "B3", "size": 58,
        "county": "Cork", "county_area": "Mahon, Cork",
        "address": "Apt 22, Marina Village, Mahon, Cork, T12 HV78",
        "eir_code": "T12 HV78",
        "seller_name": "Michael Murphy", "seller_email": "michael.murphy.cork@gmail.com",
        "seller_phone": "872345678", "is_private": True,
        "images": APT_IMGS[5:8],
    },

    # ── GALWAY ────────────────────────────────────────────────────────────────
    {
        "id": 8300,
        "title": "2 Bedroom Apartment for Rent in Galway City",
        "description": "Stylish apartment in Galway city centre, a short stroll from Shop Street and Eyre Square. Open-plan kitchen and living room, Juliette balcony, one secure parking space.",
        "bedroom_count": 2, "bathroom_count": 1,
        "property_type": "apartment", "price": 1750, "ber": "C1", "size": 70,
        "county": "Galway", "county_area": "Galway City",
        "address": "Apt 5, Merchant s Road Central, Galway, H91 XD23",
        "eir_code": "H91 XD23",
        "seller_name": "DNG Maxwell Heaslip", "seller_email": "galway@dng.ie",
        "seller_phone": "91565261", "is_private": False,
        "images": APT_IMGS[0:3],
    },
    {
        "id": 8301,
        "title": "3 Bedroom House for Rent in Salthill, Galway",
        "description": "Charming terraced house metres from the Salthill Promenade. Three good-sized bedrooms, sunny south-facing rear garden, gas central heating. Short bus ride to NUIG.",
        "bedroom_count": 3, "bathroom_count": 1,
        "property_type": "terraced-house", "price": 2200, "ber": "D1", "size": 100,
        "county": "Galway", "county_area": "Salthill, Galway",
        "address": "18 Grattan Road, Salthill, Galway, H91 KX34",
        "eir_code": "H91 KX34",
        "seller_name": "Sherry FitzGerald Galway", "seller_email": "galway@sherryfitz.ie",
        "seller_phone": "91569111", "is_private": False,
        "images": HOUSE_IMGS[1:4],
    },
    {
        "id": 8302,
        "title": "4 Bedroom Detached House for Rent in Oranmore, Galway",
        "description": "Impressive A-rated detached home in Oranmore village. Features an open-plan kitchen/diner, utility room, home office, double garage and beautifully landscaped garden.",
        "bedroom_count": 4, "bathroom_count": 3,
        "property_type": "detached", "price": 2800, "ber": "A2", "size": 195,
        "county": "Galway", "county_area": "Oranmore, Galway",
        "address": "3 Clarin Walk, Oranmore, Co. Galway, H91 PY62",
        "eir_code": "H91 PY62",
        "seller_name": "Lisney Galway", "seller_email": "galway@lisney.com",
        "seller_phone": "91530000", "is_private": False,
        "images": HOUSE_IMGS[4:7],
    },

    # ── MEATH ─────────────────────────────────────────────────────────────────
    {
        "id": 8221,
        "title": "3 Bedroom House for Rent in Drogheda, Meath",
        "description": "Spacious 3-bed family home in a quiet residential area. Close to schools, shops and M1 motorway access. Private rear garden and off-street parking.",
        "bedroom_count": 3, "bathroom_count": 3,
        "property_type": "house", "price": 2500, "ber": "C3", "size": 120,
        "county": "Meath", "county_area": "Drogheda, Meath",
        "address": "16 Colpe Park, Deepforde, Drogheda, Co. Meath",
        "eir_code": "",
        "seller_name": "Thomas Byrne Auctioneer & Valuer", "seller_email": "info@thomasbyrne.ie",
        "seller_phone": "0419832927", "is_private": False,
        "images": HOUSE_IMGS[0:3],
    },
    {
        "id": 8400,
        "title": "2 Bedroom Apartment for Rent in Navan, Meath",
        "description": "Well-presented apartment in Navan town centre. Two double bedrooms, open-plan living area, private balcony and one parking space. Close to all amenities and bus routes to Dublin.",
        "bedroom_count": 2, "bathroom_count": 1,
        "property_type": "apartment", "price": 1500, "ber": "C2", "size": 68,
        "county": "Meath", "county_area": "Navan, Meath",
        "address": "Apt 14, Copper Beech Court, Trim Road, Navan, Co. Meath, C15 X2F9",
        "eir_code": "C15 X2F9",
        "seller_name": "Sherry FitzGerald Navan", "seller_email": "navan@sherryfitz.ie",
        "seller_phone": "469021000", "is_private": False,
        "images": APT_IMGS[3:6],
    },
    {
        "id": 8401,
        "title": "3 Bedroom Semi-Detached for Rent in Trim, Meath",
        "description": "Lovely semi-detached home in a mature estate close to Trim Castle and town centre. Three bedrooms, rear garden with patio, gas central heating throughout.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "semi-detached", "price": 1800, "ber": "C1", "size": 108,
        "county": "Meath", "county_area": "Trim, Meath",
        "address": "8 Castle Arch, Trim, Co. Meath, C15 YF82",
        "eir_code": "C15 YF82",
        "seller_name": "Coonan Property", "seller_email": "trim@coonan.ie",
        "seller_phone": "469431111", "is_private": False,
        "images": HOUSE_IMGS[2:5],
    },

    # ── LOUTH ─────────────────────────────────────────────────────────────────
    {
        "id": 8220,
        "title": "1 Bedroom Apartment for Rent in Drogheda, Louth",
        "description": "Charming 1-bed apartment in a historic building on Fair Street. Walking distance to Drogheda town centre, restaurants and public transport.",
        "bedroom_count": 1, "bathroom_count": 1,
        "property_type": "apartment", "price": 1632, "ber": "D1", "size": 52,
        "county": "Louth", "county_area": "Drogheda, Louth",
        "address": "Apartment, Fair Street House, Fair Street, Drogheda, Co. Louth",
        "eir_code": "",
        "seller_name": "Thomas Byrne Auctioneer & Valuer", "seller_email": "info@thomasbyrne.ie",
        "seller_phone": "0419832927", "is_private": False,
        "images": APT_IMGS[1:4],
    },
    {
        "id": 8500,
        "title": "3 Bedroom Detached House for Rent in Dundalk, Louth",
        "description": "Superb detached home in a sought-after estate in Dundalk. South-facing rear garden, attic conversion, double garage. Minutes from Dundalk town and the M1.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "detached", "price": 2000, "ber": "B2", "size": 140,
        "county": "Louth", "county_area": "Dundalk, Louth",
        "address": "22 Ard Easmuinn, Dundalk, Co. Louth, A91 XY34",
        "eir_code": "A91 XY34",
        "seller_name": "Quillsen Estate Agents", "seller_email": "info@quillsen.ie",
        "seller_phone": "429335000", "is_private": False,
        "images": HOUSE_IMGS[5:8],
    },

    # ── LIMERICK ──────────────────────────────────────────────────────────────
    {
        "id": 8202,
        "title": "3 Bedroom Terraced House for Rent in Newcastle West, Limerick",
        "description": "Well-maintained terraced house ideal for families. Large living room, modern kitchen and sunny back garden. Close to all local amenities.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "terraced-house", "price": 1034, "ber": "", "size": 0,
        "county": "Limerick", "county_area": "Newcastle West, Limerick",
        "address": "95 Maiden Street, Newcastle West Co Limerick",
        "eir_code": "",
        "seller_name": "Resource Property Management", "seller_email": "tracey@rpmproperty.ie",
        "seller_phone": "863955597", "is_private": False,
        "images": HOUSE_IMGS[3:6],
    },
    {
        "id": 8600,
        "title": "2 Bedroom Apartment for Rent in Limerick City",
        "description": "Modern apartment in the heart of Limerick city centre. Open-plan living, city views from private balcony, secure underground parking. Close to UL, hospitals and transport.",
        "bedroom_count": 2, "bathroom_count": 1,
        "property_type": "apartment", "price": 1450, "ber": "B3", "size": 74,
        "county": "Limerick", "county_area": "Limerick City",
        "address": "Apt 9, Riverpoint, Bishops Quay, Limerick, V94 X2K1",
        "eir_code": "V94 X2K1",
        "seller_name": "Sherry FitzGerald Limerick", "seller_email": "limerick@sherryfitz.ie",
        "seller_phone": "61421789", "is_private": False,
        "images": APT_IMGS[6:9],
    },
    {
        "id": 8601,
        "title": "4 Bedroom Detached House for Rent in Dooradoyle, Limerick",
        "description": "Spacious family home in the popular suburb of Dooradoyle. Excellent schools nearby, Crescent Shopping Centre minutes away. Large garden, garage and quiet estate setting.",
        "bedroom_count": 4, "bathroom_count": 3,
        "property_type": "detached", "price": 2300, "ber": "C1", "size": 168,
        "county": "Limerick", "county_area": "Dooradoyle, Limerick",
        "address": "15 Orchard View, Dooradoyle, Limerick, V94 TF82",
        "eir_code": "V94 TF82",
        "seller_name": "Rooney Auctioneers", "seller_email": "info@rooneys.ie",
        "seller_phone": "61415799", "is_private": False,
        "images": HOUSE_IMGS[0:3],
    },

    # ── WEXFORD ───────────────────────────────────────────────────────────────
    {
        "id": 8134,
        "title": "3 Bedroom Apartment for Rent in New Ross, Wexford",
        "description": "Generous 3-bedroom apartment in a modern development. River views, allocated parking and close to New Ross town. Suitable for professionals or families.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "apartment", "price": 1400, "ber": "C1", "size": 92,
        "county": "Wexford", "county_area": "New Ross, Wexford",
        "address": "2 Rosbercon Court, Lower Rosbercon, New Ross, Co. Wexford",
        "eir_code": "",
        "seller_name": "Manor Properties", "seller_email": "brian@manorproperties.ie",
        "seller_phone": "879237573", "is_private": False,
        "images": APT_IMGS[2:5],
    },
    {
        "id": 8700,
        "title": "3 Bedroom Semi-Detached for Rent in Wexford Town",
        "description": "Attractive semi-detached in a quiet estate close to Wexford town centre. Three bedrooms, utility room, enclosed rear garden and off-street parking. Minutes from the quays.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "semi-detached", "price": 1650, "ber": "C3", "size": 112,
        "county": "Wexford", "county_area": "Wexford Town",
        "address": "7 Whitethorn Drive, Wexford Town, Co. Wexford, Y35 EH67",
        "eir_code": "Y35 EH67",
        "seller_name": "Kehoe & Associates", "seller_email": "info@kehoeassociates.ie",
        "seller_phone": "539145000", "is_private": False,
        "images": HOUSE_IMGS[1:4],
    },

    # ── KILDARE ───────────────────────────────────────────────────────────────
    {
        "id": 8800,
        "title": "3 Bedroom Semi-Detached for Rent in Naas, Kildare",
        "description": "Excellent family home in a mature estate in Naas. Three bedrooms, enclosed rear garden, gas central heating. Walking distance to Naas town, schools and sporting facilities.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "semi-detached", "price": 2000, "ber": "C2", "size": 105,
        "county": "Kildare", "county_area": "Naas, Kildare",
        "address": "11 Blessington Road, Naas, Co. Kildare, W91 FK23",
        "eir_code": "W91 FK23",
        "seller_name": "Sherry FitzGerald Naas", "seller_email": "naas@sherryfitz.ie",
        "seller_phone": "458881000", "is_private": False,
        "images": HOUSE_IMGS[2:5],
    },
    {
        "id": 8801,
        "title": "2 Bedroom Apartment for Rent in Newbridge, Kildare",
        "description": "Contemporary apartment in Newbridge town centre close to the Whitewater Shopping Centre. Open-plan layout, private balcony, one allocated parking space. Train to Dublin in 40 mins.",
        "bedroom_count": 2, "bathroom_count": 1,
        "property_type": "apartment", "price": 1650, "ber": "B2", "size": 72,
        "county": "Kildare", "county_area": "Newbridge, Kildare",
        "address": "Apt 7, Liffey Quarter, Edward Street, Newbridge, Co. Kildare, W12 RX56",
        "eir_code": "W12 RX56",
        "seller_name": "Coonan Property Kildare", "seller_email": "kildare@coonan.ie",
        "seller_phone": "458798000", "is_private": False,
        "images": APT_IMGS[4:7],
    },
    {
        "id": 8802,
        "title": "4 Bedroom Detached for Rent in Celbridge, Kildare",
        "description": "Impressive A-rated home in Celbridge backing onto woodland. Home office, utility room, large south-facing garden and double garage. Easy access to M4 and Leixlip train station.",
        "bedroom_count": 4, "bathroom_count": 3,
        "property_type": "detached", "price": 2900, "ber": "A3", "size": 190,
        "county": "Kildare", "county_area": "Celbridge, Kildare",
        "address": "4 Woodlands Drive, Celbridge, Co. Kildare, W23 XF91",
        "eir_code": "W23 XF91",
        "seller_name": "RE/MAX Kildare", "seller_email": "kildare@remax.ie",
        "seller_phone": "16303222", "is_private": False,
        "images": HOUSE_IMGS[4:7],
    },

    # ── WICKLOW ───────────────────────────────────────────────────────────────
    {
        "id": 8900,
        "title": "2 Bedroom Apartment for Rent in Bray, Wicklow",
        "description": "Bright and airy apartment on the seafront in Bray. Sea views from every room, private balcony, underground parking. DART to Dublin city in 30 minutes.",
        "bedroom_count": 2, "bathroom_count": 1,
        "property_type": "apartment", "price": 2100, "ber": "B1", "size": 76,
        "county": "Wicklow", "county_area": "Bray, Wicklow",
        "address": "Apt 11, Strand Court, Strand Road, Bray, Co. Wicklow, A98 XF21",
        "eir_code": "A98 XF21",
        "seller_name": "Sherry FitzGerald Bray", "seller_email": "bray@sherryfitz.ie",
        "seller_phone": "12864000", "is_private": False,
        "images": APT_IMGS[0:3],
    },
    {
        "id": 8901,
        "title": "3 Bedroom House for Rent in Greystones, Wicklow",
        "description": "Charming three-bedroom terraced home steps from Greystones beach and DART station. Sunny rear garden, recently renovated throughout. Popular coastal village lifestyle.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "terraced-house", "price": 2400, "ber": "C2", "size": 108,
        "county": "Wicklow", "county_area": "Greystones, Wicklow",
        "address": "9 Killincarrig Road, Greystones, Co. Wicklow, A63 HD72",
        "eir_code": "A63 HD72",
        "seller_name": "Byrne Sheridan", "seller_email": "info@byrnesheridan.ie",
        "seller_phone": "12876000", "is_private": False,
        "images": HOUSE_IMGS[0:3],
    },

    # ── KERRY ─────────────────────────────────────────────────────────────────
    {
        "id": 9000,
        "title": "2 Bedroom Apartment for Rent in Tralee, Kerry",
        "description": "Well-appointed apartment in Tralee town centre. Two bedrooms, modern kitchen, private parking. Close to Brandon Hotel, the Rose of Tralee Festival grounds and bus services.",
        "bedroom_count": 2, "bathroom_count": 1,
        "property_type": "apartment", "price": 1200, "ber": "C3", "size": 65,
        "county": "Kerry", "county_area": "Tralee, Kerry",
        "address": "Apt 4, Ashe Street Court, Ashe Street, Tralee, Co. Kerry, V92 HX31",
        "eir_code": "V92 HX31",
        "seller_name": "Horan Estate Agents", "seller_email": "info@horanestateagents.ie",
        "seller_phone": "667127000", "is_private": False,
        "images": APT_IMGS[1:4],
    },
    {
        "id": 9001,
        "title": "3 Bedroom Bungalow for Rent in Killarney, Kerry",
        "description": "Delightful detached bungalow on the outskirts of Killarney with mountain views. Large garden, off-street parking. Ideal for nature lovers — minutes to Killarney National Park.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "bungalow", "price": 1600, "ber": "D1", "size": 115,
        "county": "Kerry", "county_area": "Killarney, Kerry",
        "address": "Lakeview Cottage, Muckross Road, Killarney, Co. Kerry, V93 PX72",
        "eir_code": "V93 PX72",
        "seller_name": "Daly Auctioneers", "seller_email": "info@dalyauctioneers.ie",
        "seller_phone": "6431068", "is_private": False,
        "images": HOUSE_IMGS[3:6],
    },

    # ── WATERFORD ─────────────────────────────────────────────────────────────
    {
        "id": 9100,
        "title": "2 Bedroom Apartment for Rent in Waterford City",
        "description": "Excellent apartment in Waterford city, just off the Quays. Open-plan living with river views, secure parking and close to all amenities. SETU Waterford campus nearby.",
        "bedroom_count": 2, "bathroom_count": 1,
        "property_type": "apartment", "price": 1350, "ber": "B3", "size": 69,
        "county": "Waterford", "county_area": "Waterford City",
        "address": "Apt 6, The Granary, Hanover Street, Waterford City, X91 YT43",
        "eir_code": "X91 YT43",
        "seller_name": "Sherry FitzGerald Waterford", "seller_email": "waterford@sherryfitz.ie",
        "seller_phone": "51876000", "is_private": False,
        "images": APT_IMGS[5:8],
    },
    {
        "id": 9101,
        "title": "4 Bedroom Detached for Rent in Dunmore East, Waterford",
        "description": "Stunning coastal home overlooking Dunmore East harbour. Four bedrooms, wrap-around deck, private garden and breath-taking sea views. A rare find on the Copper Coast.",
        "bedroom_count": 4, "bathroom_count": 3,
        "property_type": "detached", "price": 2500, "ber": "C1", "size": 175,
        "county": "Waterford", "county_area": "Dunmore East, Waterford",
        "address": "Harbour View House, Dunmore East, Co. Waterford, X91 PQ82",
        "eir_code": "X91 PQ82",
        "seller_name": "Fitzgerald Auctioneers", "seller_email": "info@fitzgeraldauct.ie",
        "seller_phone": "51383000", "is_private": False,
        "images": HOUSE_IMGS[1:4],
    },

    # ── CLARE ─────────────────────────────────────────────────────────────────
    {
        "id": 9200,
        "title": "3 Bedroom Semi-Detached for Rent in Ennis, Clare",
        "description": "Superb family home in a quiet residential estate in Ennis. Three bedrooms, south-facing garden, gas central heating. Walking distance to Ennis town centre and schools.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "semi-detached", "price": 1600, "ber": "C2", "size": 110,
        "county": "Clare", "county_area": "Ennis, Clare",
        "address": "19 Harmony Row, Ennis, Co. Clare, V95 FK42",
        "eir_code": "V95 FK42",
        "seller_name": "Considine Auctioneers", "seller_email": "info@considine.ie",
        "seller_phone": "65684000", "is_private": False,
        "images": HOUSE_IMGS[5:8],
    },

    # ── TIPPERARY ─────────────────────────────────────────────────────────────
    {
        "id": 9300,
        "title": "3 Bedroom House for Rent in Clonmel, Tipperary",
        "description": "Spacious three-bedroom home in a mature estate in Clonmel. Large enclosed garden, off-street parking, gas central heating. Close to schools, shops and Clonmel Racecourse.",
        "bedroom_count": 3, "bathroom_count": 2,
        "property_type": "house", "price": 1300, "ber": "D2", "size": 102,
        "county": "Tipperary", "county_area": "Clonmel, Tipperary",
        "address": "34 Hillview Estate, Clonmel, Co. Tipperary, E91 XF23",
        "eir_code": "E91 XF23",
        "seller_name": "Quinn Property", "seller_email": "info@quinnproperty.ie",
        "seller_phone": "52621000", "is_private": False,
        "images": HOUSE_IMGS[0:3],
    },

    # ── SLIGO ─────────────────────────────────────────────────────────────────
    {
        "id": 9400,
        "title": "2 Bedroom Apartment for Rent in Sligo Town",
        "description": "Modern apartment in Sligo town centre. Two bedrooms, open-plan kitchen/living, parking space. Short walk to Sligo IT, restaurants and the picturesque Garavogue River.",
        "bedroom_count": 2, "bathroom_count": 1,
        "property_type": "apartment", "price": 1100, "ber": "C1", "size": 64,
        "county": "Sligo", "county_area": "Sligo Town",
        "address": "Apt 3, Wine Street Quarter, Wine Street, Sligo, F91 XD43",
        "eir_code": "F91 XD43",
        "seller_name": "Sotheby Sligo", "seller_email": "info@sothebys-sligo.ie",
        "seller_phone": "71914000", "is_private": False,
        "images": APT_IMGS[2:5],
    },
]


class Command(BaseCommand):
    help = "Seed the database with 40+ sample property listings across Ireland"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing properties before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            Property.objects.all().delete()
            Seller.objects.all().delete()
            County.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing data."))

        self.stdout.write("Seeding data...")

        # Size unit
        sqm, _ = PropertySizeUnit.objects.get_or_create(
            reference="square-meters",
            defaults={"name": "Square Meters", "symbol": "m²"}
        )

        # Sections & aisles
        rent_section, _ = Section.objects.get_or_create(
            reference="properties-for-rent",
            defaults={"name": "Properties FOR RENT", "translation_key": "n3590"}
        )
        Section.objects.get_or_create(
            reference="properties-for-sale",
            defaults={"name": "Properties FOR SALE", "translation_key": "n3591"}
        )
        rent_res, _ = Aisle.objects.get_or_create(
            reference="rent-residential",
            defaults={"section": rent_section, "name": "Rent Residential", "translation_key": "n793"}
        )

        # Seller types
        private_type, _ = SellerType.objects.get_or_create(id=1, defaults={"name": "Private"})
        agent_type, _ = SellerType.objects.get_or_create(id=2, defaults={"name": "Agent/Broker"})

        created_count = 0
        skipped_count = 0

        for item in SAMPLE_DATA:
            # County
            county_name = item["county"]
            county_ref = (
                county_name.lower()
                .replace(" ", "-").replace("(", "").replace(")", "")
                .replace("--", "-").strip("-")
            )
            county, _ = County.objects.get_or_create(
                reference=county_ref,
                defaults={"name": county_name}
            )

            # County area
            area_name = item["county_area"]
            area_ref = area_name.lower().replace(" ", "-").replace(",", "").replace("'", "")[:50]
            area, _ = CountyArea.objects.get_or_create(
                county=county,
                reference=area_ref,
                defaults={"name": area_name}
            )

            # Seller
            seller_type = private_type if item["is_private"] else agent_type
            seller_ref = (
                item["seller_name"].lower()
                .replace(" ", "-").replace("&", "and").replace("'", "")[:50]
            )
            seller, _ = Seller.objects.get_or_create(
                email=item["seller_email"],
                defaults={
                    "name": item["seller_name"],
                    "profile_id": seller_ref,
                    "seller_type": seller_type,
                    "phone": item["seller_phone"],
                    "is_verified": True,
                    "picture": "https://images.findqo.com/profile-avatar/Default.png",
                    "tagline": "" if item["is_private"] else "Real Estate Broker",
                }
            )

            # Property
            prop, created = Property.objects.get_or_create(
                id=item["id"],
                defaults={
                    "section": rent_section,
                    "aisle": rent_res,
                    "seller": seller,
                    "county": county,
                    "county_area": area,
                    "title": item["title"],
                    "description": item.get("description", ""),
                    "property_type": item["property_type"],
                    "bedroom_count": item["bedroom_count"],
                    "bathroom_count": item["bathroom_count"],
                    "price_min_value": item["price"],
                    "ber": item["ber"],
                    "ad_address": item["address"],
                    "eir_code": item["eir_code"],
                    "property_size_value": item.get("size", 0),
                    "property_size_unit": sqm,
                }
            )

            if created:
                for idx, img_url in enumerate(item["images"]):
                    PropertyImage.objects.create(
                        property=prop,
                        url=img_url,
                        is_cover=(idx == 0),
                        active=True,
                        order=idx,
                    )
                created_count += 1
                self.stdout.write(f"  ✓ Created: {prop.title}")
            else:
                skipped_count += 1
                self.stdout.write(f"  - Exists:  {prop.title}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! {created_count} created, {skipped_count} already existed."
            )
        )