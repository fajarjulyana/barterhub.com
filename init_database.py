
from app import app, db
import logging

def init_database():
    """Initialize database and create missing tables/columns"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Check if ChatMessage table exists and has all required columns
            inspector = db.inspect(db.engine)
            if 'chat_message' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('chat_message')]
                required_columns = [
                    'message_type', 'offer_price', 'offer_quantity', 'is_deal',
                    'deal_accepted', 'deal_accepted_at', 'expires_at', 'conversation_id'
                ]
                
                missing_columns = [col for col in required_columns if col not in columns]
                
                if missing_columns:
                    print(f"⚠️  Missing columns in chat_message table: {missing_columns}")
                    print("🔄 Adding missing columns...")
                    
                    # Add missing columns with ALTER TABLE statements
                    with db.engine.connect() as conn:
                        if 'message_type' not in columns:
                            conn.execute(db.text("ALTER TABLE chat_message ADD COLUMN message_type VARCHAR(20) DEFAULT 'text'"))
                        if 'offer_price' not in columns:
                            conn.execute(db.text("ALTER TABLE chat_message ADD COLUMN offer_price FLOAT"))
                        if 'offer_quantity' not in columns:
                            conn.execute(db.text("ALTER TABLE chat_message ADD COLUMN offer_quantity INTEGER DEFAULT 1"))
                        if 'is_deal' not in columns:
                            conn.execute(db.text("ALTER TABLE chat_message ADD COLUMN is_deal BOOLEAN DEFAULT FALSE"))
                        if 'deal_accepted' not in columns:
                            conn.execute(db.text("ALTER TABLE chat_message ADD COLUMN deal_accepted BOOLEAN"))
                        if 'deal_accepted_at' not in columns:
                            conn.execute(db.text("ALTER TABLE chat_message ADD COLUMN deal_accepted_at TIMESTAMP"))
                        if 'expires_at' not in columns:
                            conn.execute(db.text("ALTER TABLE chat_message ADD COLUMN expires_at TIMESTAMP"))
                        if 'conversation_id' not in columns:
                            conn.execute(db.text("ALTER TABLE chat_message ADD COLUMN conversation_id VARCHAR(100)"))
                        
                        conn.commit()
                    
                    print("✅ Missing columns added successfully")
                else:
                    print("✅ ChatMessage table has all required columns")
            else:
                print("ℹ️  ChatMessage table will be created by SQLAlchemy")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            logging.error(f"Database initialization error: {e}")

if __name__ == "__main__":
    init_database()
