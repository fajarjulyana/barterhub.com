from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='pembeli')  # penjual, pembeli, admin
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='owner', lazy='dynamic', foreign_keys='Product.user_id')
    sent_messages = db.relationship('ChatMessage', foreign_keys='ChatMessage.sender_id', backref='sender', lazy='dynamic')
    transactions_as_seller = db.relationship('Transaction', foreign_keys='Transaction.seller_id', backref='seller', lazy='dynamic')
    transactions_as_buyer = db.relationship('Transaction', foreign_keys='Transaction.buyer_id', backref='buyer', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_seller(self):
        return self.role == 'penjual'
    
    def is_buyer(self):
        return self.role == 'pembeli'
    

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(20), nullable=False)  # New, Like New, Good, Fair, Poor
    
    # Point calculation factors (1-10 scale)
    utility_score = db.Column(db.Integer, default=5)
    scarcity_score = db.Column(db.Integer, default=5)
    durability_score = db.Column(db.Integer, default=5)
    portability_score = db.Column(db.Integer, default=5)
    seasonal_score = db.Column(db.Integer, default=5)
    
    # Calculated points
    total_points = db.Column(db.Integer, default=0)
    
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    offers_received = db.relationship('TransactionOffer', backref='product', lazy='dynamic')
    
    def calculate_points(self):
        """Calculate total points based on various factors"""
        # Base calculation
        base_score = (self.utility_score + self.scarcity_score + self.durability_score + 
                     self.portability_score + self.seasonal_score) / 5
        
        # Condition multiplier
        condition_multipliers = {
            'New': 1.0,
            'Like New': 0.9,
            'Good': 0.8,
            'Fair': 0.6,
            'Poor': 0.4
        }
        
        condition_multiplier = condition_multipliers.get(self.condition, 0.8)
        self.total_points = int(base_score * condition_multiplier * 10)  # Scale to reasonable range
        
        return self.total_points
    
    def get_main_image(self):
        """Get the main product image"""
        image = self.images.filter_by(is_main=True).first()
        if not image:
            image = self.images.first()
        return image.filename if image else 'default-product.jpg'

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatRoom(db.Model):
    __tablename__ = 'chat_rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])
    product = db.relationship('Product')
    messages = db.relationship('ChatMessage', backref='room', lazy='dynamic', cascade='all, delete-orphan')

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, offer, counter_offer, system
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Untuk pesan tipe offer/counter_offer
    offered_products_json = db.Column(db.Text)  # JSON array of {product_id, quantity}
    requested_products_json = db.Column(db.Text)  # JSON array of {product_id, quantity}

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    status = db.Column(db.String(20), default='pending')  # pending, agreed, shipped, completed, cancelled, dispute
    
    # Shipping information
    seller_tracking_number = db.Column(db.String(100))
    buyer_tracking_number = db.Column(db.String(100))
    seller_shipped_at = db.Column(db.DateTime)
    buyer_shipped_at = db.Column(db.DateTime)
    seller_received_at = db.Column(db.DateTime)
    buyer_received_at = db.Column(db.DateTime)
    
    # Points
    total_seller_points = db.Column(db.Integer, default=0)
    total_buyer_points = db.Column(db.Integer, default=0)
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product')
    offers = db.relationship('TransactionOffer', backref='transaction', lazy='dynamic', cascade='all, delete-orphan')

class TransactionOffer(db.Model):
    __tablename__ = 'transaction_offers'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    offered_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    offered_by = db.relationship('User')
