from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    is_suspended = db.Column(db.Boolean, default=False)
    suspension_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='owner', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
    sent_proposals = db.relationship('BarterProposal', foreign_keys='BarterProposal.proposer_id', backref='proposer', lazy=True)
    received_proposals = db.relationship('BarterProposal', foreign_keys='BarterProposal.receiver_id', backref='proposal_receiver', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(20), nullable=False)  # New, Used, Fair, etc.
    estimated_value = db.Column(db.Float, nullable=True)
    image_filename = db.Column(db.String(120), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    
    # Barter Value Factors (1-10 scale)
    utility_score = db.Column(db.Integer, default=5)  # Kebutuhan - seberapa dibutuhkan
    scarcity_score = db.Column(db.Integer, default=5)  # Kelangkaan - seberapa langka
    durability_score = db.Column(db.Integer, default=5)  # Daya tahan
    portability_score = db.Column(db.Integer, default=5)  # Kemudahan dibawa
    seasonal_factor = db.Column(db.Float, default=1.0)  # Faktor musiman (0.5-2.0)
    barter_value_points = db.Column(db.Integer, default=25)  # Total nilai barter
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Relationships
    proposals_offered = db.relationship('BarterProposal', foreign_keys='BarterProposal.offered_product_id', backref='offered_product', lazy=True)
    proposals_wanted = db.relationship('BarterProposal', foreign_keys='BarterProposal.wanted_product_id', backref='wanted_product', lazy=True)
    
    def calculate_barter_value(self):
        """Calculate total barter value based on all factors"""
        base_value = (self.utility_score + self.scarcity_score + 
                     self.durability_score + self.portability_score)
        return int(base_value * self.seasonal_factor)
    
    def update_barter_value(self):
        """Update the stored barter value points"""
        self.barter_value_points = self.calculate_barter_value()
    
    def get_condition_modifier(self):
        """Get value modifier based on condition"""
        modifiers = {
            'New': 1.2,
            'Like New': 1.1,
            'Good': 1.0,
            'Fair': 0.8,
            'Poor': 0.6
        }
        return modifiers.get(self.condition, 1.0)
    
    def get_final_barter_value(self):
        """Get final barter value including condition modifier"""
        return int(self.barter_value_points * self.get_condition_modifier())
    
    def __repr__(self):
        return f'<Product {self.title}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.receiver_id}>'

class BarterProposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    proposer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offered_product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    wanted_product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    def __repr__(self):
        return f'<BarterProposal {self.id} - {self.status}>'
