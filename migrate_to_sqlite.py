
import os
from app import create_app, db
from models import *

def migrate_to_sqlite():
    """Migrate database to SQLite3"""
    app = create_app()
    
    with app.app_context():
        # Remove existing database file if it exists
        if os.path.exists('barterhub.db'):
            os.remove('barterhub.db')
            print("Removed existing SQLite database")
        
        # Create all tables
        db.create_all()
        print("Created all tables in SQLite database")
        
        # Create default categories
        if Category.query.count() == 0:
            categories = [
                Category(name='Elektronik', description='Perangkat elektronik dan gadget'),
                Category(name='Fashion', description='Pakaian, sepatu, dan aksesoris'),
                Category(name='Rumah Tangga', description='Peralatan dan perlengkapan rumah'),
                Category(name='Olahraga', description='Peralatan dan perlengkapan olahraga'),
                Category(name='Buku & Media', description='Buku, CD, DVD, dan media lainnya'),
                Category(name='Kendaraan', description='Motor, mobil, dan aksesoris kendaraan'),
                Category(name='Hobi & Koleksi', description='Barang hobi dan koleksi'),
                Category(name='Lainnya', description='Kategori lainnya')
            ]

            for category in categories:
                db.session.add(category)
            db.session.commit()
            print("Created default categories")

        # Create admin user
        admin = User.query.filter_by(username='fajarjulyana').first()
        if not admin:
            admin = User(
                username='fajarjulyana',
                email='fajarjulyana@barterhub.com',
                full_name='Fajar Julyana',
                role='admin'
            )
            admin.set_password('fajar123')
            db.session.add(admin)
            db.session.commit()
            print("Created admin user")
        else:
            print("Admin user already exists")

        print("✅ Migration to SQLite3 completed successfully!")
        print("Database file: barterhub.db")

if __name__ == "__main__":
    migrate_to_sqlite()
