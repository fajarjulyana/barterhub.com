import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import or_, and_
from app import db
from models import User, Product, Category, ProductImage, ChatRoom, ChatMessage, Transaction, TransactionOffer
from forms import LoginForm, RegisterForm, ProductForm, ChatMessageForm, OfferForm, TrackingForm
from utils import save_uploaded_file, calculate_point_balance, get_transaction_status_text, get_condition_text

# Main blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Get featured products
    featured_products = Product.query.filter_by(is_available=True).order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', products=featured_products, categories=categories)

@main.route('/profile')
@login_required
def profile():
    user_products = current_user.products.filter_by(is_available=True).all()
    user_transactions = Transaction.query.filter(
        or_(Transaction.seller_id == current_user.id, Transaction.buyer_id == current_user.id)
    ).order_by(Transaction.created_at.desc()).limit(10).all()
    return render_template('profile.html', products=user_products, transactions=user_transactions)

# Authentication blueprint
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role=form.role.data,
            phone=form.phone.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Selamat datang, {user.full_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Username atau password salah.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('main.index'))

# Products blueprint
products = Blueprint('products', __name__)

@products.route('/')
def list_products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    condition = request.args.get('condition', '')
    
    query = Product.query.filter_by(is_available=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(
            or_(Product.title.ilike(f'%{search}%'), 
                Product.description.ilike(f'%{search}%'))
        )
    
    if condition:
        query = query.filter_by(condition=condition)
    
    products_pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    categories = Category.query.all()
    conditions = ['New', 'Like New', 'Good', 'Fair', 'Poor']
    
    return render_template('products/list.html', 
                         products=products_pagination.items,
                         pagination=products_pagination,
                         categories=categories,
                         conditions=conditions,
                         current_category=category_id,
                         current_search=search,
                         current_condition=condition)

@products.route('/<int:id>')
def detail(id):
    product = Product.query.get_or_404(id)
    similar_products = Product.query.filter(
        and_(Product.category_id == product.category_id,
             Product.id != product.id,
             Product.is_available == True)
    ).limit(4).all()
    
    return render_template('products/detail.html', product=product, similar_products=similar_products)

@products.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    # Semua user terdaftar bisa menambah produk untuk ditukar
    
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            user_id=current_user.id,
            category_id=form.category_id.data,
            title=form.title.data,
            description=form.description.data,
            condition=form.condition.data,
            utility_score=form.utility_score.data,
            scarcity_score=form.scarcity_score.data,
            durability_score=form.durability_score.data,
            portability_score=form.portability_score.data,
            seasonal_score=form.seasonal_score.data
        )
        
        # Calculate points
        product.calculate_points()
        
        db.session.add(product)
        db.session.flush()  # Get the product ID
        
        # Handle image uploads
        if form.images.data:
            files = request.files.getlist('images')
            for i, file in enumerate(files[:5]):  # Max 5 images
                if file and file.filename:
                    filename = save_uploaded_file(file, 'products')
                    if filename:
                        image = ProductImage(
                            product_id=product.id,
                            filename=filename,
                            is_main=(i == 0)  # First image is main
                        )
                        db.session.add(image)
        
        db.session.commit()
        flash('Produk berhasil ditambahkan!', 'success')
        return redirect(url_for('products.detail', id=product.id))
    
    return render_template('products/add.html', form=form)

@products.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    
    if product.user_id != current_user.id and not current_user.is_admin():
        flash('Anda tidak memiliki akses untuk mengedit produk ini.', 'error')
        return redirect(url_for('products.detail', id=id))
    
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        product.calculate_points()
        
        # Handle new image uploads
        if form.images.data:
            files = request.files.getlist('images')
            for file in files[:5]:  # Max 5 images
                if file and file.filename:
                    filename = save_uploaded_file(file, 'products')
                    if filename:
                        image = ProductImage(
                            product_id=product.id,
                            filename=filename,
                            is_main=False
                        )
                        db.session.add(image)
        
        db.session.commit()
        flash('Produk berhasil diperbarui!', 'success')
        return redirect(url_for('products.detail', id=id))
    
    return render_template('products/edit.html', form=form, product=product)

# Chat blueprint
chat = Blueprint('chat', __name__)

@chat.route('/rooms')
@login_required
def get_rooms():
    """API endpoint untuk mendapatkan daftar chat rooms"""
    try:
        rooms = ChatRoom.query.filter(
            or_(ChatRoom.user1_id == current_user.id, ChatRoom.user2_id == current_user.id)
        ).all()
    except Exception as e:
        # If status column doesn't exist, return empty rooms
        print(f"Database error: {e}")
        return jsonify({
            'rooms': [],
            'total_unread': 0
        })
    
    rooms_data = []
    total_unread = 0
    
    for room in rooms:
        # Tentukan siapa lawan chat
        other_user = room.user2.full_name if room.user1_id == current_user.id else room.user1.full_name
        
        # Hitung pesan yang belum dibaca
        unread_count = ChatMessage.query.filter(
            and_(
                ChatMessage.room_id == room.id,
                ChatMessage.sender_id != current_user.id,
                ChatMessage.is_read == False
            )
        ).count()
        
        total_unread += unread_count
        
        # Pesan terakhir
        last_message = ChatMessage.query.filter_by(room_id=room.id).order_by(ChatMessage.created_at.desc()).first()
        
        rooms_data.append({
            'id': room.id,
            'product_name': room.product.title,
            'other_user': other_user,
            'unread_count': unread_count,
            'last_message': last_message.message if last_message else 'Belum ada pesan',
            'last_message_time': last_message.created_at.strftime('%H:%M') if last_message else '',
            'status': 'active'  # Default status since column doesn't exist yet
        })
    
    return jsonify({
        'rooms': rooms_data,
        'total_unread': total_unread
    })

@chat.route('/room/<int:product_id>')
@login_required
def room(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.user_id == current_user.id:
        flash('Anda tidak dapat chat dengan diri sendiri.', 'error')
        return redirect(url_for('products.detail', id=product_id))
    
    # Find or create chat room
    chat_room = ChatRoom.query.filter(
        or_(
            and_(ChatRoom.user1_id == current_user.id, ChatRoom.user2_id == product.user_id),
            and_(ChatRoom.user1_id == product.user_id, ChatRoom.user2_id == current_user.id)
        ),
        ChatRoom.product_id == product_id
    ).first()
    
    if not chat_room:
        chat_room = ChatRoom(
            user1_id=current_user.id,
            user2_id=product.user_id,
            product_id=product_id
        )
        db.session.add(chat_room)
        db.session.commit()
    
    messages = chat_room.messages.order_by(ChatMessage.created_at.asc()).all()
    form = ChatMessageForm()
    
    if form.validate_on_submit():
        message = ChatMessage(
            room_id=chat_room.id,
            sender_id=current_user.id,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Pesan terkirim!', 'success')
        return redirect(url_for('chat.room', product_id=product_id))
    
    return render_template('chat/room.html', 
                         chat_room=chat_room, 
                         messages=messages, 
                         form=form, 
                         product=product)

@chat.route('/room/<int:room_id>/send_negotiation', methods=['POST'])
@login_required 
def send_negotiation(room_id):
    """Endpoint untuk mengirim penawaran negosiasi"""
    import json
    
    chat_room = ChatRoom.query.get_or_404(room_id)
    
    # Cek akses
    if (chat_room.user1_id != current_user.id and 
        chat_room.user2_id != current_user.id):
        return jsonify({'success': False, 'error': 'Akses ditolak'}), 403
    
    data = request.get_json()
    
    message = ChatMessage(
        room_id=room_id,
        sender_id=current_user.id,
        message=data.get('message', ''),
        message_type='offer',
        offered_products_json=json.dumps(data.get('offered_products', [])),
        requested_products_json=json.dumps(data.get('requested_products', []))
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'success': True})

@chat.route('/offer/<int:message_id>/accept', methods=['POST'])
@login_required
def accept_offer(message_id):
    """Terima penawaran dan buat transaksi"""
    message = ChatMessage.query.get_or_404(message_id)
    chat_room = message.room
    
    # Cek akses
    if (chat_room.user1_id != current_user.id and 
        chat_room.user2_id != current_user.id and
        message.sender_id == current_user.id):
        return jsonify({'success': False, 'error': 'Anda tidak dapat menerima penawaran sendiri'}), 403
    
    # Buat transaksi baru
    # Tentukan siapa penjual dan pembeli berdasarkan produk
    product = chat_room.product
    seller_id = product.user_id
    buyer_id = chat_room.user1_id if chat_room.user1_id != seller_id else chat_room.user2_id
    
    transaction = Transaction(
        seller_id=seller_id,
        buyer_id=buyer_id,
        product_id=chat_room.product_id,
        status='agreed',
        notes=f'Penawaran diterima dari chat message #{message_id}'
    )
    
    db.session.add(transaction)
    
    # Tambahkan pesan sistem
    system_message = ChatMessage(
        room_id=chat_room.id,
        sender_id=current_user.id,
        message=f'✅ Penawaran diterima! Transaksi #{transaction.id} telah dibuat. Silakan lanjutkan ke tahap pengiriman.',
        message_type='system'
    )
    db.session.add(system_message)
    
    db.session.commit()
    
    return jsonify({'success': True, 'transaction_id': transaction.id})

@chat.route('/offer/<int:message_id>/decline', methods=['POST'])
@login_required
def decline_offer(message_id):
    """Tolak penawaran"""
    message = ChatMessage.query.get_or_404(message_id)
    chat_room = message.room
    
    # Cek akses
    if (chat_room.user1_id != current_user.id and 
        chat_room.user2_id != current_user.id and
        message.sender_id == current_user.id):
        return jsonify({'success': False, 'error': 'Anda tidak dapat menolak penawaran sendiri'}), 403
    
    data = request.get_json() or {}
    reason = data.get('reason', '')
    
    # Tambahkan pesan sistem
    decline_msg = f'❌ Penawaran ditolak oleh {current_user.full_name}'
    if reason:
        decline_msg += f'. Alasan: {reason}'
    
    system_message = ChatMessage(
        room_id=chat_room.id,
        sender_id=current_user.id,
        message=decline_msg,
        message_type='system'
    )
    db.session.add(system_message)
    db.session.commit()
    
    return jsonify({'success': True})

# Transactions blueprint
transactions = Blueprint('transactions', __name__)

@transactions.route('/')
@login_required
def list_transactions():
    page = request.args.get('page', 1, type=int)
    
    user_transactions = Transaction.query.filter(
        or_(Transaction.seller_id == current_user.id, Transaction.buyer_id == current_user.id)
    ).order_by(Transaction.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('transactions/list.html', 
                         transactions=user_transactions.items,
                         pagination=user_transactions)

@transactions.route('/<int:id>')
@login_required
def detail(id):
    transaction = Transaction.query.get_or_404(id)
    
    if (transaction.seller_id != current_user.id and 
        transaction.buyer_id != current_user.id and 
        not current_user.is_admin()):
        flash('Anda tidak memiliki akses untuk melihat transaksi ini.', 'error')
        return redirect(url_for('transactions.list_transactions'))
    
    tracking_form = TrackingForm()
    
    if tracking_form.validate_on_submit():
        if current_user.id == transaction.seller_id:
            transaction.seller_tracking_number = tracking_form.tracking_number.data
            transaction.seller_shipped_at = datetime.utcnow()
        elif current_user.id == transaction.buyer_id:
            transaction.buyer_tracking_number = tracking_form.tracking_number.data
            transaction.buyer_shipped_at = datetime.utcnow()
        
        # Update status if both have shipped
        if (transaction.seller_tracking_number and 
            transaction.buyer_tracking_number and 
            transaction.status == 'agreed'):
            transaction.status = 'shipped'
        
        db.session.commit()
        flash('Nomor resi berhasil diperbarui!', 'success')
        return redirect(url_for('transactions.detail', id=id))
    
    return render_template('transactions/detail.html', 
                         transaction=transaction, 
                         tracking_form=tracking_form)

@transactions.route('/<int:id>/receipt')
@login_required
def receipt(id):
    """Cetak resi pengiriman"""
    transaction = Transaction.query.get_or_404(id)
    
    if (transaction.seller_id != current_user.id and 
        transaction.buyer_id != current_user.id and 
        not current_user.is_admin()):
        flash('Anda tidak memiliki akses untuk melihat resi ini.', 'error')
        return redirect(url_for('transactions.list_transactions'))
    
    return render_template('transactions/receipt.html', transaction=transaction)

@transactions.route('/<int:id>/tracking')
@login_required
def tracking(id):
    """Tracking ekspedisi pengiriman"""
    transaction = Transaction.query.get_or_404(id)
    
    if (transaction.seller_id != current_user.id and 
        transaction.buyer_id != current_user.id and 
        not current_user.is_admin()):
        flash('Anda tidak memiliki akses untuk tracking transaksi ini.', 'error')
        return redirect(url_for('transactions.list_transactions'))
    
    # Simulasi data tracking (dalam implementasi nyata, ini akan mengintegrasikan dengan API ekspedisi)
    tracking_data = {
        'seller_tracking': get_tracking_info(transaction.seller_tracking_number) if transaction.seller_tracking_number else None,
        'buyer_tracking': get_tracking_info(transaction.buyer_tracking_number) if transaction.buyer_tracking_number else None
    }
    
    return render_template('transactions/tracking.html', 
                         transaction=transaction, 
                         tracking_data=tracking_data)

def get_tracking_info(tracking_number):
    """Simulasi mendapatkan informasi tracking dari API ekspedisi"""
    import random
    from datetime import datetime, timedelta
    
    if not tracking_number:
        return None
    
    # Simulasi status tracking
    statuses = [
        'Paket diterima oleh kurir',
        'Paket dalam perjalanan ke hub',
        'Paket tiba di hub asal', 
        'Paket dalam perjalanan ke kota tujuan',
        'Paket tiba di hub tujuan',
        'Paket dalam perjalanan untuk pengiriman',
        'Paket sudah dikirim ke alamat tujuan',
        'Paket berhasil diterima'
    ]
    
    # Generate timeline tracking
    timeline = []
    for i, status in enumerate(statuses[:random.randint(3, len(statuses))]):
        timeline.append({
            'status': status,
            'time': (datetime.now() - timedelta(days=len(statuses)-i, hours=random.randint(0, 23))).strftime('%d/%m/%Y %H:%M'),
            'location': f'Hub {["Jakarta", "Bandung", "Surabaya", "Medan", "Yogyakarta"][random.randint(0, 4)]}',
            'is_current': i == len(statuses)-1
        })
    
    return {
        'tracking_number': tracking_number,
        'courier': random.choice(['JNE', 'J&T Express', 'SiCepat', 'Pos Indonesia']),
        'status': timeline[-1]['status'] if timeline else 'Belum ada update',
        'timeline': timeline
    }

@transactions.route('/<int:id>/auto_confirm')
@login_required  
def auto_confirm_check(id):
    """Cek dan lakukan auto konfirmasi setelah 24 jam"""
    transaction = Transaction.query.get_or_404(id)
    
    # Cek apakah sudah 24 jam setelah kedua barang sampai
    if (transaction.status == 'shipped' and 
        transaction.seller_shipped_at and transaction.buyer_shipped_at):
        
        # Hitung 24 jam dari pengiriman terakhir
        last_shipped = max(transaction.seller_shipped_at, transaction.buyer_shipped_at)
        auto_confirm_time = last_shipped + timedelta(hours=24)
        
        if datetime.utcnow() >= auto_confirm_time:
            # Auto konfirmasi jika belum dikonfirmasi manual
            if not transaction.seller_received_at:
                transaction.seller_received_at = datetime.utcnow()
                
            if not transaction.buyer_received_at:
                transaction.buyer_received_at = datetime.utcnow()
            
            transaction.status = 'completed'
            db.session.commit()
            
            return jsonify({
                'auto_confirmed': True,
                'message': 'Transaksi otomatis selesai karena tidak ada konfirmasi dalam 24 jam'
            })
    
    return jsonify({'auto_confirmed': False})

@transactions.route('/<int:id>/dispute', methods=['GET', 'POST'])
@login_required
def dispute(id):
    """Buat atau lihat sengketa transaksi"""
    transaction = Transaction.query.get_or_404(id)
    
    if (transaction.seller_id != current_user.id and 
        transaction.buyer_id != current_user.id):
        flash('Anda tidak memiliki akses untuk transaksi ini.', 'error')
        return redirect(url_for('transactions.list_transactions'))
    
    if request.method == 'POST':
        reason = request.form.get('reason')
        description = request.form.get('description')
        
        # Update status transaksi menjadi dispute
        transaction.status = 'dispute'
        transaction.notes = f"Sengketa: {reason}\nDeskripsi: {description}\nDilaporkan oleh: {current_user.full_name}"
        db.session.commit()
        
        flash('Sengketa berhasil dilaporkan. Tim kami akan meninjau dalam 1x24 jam.', 'info')
        return redirect(url_for('transactions.detail', id=id))
    
    return render_template('transactions/dispute.html', transaction=transaction)

@transactions.route('/<int:id>/confirm_received')
@login_required
def confirm_received(id):
    transaction = Transaction.query.get_or_404(id)
    
    if transaction.seller_id == current_user.id:
        if not transaction.seller_received_at:
            transaction.seller_received_at = datetime.utcnow()
            flash(f'Konfirmasi penerimaan berhasil! Anda telah mengkonfirmasi menerima barang dari {transaction.buyer.full_name}.', 'success')
        else:
            flash('Anda sudah mengkonfirmasi penerimaan barang sebelumnya.', 'info')
    elif transaction.buyer_id == current_user.id:
        if not transaction.buyer_received_at:
            transaction.buyer_received_at = datetime.utcnow()
            flash(f'Konfirmasi penerimaan berhasil! Anda telah mengkonfirmasi menerima barang dari {transaction.seller.full_name}.', 'success')
        else:
            flash('Anda sudah mengkonfirmasi penerimaan barang sebelumnya.', 'info')
    else:
        flash('Anda tidak memiliki akses untuk mengkonfirmasi transaksi ini.', 'error')
        return redirect(url_for('transactions.detail', id=id))
    
    # Mark as completed if both parties confirmed
    if transaction.seller_received_at and transaction.buyer_received_at:
        transaction.status = 'completed'
        flash('🎉 Transaksi barter berhasil diselesaikan! Kedua belah pihak telah mengkonfirmasi penerimaan barang.', 'success')
        
        # Tambahkan pesan sistem ke chat room jika ada
        chat_room = ChatRoom.query.filter(
            and_(
                ChatRoom.product_id == transaction.product_id,
                or_(
                    and_(ChatRoom.user1_id == transaction.seller_id, ChatRoom.user2_id == transaction.buyer_id),
                    and_(ChatRoom.user1_id == transaction.buyer_id, ChatRoom.user2_id == transaction.seller_id)
                )
            )
        ).first()
        
        if chat_room:
            system_message = ChatMessage(
                room_id=chat_room.id,
                sender_id=current_user.id,
                message=f'🎉 Transaksi barter berhasil diselesaikan! Kedua belah pihak telah mengkonfirmasi penerimaan barang. Terima kasih telah menggunakan BarterHub!',
                message_type='system'
            )
            db.session.add(system_message)
    
    db.session.commit()
    return redirect(url_for('transactions.detail', id=id))

@transactions.route('/create/<int:product_id>', methods=['GET', 'POST'])
@login_required
def create_offer(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.user_id == current_user.id:
        flash('Anda tidak dapat menawar produk sendiri.', 'error')
        return redirect(url_for('products.detail', id=product_id))
    
    # Get user's products for offering
    user_products = current_user.products.filter_by(is_available=True).all()
    
    if request.method == 'POST':
        offered_product_ids = request.form.getlist('offered_products')
        
        if not offered_product_ids:
            flash('Pilih minimal satu produk untuk ditawarkan.', 'error')
            return redirect(url_for('transactions.create_offer', product_id=product_id))
        
        # Create transaction
        transaction = Transaction(
            seller_id=product.user_id,
            buyer_id=current_user.id,
            product_id=product_id,
            total_seller_points=product.total_points
        )
        
        db.session.add(transaction)
        db.session.flush()
        
        # Add offered products
        total_buyer_points = 0
        for product_id_str in offered_product_ids:
            offered_product = Product.query.get(int(product_id_str))
            if offered_product and offered_product.user_id == current_user.id:
                offer = TransactionOffer(
                    transaction_id=transaction.id,
                    product_id=offered_product.id,
                    offered_by_id=current_user.id,
                    points=offered_product.total_points
                )
                db.session.add(offer)
                total_buyer_points += offered_product.total_points
        
        transaction.total_buyer_points = total_buyer_points
        db.session.commit()
        
        flash('Penawaran berhasil dikirim!', 'success')
        return redirect(url_for('transactions.detail', id=transaction.id))
    
    return render_template('transactions/create_offer.html', 
                         product=product, 
                         user_products=user_products)

# Admin blueprint
admin = Blueprint('admin', __name__)

@admin.before_request
@login_required
def require_admin():
    if not current_user.is_admin():
        flash('Akses ditolak. Hanya admin yang dapat mengakses halaman ini.', 'error')
        return redirect(url_for('main.index'))

@admin.route('/dashboard')
def dashboard():
    from models import Report
    
    # User Management Statistics
    total_users = User.query.count()
    banned_users = User.query.filter_by(is_banned=True).count()
    active_sellers = User.query.filter_by(role='penjual', is_active=True, is_banned=False).count()
    active_buyers = User.query.filter_by(role='pembeli', is_active=True, is_banned=False).count()
    
    # Report Statistics
    pending_reports = Report.query.filter_by(status='pending').count()
    total_reports = Report.query.count()
    recent_violations = User.query.filter(User.violation_count > 0).order_by(User.violation_count.desc()).limit(5).all()
    
    # Recent Reports
    recent_reports = Report.query.order_by(Report.created_at.desc()).limit(5).all()
    
    # High-risk users (with multiple violations)
    high_risk_users = User.query.filter(User.violation_count >= 3).order_by(User.violation_count.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         banned_users=banned_users,
                         active_sellers=active_sellers,
                         active_buyers=active_buyers,
                         pending_reports=pending_reports,
                         total_reports=total_reports,
                         recent_reports=recent_reports,
                         recent_violations=recent_violations,
                         high_risk_users=high_risk_users)

@admin.route('/users')
def users():
    page = request.args.get('page', 1, type=int)
    users_pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html', 
                         users=users_pagination.items,
                         pagination=users_pagination)

@admin.route('/users/<int:id>/toggle_status')
def toggle_user_status(id):
    user = User.query.get_or_404(id)
    if user.is_admin():
        flash('Tidak dapat mengubah status admin.', 'error')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        status = 'diaktifkan' if user.is_active else 'dinonaktifkan'
        flash(f'User {user.username} berhasil {status}.', 'success')
    
    return redirect(url_for('admin.users'))

@admin.route('/users/<int:id>/ban', methods=['POST'])
def ban_user(id):
    user = User.query.get_or_404(id)
    ban_reason = request.form.get('ban_reason', 'Pelanggaran aturan platform')
    
    if user.is_admin():
        flash('Tidak dapat memban admin.', 'error')
    else:
        user.ban_user(ban_reason, current_user.id)
        user.add_violation()
        db.session.commit()
        flash(f'User {user.username} berhasil dibanned. Alasan: {ban_reason}', 'success')
    
    return redirect(url_for('admin.users'))

@admin.route('/users/<int:id>/unban')
def unban_user(id):
    user = User.query.get_or_404(id)
    user.unban_user()
    db.session.commit()
    flash(f'User {user.username} berhasil di-unban.', 'success')
    
    return redirect(url_for('admin.users'))

@admin.route('/reports')
def reports():
    from models import Report
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    type_filter = request.args.get('type', '')
    
    query = Report.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if type_filter:
        query = query.filter_by(report_type=type_filter)
    
    reports_pagination = query.order_by(Report.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/reports.html', 
                         reports=reports_pagination.items,
                         pagination=reports_pagination,
                         status_filter=status_filter,
                         type_filter=type_filter)

@admin.route('/reports/<int:id>/resolve', methods=['POST'])
def resolve_report(id):
    from models import Report
    report = Report.query.get_or_404(id)
    action = request.form.get('action')  # 'dismiss', 'warn', 'ban'
    response = request.form.get('admin_response', '')
    
    report.status = 'resolved'
    report.admin_response = response
    report.resolved_by = current_user.id
    report.resolved_at = datetime.utcnow()
    
    if action == 'ban':
        reported_user = report.reported_user
        ban_reason = f"Laporan: {report.subject}"
        reported_user.ban_user(ban_reason, current_user.id)
        reported_user.add_violation()
    elif action == 'warn':
        reported_user = report.reported_user
        reported_user.add_violation()
    
    db.session.commit()
    flash(f'Laporan berhasil diselesaikan dengan aksi: {action}', 'success')
    
    return redirect(url_for('admin.reports'))

@admin.route('/products')
def admin_products():
    page = request.args.get('page', 1, type=int)
    products_pagination = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/products.html', 
                         products=products_pagination.items,
                         pagination=products_pagination)

@admin.route('/transactions')
def admin_transactions():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = Transaction.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    transactions_pagination = query.order_by(Transaction.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/transactions.html', 
                         transactions=transactions_pagination.items,
                         pagination=transactions_pagination,
                         current_status=status_filter)

# Initialize default data function (removed before_app_first_request decorator)
def init_db():
    try:
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
        
        # Create admin user if doesn't exist
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
            print("Admin user created")
        else:
            print("Admin user already exists")
            
    except Exception as e:
        print(f"Error in init_db: {e}")
        db.session.rollback()
