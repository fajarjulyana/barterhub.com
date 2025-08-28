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
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, completed, negotiating
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Negotiation fields
    seller_asking_price = db.Column(db.Float, nullable=True)  # Harga yang diminta penjual
    buyer_offer_price = db.Column(db.Float, nullable=True)   # Tawaran pembeli
    additional_items_requested = db.Column(db.Text, nullable=True)  # Item tambahan yang diminta
    quantity_requested = db.Column(db.Integer, default=1)    # Jumlah yang diminta
    negotiation_round = db.Column(db.Integer, default=0)     # Putaran negosiasi
    
    # Foreign Keys
    proposer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offered_product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    wanted_product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    # Relationships
    negotiations = db.relationship('Negotiation', backref='proposal', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<BarterProposal {self.id} - {self.status}>'

class Negotiation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('barter_proposal.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    offer_price = db.Column(db.Float, nullable=True)
    additional_items = db.Column(db.Text, nullable=True)
    quantity_offered = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = db.relationship('User', backref='negotiations')
    
    def __repr__(self):
        return f'<Negotiation {self.id} for Proposal {self.proposal_id}>'

class TransactionReceipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(20), unique=True, nullable=False)
    proposal_id = db.Column(db.Integer, db.ForeignKey('barter_proposal.id'), nullable=False)
    
    # Transaction details
    seller_name = db.Column(db.String(100), nullable=False)
    buyer_name = db.Column(db.String(100), nullable=False)
    main_item_offered = db.Column(db.String(200), nullable=False)
    main_item_wanted = db.Column(db.String(200), nullable=False)
    additional_items_detail = db.Column(db.Text, nullable=True)
    final_agreed_price = db.Column(db.Float, nullable=True)
    
    # Shipping details
    shipping_cost = db.Column(db.Float, nullable=True)
    shipping_method = db.Column(db.String(50), nullable=True)
    tracking_number = db.Column(db.String(100), nullable=True)
    shipping_address = db.Column(db.Text, nullable=True)
    
    # Status tracking
    transaction_status = db.Column(db.String(20), default='confirmed')  # confirmed, shipped, delivered, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    proposal = db.relationship('BarterProposal', backref='receipt')
    
    def generate_receipt_number(self):
        import random
        import string
        timestamp = self.created_at.strftime('%y%m%d')
        random_suffix = ''.join(random.choices(string.digits, k=4))
        self.receipt_number = f'BH{timestamp}{random_suffix}'
    
    def __repr__(self):
        return f'<TransactionReceipt {self.receipt_number}>'

class ShippingDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey('transaction_receipt.id'), nullable=False)
    
    # Sender details (buyer pays shipping)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_address = db.Column(db.Text, nullable=False)
    sender_phone = db.Column(db.String(20), nullable=False)
    
    # Receiver details
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_address = db.Column(db.Text, nullable=False)
    receiver_phone = db.Column(db.String(20), nullable=False)
    
    # Package details
    package_weight = db.Column(db.Float, nullable=True)  # in kg
    package_dimensions = db.Column(db.String(50), nullable=True)  # e.g., "30x20x10 cm"
    insurance_value = db.Column(db.Float, nullable=True)
    
    # Shipping service details
    courier_service = db.Column(db.String(50), nullable=False)  # JNE, J&T, TIKI, etc.
    service_type = db.Column(db.String(50), nullable=False)  # REG, OKE, YES, etc.
    estimated_delivery = db.Column(db.Integer, nullable=True)  # days
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    receipt = db.relationship('TransactionReceipt', backref='shipping_details')
    
    def __repr__(self):
        return f'<ShippingDetail for Receipt {self.receipt_id}>'
