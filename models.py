from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import uuid
import random

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    user_role = db.Column(db.String(20), nullable=True)  # 'seller' or 'buyer'
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

    def get_unread_message_count(self):
        """Get total unread messages count (traditional messages + chat messages)"""
        try:
            # Traditional messages
            traditional_unread = Message.query.filter_by(receiver_id=self.id, is_read=False).count()
        except Exception:
            traditional_unread = 0
        
        try:
            # Chat messages - handle case when table doesn't exist or columns are missing
            chat_unread = ChatMessage.query.filter_by(receiver_id=self.id, is_read=False).count()
        except Exception:
            # If ChatMessage table doesn't exist or has issues, return 0
            chat_unread = 0
        
        return traditional_unread + chat_unread

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
    image_filename = db.Column(db.String(120), nullable=True)  # Keep for backward compatibility
    image_url = db.Column(db.String(500), nullable=True)  # For external image URLs
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

    def get_primary_image(self):
        """Get the primary image (first image or fallback to old image fields)"""
        primary_image = ProductImage.query.filter_by(product_id=self.id, is_primary=True).first()
        if primary_image:
            return primary_image

        # Fallback to existing image fields for backward compatibility
        first_image = ProductImage.query.filter_by(product_id=self.id).first()
        if first_image:
            return first_image

        return None

    def get_all_images(self):
        """Get all images for this product"""
        return ProductImage.query.filter_by(product_id=self.id).order_by(ProductImage.is_primary.desc(), ProductImage.id.asc()).all()

    def __repr__(self):
        return f'<Product {self.title}>'

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_filename = db.Column(db.String(120), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    product = db.relationship('Product', backref='images')

    def get_image_url(self):
        """Get the image URL for display"""
        if self.image_url:
            return self.image_url
        elif self.image_filename:
            from flask import url_for
            return url_for('static', filename='uploads/' + self.image_filename)
        return None

    def __repr__(self):
        return f'<ProductImage {self.id} for Product {self.product_id}>'

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

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    buyer = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')

    def __repr__(self):
        return f'<Cart {self.buyer_id} - {self.product_id}>'

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)  # Chat tentang produk tertentu
    message = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, offer, deal, negotiation
    is_read = db.Column(db.Boolean, default=False)

    # Negosiasi dan Deal fields
    offer_price = db.Column(db.Float, nullable=True)  # Harga yang ditawarkan
    offer_quantity = db.Column(db.Integer, default=1)  # Jumlah yang ditawarkan
    is_deal = db.Column(db.Boolean, default=False)  # Apakah ini deal final
    deal_accepted = db.Column(db.Boolean, nullable=True)  # True = accepted, False = rejected, None = pending
    deal_accepted_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)  # Kapan offer/deal expires

    # Conversation grouping
    conversation_id = db.Column(db.String(100), nullable=True)  # Group messages by seller-buyer-product

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_chats')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_chats')
    product = db.relationship('Product', backref='chat_messages')

    def generate_conversation_id(self):
        """Generate unique conversation ID based on participants and product"""
        if self.product_id:
            participants = sorted([self.sender_id, self.receiver_id])
            return f"conv_{participants[0]}_{participants[1]}_product_{self.product_id}"
        else:
            participants = sorted([self.sender_id, self.receiver_id])
            return f"conv_{participants[0]}_{participants[1]}_general"

    def is_expired(self):
        """Check if offer/deal has expired"""
        if self.expires_at and self.expires_at < datetime.utcnow():
            return True
        return False

    def __repr__(self):
        return f'<ChatMessage {self.sender_id} to {self.receiver_id}>'

class ChatConversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(100), unique=True, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)

    # Conversation status
    status = db.Column(db.String(20), default='active')  # active, negotiating, deal_pending, completed, closed
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_message_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Deal tracking
    current_offer_price = db.Column(db.Float, nullable=True)
    current_offer_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    deal_finalized = db.Column(db.Boolean, default=False)
    deal_price = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    seller = db.relationship('User', foreign_keys=[seller_id])
    buyer = db.relationship('User', foreign_keys=[buyer_id])
    product = db.relationship('Product')
    last_message_user = db.relationship('User', foreign_keys=[last_message_by])
    current_offer_user = db.relationship('User', foreign_keys=[current_offer_by])

    def get_unread_count_for_user(self, user_id):
        """Get unread message count for specific user in this conversation"""
        return ChatMessage.query.filter_by(
            conversation_id=self.conversation_id,
            receiver_id=user_id,
            is_read=False
        ).count()

    def __repr__(self):
        return f'<ChatConversation {self.conversation_id}>'