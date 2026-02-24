# 🏠 FindQo Property Listing App

A full-stack property listing platform modelled on [findqo.ie](https://findqo.ie/properties-for-rent/antrim), built with **Django REST Framework** (backend) + **React/Vite** (frontend) + **MySQL**.

---

## 📁 Project Structure

```
property-app/
├── backend/                   # Django app
│   ├── models.py              # ORM models
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # API views
│   ├── urls.py                # API routes
│   ├── admin.py               # Django admin config
│   ├── settings.py            # Django settings
│   ├── requirements.txt       # Python dependencies
│   └── management/
│       └── commands/
│           └── seed_data.py   # Sample data seeder
│
├── frontend/                  # React/Vite app
    ├── src/
    │   ├── App.jsx            # Main app component (all sections)
    │   └── main.jsx           # React entry point
    ├── index.html
    ├── package.json
    └── vite.config.js


```

---

## 🗄️ Database Schema

### Key Tables

| Table | Description |
|-------|-------------|
| `sections` | Top-level categories (FOR RENT, FOR SALE, SHARE) |
| `aisles` | Sub-categories (Rent Residential, Rent Commercial, etc.) |
| `counties` | Irish counties |
| `county_areas` | Areas/towns within each county |
| `sellers` | Both private landlords and estate agents |
| `properties` | Core listing data |
| `property_images` | Multiple images per property (cover flagged) |
| `enquiries` | Contact form submissions |

### Key Design Decisions
- **BER stored as text**: flexible for future ratings, validated at app level
- **`price_min_value`** as `NUMERIC(12,2)` supports both rent (monthly) and sale prices
- **`rental_period`** supports Monthly/Weekly/Daily
- **Full-text search index** via PostgreSQL `GIN` on `title || description || address`
- **`v_property_listing` view** pre-joins cover image + county + seller for fast listing queries

---

## 🚀 Setup Instructions

### Backend (Django)

```bash
# 1. Create virtualenv
python -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Configure database in settings.py (MySQL )

# 4. Run migrations
python manage.py makemigrations properties
python manage.py migrate

# 5. Seed sample data (from the JSON API format)
python manage.py seed_data

# 6. Start server
python manage.py runserver
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev    # http://localhost:3000
```

