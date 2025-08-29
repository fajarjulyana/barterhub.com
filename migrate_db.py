import os
from app import create_app
from models import db, User, Category, Product, ProductImage, ChatRoom, ChatMessage, Transaction, TransactionOffer, Report

def migrate_database():
    """Create SQLite database and tables"""
    app = create_app()

    with app.app_context():
        try:
            # Drop all tables if they exist (for clean migration)
            print("Dropping existing tables...")
            db.drop_all()

            # Create all tables from scratch
            print("Creating all tables...")
            db.create_all()

            # Initialize default data
            print("Initializing default data...")

            # Create default categories
            categories = [
                {"name": "Elektronik", "description": "Gadget, komputer, dan perangkat elektronik"},
                {"name": "Fashion", "description": "Pakaian, sepatu, dan aksesoris"},
                {"name": "Hobi & Koleksi", "description": "Barang koleksi, mainan, dan hobi"},
                {"name": "Rumah Tangga", "description": "Peralatan rumah tangga dan dekorasi"},
                {"name": "Kendaraan", "description": "Motor, mobil, dan aksesoris kendaraan"},
                {"name": "Olahraga", "description": "Peralatan dan perlengkapan olahraga"},
                {"name": "Buku & Media", "description": "Buku, CD, DVD, dan media lainnya"},
                {"name": "Lainnya", "description": "Kategori lain yang tidak termasuk di atas"}
            ]

            for cat_data in categories:
                existing_cat = Category.query.filter_by(name=cat_data["name"]).first()
                if not existing_cat:
                    category = Category(
                        name=cat_data["name"],
                        description=cat_data["description"]
                    )
                    db.session.add(category)

            # Create default admin user
            admin_user = User.query.filter_by(username='fajarjulyana').first()
            if not admin_user:
                admin_user = User(
                    username='fajarjulyana',
                    email='admin@barterhub.com',
                    full_name='Admin BarterHub',
                    role='admin',
                    phone='081234567890',
                    address='Jl. Admin No. 1, Jakarta',
                    kode_pos='12345'
                )
                admin_user.set_password('fajar123')
                db.session.add(admin_user)
                print("Admin user created: fajarjulyana/fajar123")
            else:
                print("Admin user already exists")

            db.session.commit()
            print("SQLite database migration completed successfully!")

        except Exception as e:
            print(f"Migration error: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    migrate_database()