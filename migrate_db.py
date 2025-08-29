
import os
from app import create_app, db
from sqlalchemy import text

def migrate_database():
    app = create_app()
    
    with app.app_context():
        try:
            # Check if is_read column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'chat_messages' AND column_name = 'is_read'
            """))
            
            if not result.fetchone():
                print("Adding is_read column to chat_messages table...")
                db.session.execute(text("""
                    ALTER TABLE chat_messages 
                    ADD COLUMN is_read BOOLEAN DEFAULT FALSE
                """))
                db.session.commit()
                print("Successfully added is_read column!")
            else:
                print("is_read column already exists.")
                
            # Check if offered_products_json column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'chat_messages' AND column_name = 'offered_products_json'
            """))
            
            if not result.fetchone():
                print("Adding offered_products_json column to chat_messages table...")
                db.session.execute(text("""
                    ALTER TABLE chat_messages 
                    ADD COLUMN offered_products_json TEXT
                """))
                db.session.commit()
                print("Successfully added offered_products_json column!")
            else:
                print("offered_products_json column already exists.")
                
            # Check if requested_products_json column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'chat_messages' AND column_name = 'requested_products_json'
            """))
            
            if not result.fetchone():
                print("Adding requested_products_json column to chat_messages table...")
                db.session.execute(text("""
                    ALTER TABLE chat_messages 
                    ADD COLUMN requested_products_json TEXT
                """))
                db.session.commit()
                print("Successfully added requested_products_json column!")
            else:
                print("requested_products_json column already exists.")
                
        except Exception as e:
            print(f"Migration error: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_database()
