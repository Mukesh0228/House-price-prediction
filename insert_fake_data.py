"""
Script to insert fake data into the Real Estate platform database
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add project path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.models import db, User, Property
from werkzeug.security import generate_password_hash

# Create app context
app = create_app()

# Fake data
FAKE_LOCATIONS = [
    "Whitefield", "Koramangala", "Indiranagar", "Vijayanagar", 
    "Yeshwanthpur", "Hebbal", "Malleswaram", "Jayanagar",
    "Electronic City", "Bannerghatta Road", "HSR Layout", "Bellandur"
]

FAKE_PROPERTY_TYPES = ["apartment", "house", "villa"]

FAKE_DESCRIPTIONS = [
    "Beautiful 2BHK apartment with modern amenities and great views",
    "Spacious villa with garden and swimming pool",
    "Cozy 3BHK house in a gated community",
    "Luxury penthouse with premium finishes",
    "Modern apartment close to metro station",
    "Well-maintained villa with parking",
    "Affordable house in family-friendly area",
    "Corner plot villa with maximum natural light",
]

FAKE_USERS = [
    {"username": "john_smith", "email": "arjun@example.com", "password": "password123", "is_admin": False},
    {"username": "sarah_jones", "email": "sarah@example.com", "password": "password456", "is_admin": False},
    {"username": "mike_wilson", "email": "mike@example.com", "password": "password789", "is_admin": False},
    {"username": "emma_brown", "email": "emma@example.com", "password": "password101", "is_admin": False},
]

FAKE_ADMIN_USERS = [
    {"username": "admin", "email": "admin@example.com", "password": "admin123"},
    {"username": "admin_property_manager", "email": "manager@smartestate.com", "password": "SecurePass@123"},
    {"username": "admin_support", "email": "support@smartestate.com", "password": "SupportPass@456"},
    {"username": "admin_analytics", "email": "analytics@smartestate.com", "password": "AnalyticsPass@789"},
    {"username": "admin_operations", "email": "operations@smartestate.com", "password": "OpsPass@2024"},
]

FAKE_PROPERTIES = [
    {
        "title": "Modern 2BHK in Whitefield",
        "location": "Whitefield",
        "price": 75_00_000,
        "area_sqft": 1100,
        "bhk": 2,
        "bathrooms": 2,
        "type": "apartment",
        "image_filename": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200&h=800&fit=crop"
    },
    {
        "title": "Luxury Villa in Koramangala",
        "location": "Koramangala",
        "price": 3_50_00_000,
        "area_sqft": 3500,
        "bhk": 4,
        "bathrooms": 4,
        "type": "villa",
        "image_filename": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=1200&h=800&fit=crop"
    },
    {
        "title": "Spacious 3BHK House",
        "location": "Indiranagar",
        "price": 1_20_00_000,
        "area_sqft": 2000,
        "bhk": 3,
        "bathrooms": 2,
        "type": "house",
        "image_filename": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1200&h=800&fit=crop"
    },
    {
        "title": "Affordable 1BHK Apartment",
        "location": "Yeshwanthpur",
        "price": 45_00_000,
        "area_sqft": 650,
        "bhk": 1,
        "bathrooms": 1,
        "type": "apartment",
        "image_filename": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200&h=800&fit=crop"
    },
    {
        "title": "Premium Villa with Garden",
        "location": "Hebbal",
        "price": 2_80_00_000,
        "area_sqft": 3000,
        "bhk": 4,
        "bathrooms": 3,
        "type": "villa",
        "image_filename": "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=1200&h=800&fit=crop"
    },
    {
        "title": "Cozy 2BHK in Malleswaram",
        "location": "Malleswaram",
        "price": 68_00_000,
        "area_sqft": 950,
        "bhk": 2,
        "bathrooms": 1,
        "type": "apartment",
        "image_filename": "https://images.unsplash.com/photo-1560185127-6c548aaafba2?w=1200&h=800&fit=crop"
    },
    {
        "title": "Modern House in Jayanagar",
        "location": "Jayanagar",
        "price": 95_00_000,
        "area_sqft": 1600,
        "bhk": 3,
        "bathrooms": 2,
        "type": "house",
        "image_filename": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=1200&h=800&fit=crop"
    },
    {
        "title": "Tech Park Adjacent Apartment",
        "location": "Electronic City",
        "price": 55_00_000,
        "area_sqft": 820,
        "bhk": 2,
        "bathrooms": 1,
        "type": "apartment",
        "image_filename": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=1200&h=800&fit=crop"
    },
    {
        "title": "Villa near IT Hub",
        "location": "Bannerghatta Road",
        "price": 2_50_00_000,
        "area_sqft": 2800,
        "bhk": 3,
        "bathrooms": 3,
        "type": "villa",
        "image_filename": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200&h=800&fit=crop"
    },
    {
        "title": "Apartment in HSR Layout",
        "location": "HSR Layout",
        "price": 82_00_000,
        "area_sqft": 1200,
        "bhk": 2,
        "bathrooms": 2,
        "type": "apartment",
        "image_filename": "https://th.bing.com/th/id/OIP.sgB4AENidDHmGnrkSPtcyQHaFj?w=261&h=196&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3"
    },
    {
        "title": "Premium House in Bellandur",
        "location": "Bellandur",
        "price": 1_50_00_000,
        "area_sqft": 2200,
        "bhk": 3,
        "bathrooms": 2,
        "type": "house",
        "image_filename": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=1200&h=800&fit=crop"
    },
    {
        "title": "Luxury Penthouse",
        "location": "Koramangala",
        "price": 3_00_00_000,
        "area_sqft": 3200,
        "bhk": 4,
        "bathrooms": 4,
        "type": "apartment",
        "image_filename": "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=1200&h=800&fit=crop"
    },
]

def insert_fake_data():
    """Insert fake data into the database"""
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Property.query.delete()
        User.query.delete()
        db.session.commit()

        # Insert users
        print("Creating users...")
        users = []
        for user_data in FAKE_USERS:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=generate_password_hash(user_data["password"]),
                is_admin=user_data.get("is_admin", False)
            )
            users.append(user)
            db.session.add(user)

        # Create admin users
        print("Creating admin users...")
        admin_users = []
        for admin_data in FAKE_ADMIN_USERS:
            admin = User(
                username=admin_data["username"],
                email=admin_data["email"],
                password_hash=generate_password_hash(admin_data["password"]),
                is_admin=True
            )
            admin_users.append(admin)
            users.append(admin)
            db.session.add(admin)
        
        db.session.commit()
        print(f"✓ Created {len(users)} total users ({len(admin_users)} admins, {len(FAKE_USERS)} regular)")

        # Insert properties
        print("Creating properties...")
        now = datetime.utcnow()
        properties = []
        
        for i, prop_data in enumerate(FAKE_PROPERTIES):
            # Distribute properties among users
            user = users[i % len(users)]
            
            property_obj = Property(
                title=prop_data["title"],
                description=random.choice(FAKE_DESCRIPTIONS),
                price=prop_data["price"],
                location=prop_data["location"],
                area_sqft=prop_data["area_sqft"],
                bhk=prop_data["bhk"],
                bathrooms=prop_data["bathrooms"],
                property_type=prop_data["type"],
                image_filename=prop_data.get("image_filename"),
                user_id=user.id,
                created_at=now - timedelta(days=random.randint(1, 30))
            )
            properties.append(property_obj)
            db.session.add(property_obj)

        db.session.commit()
        print(f"✓ Created {len(properties)} properties")

        # Print summary
        print("\n" + "="*50)
        print("FAKE DATA INSERTION COMPLETE!")
        print("="*50)
        print(f"\nUsers Created:")
        for user in users:
            print(f"  • {user.username} ({user.email}) {'[ADMIN]' if user.is_admin else ''}")
        
        print(f"\nLocations Covered: {set(prop.location for prop in properties)}")
        print(f"\nPrice Range: ₹{min(p.price for p in properties):,.0f} - ₹{max(p.price for p in properties):,.0f}")
        print(f"Average Price: ₹{sum(p.price for p in properties) / len(properties):,.0f}")
        
        by_type = {}
        for prop in properties:
            by_type[prop.property_type] = by_type.get(prop.property_type, 0) + 1
        print(f"\nProperties by Type:")
        for ptype, count in by_type.items():
            print(f"  • {ptype.capitalize()}: {count}")

        print("\n" + "="*50)
        print("Default Credentials:")
        print("="*50)
        print("Admin Login:")
        print("  Email: admin@example.com")
        print("  Password: admin123")
        print("\nTest User Logins:")
        for user in users[:2]:
            print(f"  Email: {user.email}")
            print(f"  Password: password123/456/789/101 (varies)")

if __name__ == '__main__':
    try:
        insert_fake_data()
        print("\n✅ Database populated successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
