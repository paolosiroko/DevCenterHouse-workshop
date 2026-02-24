import { useState, useEffect, useCallback } from "react";

// ─── API ──────────────────────────────────────────────────────────────────────
const API_BASE = "http://localhost:8000/api";

async function fetchProperties(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== "" && v !== null && v !== undefined) query.set(k, v);
  });
  const res = await fetch(`${API_BASE}/properties/?${query}`);
  return res.json();
}

async function fetchCounties() {
  const res = await fetch(`${API_BASE}/counties/`);
  return res.json();
}

async function sendEnquiry(data) {
  const res = await fetch(`${API_BASE}/enquiries/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

// ─── SAMPLE DATA (fallback for UI demo) ──────────────────────────────────────
const DEMO_PROPERTIES = [
  {
    id: 8333,
    title: "2 Bedroom Apartment for Rent in Blackrock, Dublin",
    description: "Stunning modern apartment in the heart of Blackrock. Fully furnished with high-end finishes, private balcony with sea views, secure parking, and access to a residents' gym.",
    property_type: "apartment",
    bedroom_count: 2,
    bathroom_count: 2,
    ber: "B2",
    location: { county: "Dublin (County)", county_area: "Blackrock, Dublin (County)", address: "Apt 41, Booterstown Wood, Booterstown Avenue, Blackrock, Co. Dublin" },
    price: { min_value: "2800", symbol: "€" },
    rental_period: "Monthly",
    property_size: { value: "81", parameter: "m²" },
    images: [
      { url: "https://images.findqo.com/ad-images/8333_1771918984_2688.jpg", is_cover: true },
      { url: "https://images.findqo.com/ad-images/8333_1771918994_9726.jpg" },
      { url: "https://images.findqo.com/ad-images/8333_1771919002_2216.jpg" },
    ],
    seller: { name: "Brigid Whitehead", is_verified: true },
    contact: { name: "Brigid Whitehead", email: "brigidwhitehead@gmail.com", phone: "876196750" },
    ad_link: "#",
  },
  {
    id: 8221,
    title: "3 Bedroom House for Rent in Drogheda, Meath",
    description: "Spacious 3-bed family home in a quiet residential area. Close to schools, shops, and motorway access. Private rear garden and off-street parking.",
    property_type: "house",
    bedroom_count: 3,
    bathroom_count: 3,
    ber: "C3",
    location: { county: "Meath", county_area: "Drogheda, Meath", address: "16 Colpe Park, Deepforde, Drogheda, Co. Meath" },
    price: { min_value: "2500", symbol: "€" },
    rental_period: "Monthly",
    property_size: { value: "0", parameter: "m²" },
    images: [
      { url: "https://images.findqo.com/ad-images/8221_1771596301_4523.jpg", is_cover: true },
      { url: "https://images.findqo.com/ad-images/8221_1771596301_5595.jpg" },
    ],
    seller: { name: "Thomas Byrne Auctioneer & Valuer", is_verified: true, tagline: "Real Estate Broker" },
    contact: { name: "Brendan Byrne", email: "info@thomasbyrne.ie", phone: "0419832927" },
    ad_link: "#",
  },
  {
    id: 8220,
    title: "1 Bedroom Apartment for Rent in Drogheda, Louth",
    description: "Charming 1-bed apartment in a historic building on Fair Street. Walking distance to Drogheda town centre, restaurants, and public transport.",
    property_type: "apartment",
    bedroom_count: 1,
    bathroom_count: 1,
    ber: "D1",
    location: { county: "Louth", county_area: "Drogheda, Louth", address: "Apartment, Fair Street House, Fair Street, Drogheda, Co. Louth" },
    price: { min_value: "1632", symbol: "€" },
    rental_period: "Monthly",
    property_size: { value: "0", parameter: "m²" },
    images: [
      { url: "https://images.findqo.com/ad-images/8220_1771596108_5783.jpg", is_cover: true },
      { url: "https://images.findqo.com/ad-images/8220_1771596108_4869.jpg" },
    ],
    seller: { name: "Thomas Byrne Auctioneer & Valuer", is_verified: true, tagline: "Real Estate Broker" },
    contact: { name: "Brendan Byrne", email: "info@thomasbyrne.ie", phone: "0419832927" },
    ad_link: "#",
  },
  {
    id: 8202,
    title: "3 Bedroom Terraced House for Rent in Newcastle West, Limerick",
    description: "Well-maintained terraced house ideal for families. Large living room, modern kitchen, and sunny back garden. Close to all local amenities.",
    property_type: "terraced-house",
    bedroom_count: 3,
    bathroom_count: 2,
    ber: "",
    location: { county: "Limerick", county_area: "Newcastle West, Limerick", address: "95 Maiden Street, Newcastle West Co Limerick" },
    price: { min_value: "1034", symbol: "€" },
    rental_period: "Monthly",
    property_size: { value: "0", parameter: "m²" },
    images: [
      { url: "https://images.findqo.com/ad-images/8202_1771506965_9754.jpg", is_cover: true },
      { url: "https://images.findqo.com/ad-images/8202_1771506965_9738.jpg" },
    ],
    seller: { name: "Resource Property Management", is_verified: true, tagline: "Real Estate Broker" },
    contact: { name: "Tracey", email: "tracey@rpmproperty.ie", phone: "863955597" },
    ad_link: "#",
  },
  {
    id: 8198,
    title: "2 Bedroom Apartment for Rent in Dublin 2",
    description: "Luxury city-centre apartment in Trinity Square development. Minutes from Trinity College, Grafton Street, and Dublin's top restaurants and cultural venues.",
    property_type: "apartment",
    bedroom_count: 2,
    bathroom_count: 1,
    ber: "C3",
    location: { county: "Dublin - All", county_area: "Dublin 2", address: "Apt 65, Trinity Square, Townsend Street, Dublin 2, D02 X981" },
    price: { min_value: "2800", symbol: "€" },
    rental_period: "Monthly",
    property_size: { value: "0", parameter: "m²" },
    images: [
      { url: "https://images.findqo.com/ad-images/8198_1771447081_8395.jpg", is_cover: true },
      { url: "https://images.findqo.com/ad-images/8198_1771447082_3731.jpg" },
    ],
    seller: { name: "Kevin Cassidy", is_verified: true },
    contact: { name: "Kevin Cassidy", email: "kevincassidy313@gmail.com", phone: "863995202" },
    ad_link: "#",
  },
  {
    id: 8134,
    title: "3 Bedroom Apartment for Rent in New Ross, Wexford",
    description: "Generous 3-bedroom apartment in a modern development. River views, allocated parking, and close to New Ross town and amenities. Suitable for professionals or families.",
    property_type: "apartment",
    bedroom_count: 3,
    bathroom_count: 2,
    ber: "C1",
    location: { county: "Wexford", county_area: "New Ross, Wexford", address: "2 Rosbercon Court, Lower Rosbercon, New Ross, Co. Wexford" },
    price: { min_value: "1400", symbol: "€" },
    rental_period: "Monthly",
    property_size: { value: "0", parameter: "m²" },
    images: [
      { url: "https://images.findqo.com/ad-images/8134_1771338812_5839.jpg", is_cover: true },
      { url: "https://images.findqo.com/ad-images/8134_1771338812_5423.jpg" },
    ],
    seller: { name: "Manor Properties", is_verified: true, tagline: "Real Estate Broker" },
    contact: { name: "Brian Kenneally", email: "brian@manorproperties.ie", phone: "879237573" },
    ad_link: "#",
  },
];

const COUNTIES = [
  "Antrim", "Carlow", "Cavan", "Clare", "Cork", "Donegal",
  "Dublin - All", "Dublin (County)", "Galway", "Kerry", "Kildare",
  "Kilkenny", "Laois", "Leitrim", "Limerick", "Longford",
  "Louth", "Mayo", "Meath", "Monaghan", "Offaly", "Roscommon",
  "Sligo", "Tipperary", "Waterford", "Westmeath", "Wexford", "Wicklow",
];

const PROPERTY_TYPES = [
  { value: "", label: "Any Type" },
  { value: "apartment", label: "Apartment" },
  { value: "house", label: "House" },
  { value: "terraced-house", label: "Terraced House" },
  { value: "semi-detached", label: "Semi-Detached" },
  { value: "detached", label: "Detached" },
  { value: "bungalow", label: "Bungalow" },
  { value: "studio", label: "Studio" },
  { value: "duplex", label: "Duplex" },
];

const PRICE_RANGES = [
  { value: "", label: "Any Price" },
  { value: "0-1000", label: "Up to €1,000" },
  { value: "1000-1500", label: "€1,000 – €1,500" },
  { value: "1500-2000", label: "€1,500 – €2,000" },
  { value: "2000-2500", label: "€2,000 – €2,500" },
  { value: "2500-3000", label: "€2,500 – €3,000" },
  { value: "3000-", label: "€3,000+" },
];

const BEDROOM_OPTIONS = [
  { value: "", label: "Any" },
  { value: "1", label: "1" },
  { value: "2", label: "2" },
  { value: "3", label: "3" },
  { value: "4", label: "4" },
  { value: "5", label: "5+" },
];

const BROWSE_LOCATIONS = [
  "Dublin", "Cork", "Galway", "Limerick", "Waterford",
  "Kilkenny", "Wexford", "Meath", "Kildare", "Wicklow",
  "Clare", "Tipperary", "Kerry", "Mayo", "Sligo",
];

// ─── BER Badge colours ────────────────────────────────────────────────────────
const BER_COLORS = {
  A1: "#007A3D", A2: "#007A3D", A3: "#007A3D",
  B1: "#5CAC2D", B2: "#5CAC2D", B3: "#5CAC2D",
  C1: "#F5A623", C2: "#F5A623", C3: "#F5A623",
  D1: "#E07B2A", D2: "#E07B2A",
  E1: "#D9531E", E2: "#D9531E",
  F: "#CC0000", G: "#990000",
};

// ─── ICONS (inline SVG) ───────────────────────────────────────────────────────
const Icon = {
  Bed: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8"/><path d="M4 10V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"/>
      <line x1="2" y1="16" x2="22" y2="16"/>
    </svg>
  ),
  Bath: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1-.5C4.683 3 4 3.683 4 4.5V17a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/>
      <line x1="10" y1="5" x2="8" y2="7"/><line x1="2" y1="12" x2="22" y2="12"/>
    </svg>
  ),
  Location: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>
    </svg>
  ),
  Search: () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
    </svg>
  ),
  Phone: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.77 1.2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 8.91a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
    </svg>
  ),
  Mail: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
    </svg>
  ),
  Size: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21 3H3v7h18V3z"/><path d="M21 14H3v7h18v-7z"/>
    </svg>
  ),
  Verified: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="#2563eb" stroke="none">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
    </svg>
  ),
  Close: () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  ),
  ChevronDown: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <polyline points="6 9 12 15 18 9"/>
    </svg>
  ),
  Home: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
  ),
};

// ─── NAVBAR ───────────────────────────────────────────────────────────────────
function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav style={{
      background: "#fff",
      borderBottom: "1px solid #e5e7eb",
      position: "sticky",
      top: 0,
      zIndex: 100,
      boxShadow: "0 1px 4px rgba(0,0,0,.06)",
    }}>
      <div style={{ maxWidth: 1280, margin: "0 auto", padding: "0 24px", display: "flex", alignItems: "center", height: 64 }}>
        {/* Logo */}
        <a href="/" style={{ display: "flex", alignItems: "center", gap: 8, textDecoration: "none", marginRight: 40 }}>
          <div style={{
            background: "#1a56db",
            color: "#fff",
            fontWeight: 800,
            fontSize: 20,
            padding: "4px 10px",
            borderRadius: 6,
            letterSpacing: "-0.5px",
            fontFamily: "'Georgia', serif",
          }}>PropertyListing</div>
          <span style={{ color: "#6b7280", fontSize: 12 }}>Ireland</span>
        </a>

        {/* Desktop Nav Links */}
        <div style={{ display: "flex", gap: 2, flex: 1 }} className="nav-links">
          {["Buy", "Rent", "Share", "Property Valuation"].map(item => (
            <a key={item} href="#" style={{
              padding: "8px 14px",
              color: item === "Rent" ? "#1a56db" : "#374151",
              fontWeight: item === "Rent" ? 600 : 400,
              fontSize: 14,
              textDecoration: "none",
              borderRadius: 6,
              borderBottom: item === "Rent" ? "2px solid #1a56db" : "2px solid transparent",
              transition: "color .15s",
            }}>{item}</a>
          ))}
        </div>

        {/* Right Actions */}
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <a href="#" style={{
            background: "#1a56db",
            color: "#fff",
            padding: "8px 16px",
            borderRadius: 6,
            fontSize: 13,
            fontWeight: 600,
            textDecoration: "none",
            whiteSpace: "nowrap",
          }}>+ Place Free Ad</a>
          <a href="#" style={{
            color: "#374151",
            padding: "8px 14px",
            fontSize: 13,
            fontWeight: 500,
            textDecoration: "none",
          }}>Login</a>
          <a href="#" style={{
            border: "1px solid #d1d5db",
            color: "#374151",
            padding: "7px 14px",
            borderRadius: 6,
            fontSize: 13,
            fontWeight: 500,
            textDecoration: "none",
          }}>Sign Up</a>
        </div>
      </div>
    </nav>
  );
}

// ─── FILTER BAR ───────────────────────────────────────────────────────────────
function FilterBar({ filters, onChange, onSearch }) {
  const [localSearch, setLocalSearch] = useState(filters.search || "");

  function handleKeyDown(e) {
    if (e.key === "Enter") onSearch(localSearch);
  }

  return (
    <div style={{
      background: "#1a3a5c",
      padding: "20px 24px",
    }}>
      <div style={{ maxWidth: 1280, margin: "0 auto" }}>
        {/* Search row */}
        <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
          <div style={{ flex: 1, position: "relative" }}>
            <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: "#9ca3af" }}>
              <Icon.Search />
            </span>
            <input
              value={localSearch}
              onChange={e => setLocalSearch(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Search by address, location, or keyword..."
              style={{
                width: "100%",
                padding: "11px 12px 11px 42px",
                border: "none",
                borderRadius: 8,
                fontSize: 14,
                outline: "none",
                boxSizing: "border-box",
                fontFamily: "inherit",
              }}
            />
          </div>
          <button
            onClick={() => onSearch(localSearch)}
            style={{
              background: "#f59e0b",
              color: "#fff",
              border: "none",
              padding: "11px 24px",
              borderRadius: 8,
              fontWeight: 700,
              fontSize: 14,
              cursor: "pointer",
              whiteSpace: "nowrap",
            }}
          >Search</button>
        </div>

        {/* Filter dropdowns */}
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <Select
            value={filters.county || ""}
            onChange={v => onChange("county", v)}
            options={[{ value: "", label: "All Counties" }, ...COUNTIES.map(c => ({ value: c, label: c }))]}
            placeholder="Location"
            dark
          />
          <Select
            value={filters.property_type || ""}
            onChange={v => onChange("property_type", v)}
            options={PROPERTY_TYPES}
            placeholder="Property Type"
            dark
          />
          <Select
            value={filters.price || ""}
            onChange={v => onChange("price", v)}
            options={PRICE_RANGES}
            placeholder="Price"
            dark
          />
          <Select
            value={filters.bedrooms || ""}
            onChange={v => onChange("bedrooms", v)}
            options={BEDROOM_OPTIONS.map(o => ({ ...o, label: o.value ? `${o.label} bed` : "Any Bedrooms" }))}
            placeholder="Bedrooms"
            dark
          />
          {Object.values(filters).some(v => v) && (
            <button
              onClick={() => onChange("__clear__", null)}
              style={{
                background: "rgba(255,255,255,.15)",
                color: "#fff",
                border: "1px solid rgba(255,255,255,.3)",
                padding: "9px 16px",
                borderRadius: 8,
                fontSize: 13,
                cursor: "pointer",
              }}
            >Clear All</button>
          )}
        </div>
      </div>
    </div>
  );
}

function Select({ value, onChange, options, placeholder, dark }) {
  return (
    <div style={{ position: "relative" }}>
      <select
        value={value}
        onChange={e => onChange(e.target.value)}
        style={{
          appearance: "none",
          background: dark ? "rgba(255,255,255,.1)" : "#fff",
          color: dark ? "#fff" : "#374151",
          border: dark ? "1px solid rgba(255,255,255,.2)" : "1px solid #d1d5db",
          padding: "9px 32px 9px 12px",
          borderRadius: 8,
          fontSize: 13,
          cursor: "pointer",
          fontFamily: "inherit",
          minWidth: 150,
          outline: "none",
        }}
      >
        {options.map(o => (
          <option key={o.value} value={o.value} style={{ color: "#374151", background: "#fff" }}>
            {o.label}
          </option>
        ))}
      </select>
      <span style={{
        position: "absolute",
        right: 10,
        top: "50%",
        transform: "translateY(-50%)",
        pointerEvents: "none",
        color: dark ? "#fff" : "#6b7280",
      }}>
        <Icon.ChevronDown />
      </span>
    </div>
  );
}

// ─── PROPERTY CARD ────────────────────────────────────────────────────────────
function PropertyCard({ property, onEnquiry }) {
  const [imgIdx, setImgIdx] = useState(0);
  const images = property.images || [];
  const coverImg = images.find(i => i.is_cover) || images[0];
  const displayImg = images[imgIdx] || coverImg;

  const price = property.price;
  const loc = property.location;
  const size = property.property_size;

  function formatPrice(p) {
    if (!p) return "";
    const val = parseInt(p.min_value, 10);
    return `${p.symbol}${val.toLocaleString("en-IE")}`;
  }

  return (
    <div style={{
      background: "#fff",
      border: "1px solid #e5e7eb",
      borderRadius: 12,
      overflow: "hidden",
      display: "flex",
      flexDirection: "column",
      transition: "box-shadow .2s, transform .2s",
      cursor: "pointer",
    }}
      onMouseEnter={e => {
        e.currentTarget.style.boxShadow = "0 8px 30px rgba(0,0,0,.12)";
        e.currentTarget.style.transform = "translateY(-2px)";
      }}
      onMouseLeave={e => {
        e.currentTarget.style.boxShadow = "none";
        e.currentTarget.style.transform = "none";
      }}
    >
      {/* Image */}
      <div style={{ position: "relative", height: 220, overflow: "hidden", background: "#f3f4f6" }}>
        {displayImg && (
          <img
            src={displayImg.url}
            alt={property.title}
            style={{ width: "100%", height: "100%", objectFit: "cover", transition: "transform .4s" }}
            onError={e => { e.target.src = "https://via.placeholder.com/400x220?text=No+Image"; }}
          />
        )}
        {/* BER badge */}
        {property.ber && (
          <div style={{
            position: "absolute",
            top: 12,
            left: 12,
            background: BER_COLORS[property.ber] || "#6b7280",
            color: "#fff",
            padding: "3px 8px",
            borderRadius: 4,
            fontSize: 11,
            fontWeight: 700,
            letterSpacing: "0.5px",
          }}>BER {property.ber}</div>
        )}
        {/* Image counter */}
        {images.length > 1 && (
          <div style={{
            position: "absolute",
            bottom: 10,
            right: 10,
            background: "rgba(0,0,0,.55)",
            color: "#fff",
            fontSize: 11,
            padding: "3px 8px",
            borderRadius: 12,
          }}>
            {imgIdx + 1} / {images.length}
          </div>
        )}
        {/* Image nav */}
        {images.length > 1 && (
          <div style={{ position: "absolute", bottom: 8, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 4 }}>
            {images.slice(0, 5).map((_, i) => (
              <button
                key={i}
                onClick={e => { e.stopPropagation(); setImgIdx(i); }}
                style={{
                  width: 6, height: 6,
                  borderRadius: "50%",
                  background: i === imgIdx ? "#fff" : "rgba(255,255,255,.5)",
                  border: "none",
                  padding: 0,
                  cursor: "pointer",
                }}
              />
            ))}
          </div>
        )}
        {/* Price overlay */}
        <div style={{
          position: "absolute",
          top: 12,
          right: 12,
          background: "#1a56db",
          color: "#fff",
          padding: "5px 12px",
          borderRadius: 6,
          fontWeight: 700,
          fontSize: 15,
        }}>
          {formatPrice(price)}
          <span style={{ fontSize: 11, fontWeight: 400, opacity: 0.85 }}>/{property.rental_period === "Monthly" ? "mo" : "wk"}</span>
        </div>
      </div>

      {/* Body */}
      <div style={{ padding: "16px 16px 0" }}>
        <h3 style={{
          margin: "0 0 8px",
          fontSize: 15,
          fontWeight: 600,
          color: "#111827",
          lineHeight: 1.4,
          display: "-webkit-box",
          WebkitLineClamp: 2,
          WebkitBoxOrient: "vertical",
          overflow: "hidden",
        }}>{property.title}</h3>

        <div style={{ display: "flex", alignItems: "center", gap: 4, color: "#6b7280", fontSize: 12, marginBottom: 10 }}>
          <Icon.Location />
          <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {loc?.address || loc?.county_area}
          </span>
        </div>

        <p style={{
          margin: "0 0 12px",
          fontSize: 13,
          color: "#6b7280",
          lineHeight: 1.5,
          display: "-webkit-box",
          WebkitLineClamp: 2,
          WebkitBoxOrient: "vertical",
          overflow: "hidden",
        }}>{property.description}</p>

        {/* Specs row */}
        <div style={{ display: "flex", gap: 16, padding: "10px 0", borderTop: "1px solid #f3f4f6", borderBottom: "1px solid #f3f4f6", marginBottom: 12 }}>
          <Spec icon={<Icon.Bed />} label={`${property.bedroom_count} Bed`} />
          <Spec icon={<Icon.Bath />} label={`${property.bathroom_count} Bath`} />
          {size?.value && parseInt(size.value) > 0 && (
            <Spec icon={<Icon.Size />} label={`${size.value} ${size.parameter}`} />
          )}
        </div>

        {/* Seller */}
        <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 4 }}>
          <div style={{
            width: 28, height: 28, borderRadius: "50%",
            background: "#dbeafe",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 11, fontWeight: 700, color: "#1a56db",
            flexShrink: 0,
          }}>
            {property.seller?.name?.[0] || "?"}
          </div>
          <div style={{ minWidth: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
              <span style={{ fontSize: 12, fontWeight: 500, color: "#374151", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", maxWidth: 150 }}>
                {property.seller?.name}
              </span>
              {property.seller?.is_verified && <Icon.Verified />}
            </div>
            {property.seller?.tagline && (
              <span style={{ fontSize: 11, color: "#9ca3af" }}>{property.seller.tagline}</span>
            )}
          </div>
        </div>
      </div>

      {/* Actions */}
      <div style={{ display: "flex", gap: 8, padding: 12, marginTop: "auto" }}>
        <a
          href={`tel:${property.contact?.phone}`}
          onClick={e => e.stopPropagation()}
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 5,
            flex: 1,
            padding: "9px 12px",
            border: "1px solid #d1d5db",
            borderRadius: 7,
            color: "#374151",
            fontSize: 12,
            fontWeight: 500,
            textDecoration: "none",
            transition: "background .15s",
          }}
          onMouseEnter={e => e.currentTarget.style.background = "#f9fafb"}
          onMouseLeave={e => e.currentTarget.style.background = "transparent"}
        >
          <Icon.Phone /> Call
        </a>
        <button
          onClick={e => { e.stopPropagation(); onEnquiry(property); }}
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 5,
            flex: 2,
            padding: "9px 12px",
            background: "#1a56db",
            border: "none",
            borderRadius: 7,
            color: "#fff",
            fontSize: 12,
            fontWeight: 600,
            cursor: "pointer",
            transition: "background .15s",
          }}
          onMouseEnter={e => e.currentTarget.style.background = "#1e429f"}
          onMouseLeave={e => e.currentTarget.style.background = "#1a56db"}
        >
          <Icon.Mail /> Send Enquiry
        </button>
      </div>
    </div>
  );
}

function Spec({ icon, label }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 4, color: "#6b7280", fontSize: 12 }}>
      {icon}{label}
    </div>
  );
}

// ─── ENQUIRY MODAL ─────────────────────────────────────────────────────────────
function EnquiryModal({ property, onClose }) {
  const [form, setForm] = useState({ name: "", email: "", phone: "", message: "" });
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setSending(true);
    setTimeout(() => { setSending(false); setSent(true); }, 1200);
  }

  if (!property) return null;

  return (
    <div style={{
      position: "fixed", inset: 0,
      background: "rgba(0,0,0,.5)",
      display: "flex", alignItems: "center", justifyContent: "center",
      zIndex: 200,
      padding: 16,
    }} onClick={onClose}>
      <div style={{
        background: "#fff",
        borderRadius: 16,
        width: "100%",
        maxWidth: 500,
        overflow: "hidden",
        boxShadow: "0 25px 50px rgba(0,0,0,.25)",
      }} onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div style={{ padding: "20px 24px", borderBottom: "1px solid #e5e7eb", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <h3 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: "#111827" }}>Send Enquiry</h3>
            <p style={{ margin: "2px 0 0", fontSize: 13, color: "#6b7280" }}>{property.title}</p>
          </div>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", color: "#6b7280", padding: 4 }}>
            <Icon.Close />
          </button>
        </div>

        {sent ? (
          <div style={{ padding: 40, textAlign: "center" }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>✅</div>
            <h4 style={{ margin: "0 0 8px", color: "#111827" }}>Enquiry Sent!</h4>
            <p style={{ color: "#6b7280", margin: "0 0 20px" }}>
              {property.contact?.name} will be in touch shortly at {form.email}.
            </p>
            <button onClick={onClose} style={{
              background: "#1a56db", color: "#fff", border: "none",
              padding: "10px 24px", borderRadius: 8, fontWeight: 600, cursor: "pointer",
            }}>Close</button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ padding: 24 }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 12 }}>
              <Field label="Name *" value={form.name} onChange={v => setForm(f => ({ ...f, name: v }))} required />
              <Field label="Email *" type="email" value={form.email} onChange={v => setForm(f => ({ ...f, email: v }))} required />
            </div>
            <Field label="Phone" type="tel" value={form.phone} onChange={v => setForm(f => ({ ...f, phone: v }))} style={{ marginBottom: 12 }} />
            <div style={{ marginBottom: 20 }}>
              <label style={{ display: "block", fontSize: 12, fontWeight: 500, color: "#374151", marginBottom: 4 }}>Message</label>
              <textarea
                rows={4}
                value={form.message}
                onChange={e => setForm(f => ({ ...f, message: e.target.value }))}
                placeholder="I'm interested in this property and would like more information..."
                style={{
                  width: "100%", padding: "9px 12px",
                  border: "1px solid #d1d5db", borderRadius: 8,
                  fontSize: 13, fontFamily: "inherit", resize: "vertical",
                  outline: "none", boxSizing: "border-box",
                }}
              />
            </div>
            <button type="submit" disabled={sending} style={{
              width: "100%",
              background: sending ? "#93c5fd" : "#1a56db",
              color: "#fff",
              border: "none",
              padding: "12px",
              borderRadius: 8,
              fontWeight: 700,
              fontSize: 15,
              cursor: sending ? "not-allowed" : "pointer",
            }}>
              {sending ? "Sending..." : "Send Enquiry"}
            </button>
            <p style={{ fontSize: 11, color: "#9ca3af", textAlign: "center", marginTop: 12, marginBottom: 0 }}>
              Contact: {property.contact?.name} — {property.contact?.email}
            </p>
          </form>
        )}
      </div>
    </div>
  );
}

function Field({ label, type = "text", value, onChange, required, style = {} }) {
  return (
    <div style={{ marginBottom: 0, ...style }}>
      <label style={{ display: "block", fontSize: 12, fontWeight: 500, color: "#374151", marginBottom: 4 }}>{label}</label>
      <input
        type={type}
        value={value}
        onChange={e => onChange(e.target.value)}
        required={required}
        style={{
          width: "100%", padding: "9px 12px",
          border: "1px solid #d1d5db", borderRadius: 8,
          fontSize: 13, fontFamily: "inherit",
          outline: "none", boxSizing: "border-box",
        }}
      />
    </div>
  );
}

// ─── PAGINATION ───────────────────────────────────────────────────────────────
function Pagination({ currentPage, totalPages, onChange }) {
  if (totalPages <= 1) return null;

  const pages = [];
  const maxVisible = 7;
  let start = Math.max(1, currentPage - 3);
  let end = Math.min(totalPages, start + maxVisible - 1);
  if (end - start < maxVisible - 1) start = Math.max(1, end - maxVisible + 1);

  for (let i = start; i <= end; i++) pages.push(i);

  const btnStyle = (active) => ({
    width: 36, height: 36,
    display: "flex", alignItems: "center", justifyContent: "center",
    border: active ? "none" : "1px solid #d1d5db",
    borderRadius: 8,
    background: active ? "#1a56db" : "#fff",
    color: active ? "#fff" : "#374151",
    fontWeight: active ? 700 : 400,
    fontSize: 13,
    cursor: "pointer",
    transition: "all .15s",
  });

  return (
    <div style={{ display: "flex", justifyContent: "center", gap: 6, margin: "32px 0" }}>
      <button onClick={() => onChange(currentPage - 1)} disabled={currentPage === 1}
        style={{ ...btnStyle(false), opacity: currentPage === 1 ? 0.4 : 1 }}>‹</button>
      {start > 1 && <><button onClick={() => onChange(1)} style={btnStyle(false)}>1</button><span style={{ display: "flex", alignItems: "center", color: "#9ca3af" }}>…</span></>}
      {pages.map(p => (
        <button key={p} onClick={() => onChange(p)} style={btnStyle(p === currentPage)}>{p}</button>
      ))}
      {end < totalPages && <><span style={{ display: "flex", alignItems: "center", color: "#9ca3af" }}>…</span><button onClick={() => onChange(totalPages)} style={btnStyle(false)}>{totalPages}</button></>}
      <button onClick={() => onChange(currentPage + 1)} disabled={currentPage === totalPages}
        style={{ ...btnStyle(false), opacity: currentPage === totalPages ? 0.4 : 1 }}>›</button>
    </div>
  );
}

// ─── ADVERT BANNER ────────────────────────────────────────────────────────────
function AdvertBanner({ type = 1 }) {
  const ads = [
    {
      bg: "linear-gradient(135deg, #f59e0b, #d97706)",
      text: "Get a free property valuation",
      sub: "Expert valuers across Ireland",
      cta: "Book Now",
    },
    {
      bg: "linear-gradient(135deg, #10b981, #059669)",
      text: "Looking to list your property?",
      sub: "Place a free ad on PropertyListing today",
      cta: "List for Free",
    },
  ];
  const ad = ads[(type - 1) % ads.length];

  return (
    <div style={{
      background: ad.bg,
      borderRadius: 12,
      padding: "20px 24px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      margin: "24px 0",
      flexWrap: "wrap",
      gap: 12,
    }}>
      <div>
        <div style={{ color: "#fff", fontWeight: 700, fontSize: 16 }}>{ad.text}</div>
        <div style={{ color: "rgba(255,255,255,.85)", fontSize: 13 }}>{ad.sub}</div>
      </div>
      <button style={{
        background: "#fff",
        color: "#111827",
        border: "none",
        padding: "10px 20px",
        borderRadius: 8,
        fontWeight: 700,
        fontSize: 13,
        cursor: "pointer",
        whiteSpace: "nowrap",
      }}>{ad.cta}</button>
    </div>
  );
}

// ─── BROWSE BY LOCATION ───────────────────────────────────────────────────────
function BrowseByLocation() {
  const [mode, setMode] = useState("rent");

  return (
    <div style={{ background: "#f9fafb", borderRadius: 16, padding: "32px 24px", margin: "32px 0" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20, flexWrap: "wrap", gap: 12 }}>
        <h2 style={{ margin: 0, fontSize: 20, fontWeight: 700, color: "#111827" }}>
          Browse Properties by Location
        </h2>
        <div style={{ display: "flex", gap: 4, background: "#e5e7eb", borderRadius: 8, padding: 3 }}>
          {["sale", "rent", "share"].map(m => (
            <button key={m} onClick={() => setMode(m)} style={{
              padding: "6px 14px",
              borderRadius: 6,
              border: "none",
              background: mode === m ? "#fff" : "transparent",
              color: mode === m ? "#1a56db" : "#6b7280",
              fontWeight: mode === m ? 600 : 400,
              fontSize: 13,
              cursor: "pointer",
              textTransform: "capitalize",
              boxShadow: mode === m ? "0 1px 4px rgba(0,0,0,.1)" : "none",
            }}>
              {m.charAt(0).toUpperCase() + m.slice(1)}
            </button>
          ))}
        </div>
      </div>
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))",
        gap: 8,
      }}>
        {BROWSE_LOCATIONS.map(loc => (
          <a key={loc} href="#" style={{
            display: "flex",
            alignItems: "center",
            gap: 6,
            padding: "10px 12px",
            background: "#fff",
            border: "1px solid #e5e7eb",
            borderRadius: 8,
            textDecoration: "none",
            color: "#374151",
            fontSize: 13,
            fontWeight: 500,
            transition: "all .15s",
          }}
            onMouseEnter={e => {
              e.currentTarget.style.borderColor = "#1a56db";
              e.currentTarget.style.color = "#1a56db";
            }}
            onMouseLeave={e => {
              e.currentTarget.style.borderColor = "#e5e7eb";
              e.currentTarget.style.color = "#374151";
            }}
          >
            <Icon.Home />
            {loc}
          </a>
        ))}
      </div>
    </div>
  );
}

// ─── SIMILAR PROPERTIES ───────────────────────────────────────────────────────
function SimilarProperties({ properties, onEnquiry }) {
  if (!properties.length) return null;
  return (
    <div style={{ margin: "32px 0" }}>
      <h2 style={{ fontSize: 20, fontWeight: 700, color: "#111827", marginBottom: 20 }}>
        Similar Properties
      </h2>
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
        gap: 20,
      }}>
        {properties.slice(0, 3).map(p => (
          <PropertyCard key={p.id} property={p} onEnquiry={onEnquiry} />
        ))}
      </div>
    </div>
  );
}

// ─── FOOTER ───────────────────────────────────────────────────────────────────
function Footer() {
  const cols = [
    {
      title: "For Buyers & Renters",
      links: ["Properties for Rent", "Properties for Sale", "Shared Accommodation", "New Homes", "Commercial Properties"],
    },
    {
      title: "For Sellers & Landlords",
      links: ["Place Free Ad", "Premium Listings", "Property Valuation", "Advertise With Us", "Agent Login"],
    },
    {
      title: "Company",
      links: ["About PropertyListing", "Contact Us", "Press", "Careers", "Blog"],
    },
    {
      title: "Legal",
      links: ["Privacy Policy", "Terms of Use", "Cookie Policy", "GDPR", "Disclaimer"],
    },
  ];

  return (
    <footer style={{ background: "#1a3a5c", color: "#fff", marginTop: 40 }}>
      <div style={{ maxWidth: 1280, margin: "0 auto", padding: "48px 24px 24px" }}>
        {/* Logo & description */}
        <div style={{ marginBottom: 40 }}>
          <div style={{
            display: "inline-block",
            background: "rgba(255,255,255,.15)",
            color: "#fff",
            fontWeight: 800,
            fontSize: 24,
            padding: "4px 12px",
            borderRadius: 6,
            letterSpacing: "-0.5px",
            fontFamily: "'Georgia', serif",
            marginBottom: 12,
          }}>PrpertyListing</div>
          <p style={{ color: "rgba(255,255,255,.7)", fontSize: 14, maxWidth: 400, margin: 0 }}>
            Ireland's leading property portal. Search thousands of properties for rent, sale, and sharing across every county.
          </p>
        </div>

        {/* Columns */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 32, marginBottom: 40 }}>
          {cols.map(col => (
            <div key={col.title}>
              <h4 style={{ color: "#fff", fontWeight: 600, fontSize: 13, marginBottom: 12, textTransform: "uppercase", letterSpacing: "0.5px" }}>
                {col.title}
              </h4>
              {col.links.map(link => (
                <a key={link} href="#" style={{
                  display: "block",
                  color: "rgba(255,255,255,.65)",
                  fontSize: 13,
                  textDecoration: "none",
                  marginBottom: 6,
                  transition: "color .15s",
                }}
                  onMouseEnter={e => e.currentTarget.style.color = "#fff"}
                  onMouseLeave={e => e.currentTarget.style.color = "rgba(255,255,255,.65)"}
                >{link}</a>
              ))}
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div style={{ borderTop: "1px solid rgba(255,255,255,.15)", paddingTop: 20, display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }}>
          <p style={{ margin: 0, color: "rgba(255,255,255,.5)", fontSize: 12 }}>
            © {new Date().getFullYear()} PropertyListing.ie — All rights reserved.
          </p>
          <div style={{ display: "flex", gap: 16 }}>
            {["Privacy", "Terms", "Cookies"].map(l => (
              <a key={l} href="#" style={{ color: "rgba(255,255,255,.5)", fontSize: 12, textDecoration: "none" }}>{l}</a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}

// ─── BREADCRUMBS ──────────────────────────────────────────────────────────────
function Breadcrumbs({ total, filters }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6, color: "#6b7280", fontSize: 13, marginBottom: 20 }}>
      <a href="/" style={{ color: "#1a56db", textDecoration: "none" }}>Home</a>
      <span>›</span>
      <a href="/rent" style={{ color: "#1a56db", textDecoration: "none" }}>Properties for Rent</a>
      {filters.county && <><span>›</span><span style={{ color: "#374151" }}>{filters.county}</span></>}
      <span style={{ marginLeft: "auto", color: "#374151", fontWeight: 500 }}>
        {total} {total === 1 ? "Property" : "Properties"} found
      </span>
    </div>
  );
}

// ─── MAIN APP ─────────────────────────────────────────────────────────────────
export default function App() {
  const [properties, setProperties] = useState(DEMO_PROPERTIES);
  const [total, setTotal] = useState(DEMO_PROPERTIES.length);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [enquiryProp, setEnquiryProp] = useState(null);
  const [filters, setFilters] = useState({
    county: "",
    property_type: "",
    price: "",
    bedrooms: "",
    search: "",
  });

  // Derive similar from same county
  const similar = properties.length > 1 ? properties.slice(3, 6) : [];

  const loadProperties = useCallback(async (newFilters, page = 1) => {
    setLoading(true);
    try {
      const params = { page };
      if (newFilters.county) params.county = newFilters.county.toLowerCase().replace(/\s+/g, "-").replace(/[()]/g, "");
      if (newFilters.property_type) params.property_type = newFilters.property_type;
      if (newFilters.bedrooms) params.bedrooms = newFilters.bedrooms;
      if (newFilters.search) params.search = newFilters.search;
      if (newFilters.price) {
        const [min, max] = newFilters.price.split("-");
        if (min) params.price_min = min;
        if (max) params.price_max = max;
      }

      const data = await fetchProperties(params);
      if (data.results) {
        setProperties(data.results);
        setTotal(data.meta?.total || data.count || data.results.length);
        setTotalPages(data.meta?.total_pages || Math.ceil((data.count || data.results.length) / 6));
      } else if (data.data) {
        setProperties(data.data);
        setTotal(parseInt(data.meta?.total || data.data.length));
        setTotalPages(parseInt(data.meta?.total_pages || 1));
      }
    } catch {
      // API not available – keep demo data
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadProperties(filters, 1);
  }, []);

  function handleFilterChange(key, value) {
    if (key === "__clear__") {
      const cleared = { county: "", property_type: "", price: "", bedrooms: "", search: "" };
      setFilters(cleared);
      setCurrentPage(1);
      loadProperties(cleared, 1);
      return;
    }
    const updated = { ...filters, [key]: value };
    setFilters(updated);
    setCurrentPage(1);
    loadProperties(updated, 1);
  }

  function handleSearch(searchText) {
    handleFilterChange("search", searchText);
  }

  function handlePageChange(page) {
    setCurrentPage(page);
    loadProperties(filters, page);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // Filter demo data client-side for preview
  const displayedProperties = loading ? [] : (
    properties === DEMO_PROPERTIES
      ? DEMO_PROPERTIES.filter(p => {
          if (filters.county && !p.location?.county?.toLowerCase().includes(filters.county.toLowerCase()) &&
              !p.location?.county_area?.toLowerCase().includes(filters.county.toLowerCase())) return false;
          if (filters.property_type && p.property_type !== filters.property_type) return false;
          if (filters.bedrooms && parseInt(p.bedroom_count) !== parseInt(filters.bedrooms)) return false;
          if (filters.search) {
            const s = filters.search.toLowerCase();
            if (!p.title.toLowerCase().includes(s) && !p.location?.address?.toLowerCase().includes(s)) return false;
          }
          if (filters.price) {
            const [min, max] = filters.price.split("-");
            const val = parseInt(p.price?.min_value);
            if (min && val < parseInt(min)) return false;
            if (max && val > parseInt(max)) return false;
          }
          return true;
        })
      : properties
  );

  return (
    <div style={{ minHeight: "100vh", background: "#f9fafb", fontFamily: "'Inter', -apple-system, sans-serif" }}>
      <style>{`
        * { box-sizing: border-box; }
        body { margin: 0; }
        @media (max-width: 640px) {
          .nav-links { display: none !important; }
        }
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>

      <Navbar />
      <FilterBar filters={filters} onChange={handleFilterChange} onSearch={handleSearch} />

      <main style={{ maxWidth: 1280, margin: "0 auto", padding: "32px 24px" }}>
        <Breadcrumbs total={displayedProperties.length} filters={filters} />

        {/* Property Grid */}
        {loading ? (
          <div style={{ textAlign: "center", padding: 60 }}>
            <div style={{
              width: 40, height: 40, border: "3px solid #e5e7eb",
              borderTopColor: "#1a56db", borderRadius: "50%",
              animation: "spin 0.7s linear infinite",
              margin: "0 auto 16px",
            }} />
            <p style={{ color: "#6b7280" }}>Loading properties...</p>
          </div>
        ) : displayedProperties.length === 0 ? (
          <div style={{ textAlign: "center", padding: "60px 20px" }}>
            <div style={{ fontSize: 56, marginBottom: 16 }}>🏠</div>
            <h3 style={{ color: "#111827", marginBottom: 8 }}>No properties found</h3>
            <p style={{ color: "#6b7280", marginBottom: 20 }}>Try adjusting your filters or search term.</p>
            <button onClick={() => handleFilterChange("__clear__", null)} style={{
              background: "#1a56db", color: "#fff", border: "none",
              padding: "10px 20px", borderRadius: 8, fontWeight: 600, cursor: "pointer",
            }}>Clear filters</button>
          </div>
        ) : (
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
            gap: 24,
          }}>
            {displayedProperties.map((p, i) => (
              <>
                <PropertyCard key={p.id} property={p} onEnquiry={setEnquiryProp} />
                {/* Insert first ad after 3rd card */}
                {i === 2 && <div style={{ gridColumn: "1 / -1" }}><AdvertBanner type={1} /></div>}
              </>
            ))}
          </div>
        )}

        <Pagination currentPage={currentPage} totalPages={Math.max(totalPages, Math.ceil(displayedProperties.length / 6))} onChange={handlePageChange} />

        <AdvertBanner type={2} />
        <SimilarProperties properties={similar} onEnquiry={setEnquiryProp} />
        <BrowseByLocation />
      </main>

      <Footer />

      {enquiryProp && (
        <EnquiryModal property={enquiryProp} onClose={() => setEnquiryProp(null)} />
      )}
    </div>
  );
}
