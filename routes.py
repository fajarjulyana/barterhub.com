import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app import app, db, login_manager # Assuming login_manager is initialized here
from models import User, Product, Category, Message, BarterProposal, Negotiation, TransactionReceipt, ShippingDetail # Added missing imports
import uuid

# Language detection - Default to Indonesian
def get_user_language():
    # Initially, always return Indonesian
    return 'id'

# Internationalization messages
MESSAGES = {
    'en': {
        'login_successful': 'Login successful!',
        'invalid_credentials': 'Invalid username or password',
        'username_exists': 'Username already exists',
        'email_registered': 'Email already registered',
        'registration_successful': 'Registration successful! Please log in.',
        'logged_out': 'You have been logged out.',
        'product_added': 'Product added successfully!',
        'cannot_propose_own': 'You cannot propose a barter for your own product!',
        'only_own_products': 'You can only offer your own products!',
        'proposal_sent': 'Barter proposal sent successfully!',
        'message_sent': 'Message sent successfully!',
        'access_denied_admin': 'Access denied. Admin privileges required.',
        'cannot_deactivate_self': 'You cannot deactivate your own account.',
        'user_activated': 'activated',
        'user_deactivated': 'deactivated',
        'message_to_admin': 'Message has been sent to admin. We will respond soon.',
        'admin_not_found': 'Admin not found. Please try again later.',
        'cannot_suspend_self': 'You cannot suspend your own account.',
        'user_suspended': 'User {username} has been suspended. Store temporarily closed.',
        'user_unsuspended': 'User {username} has been restored. Store can operate again.',
        'access_denied': 'Access denied.',
        'product_deleted': 'Product successfully deleted.',
        'proposal_accepted': 'accepted',
        'proposal_rejected': 'rejected',
        'proposal_responded': 'Proposal successfully {action}.'
    },
    'id': {
        'login_successful': 'Login berhasil!',
        'invalid_credentials': 'Username atau password salah',
        'username_exists': 'Username sudah ada',
        'email_registered': 'Email sudah terdaftar',
        'registration_successful': 'Pendaftaran berhasil! Silakan login.',


from datetime import datetime

# Update user's last seen and online status
@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_user.is_online = True
        try:
            db.session.commit()
        except:
            db.session.rollback()

@app.route('/update_online_status', methods=['POST'])
@login_required
def update_online_status():
    status = request.json.get('status', 'online')
    current_user.is_online = (status == 'online')
    current_user.last_seen = datetime.utcnow()
    try:
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'success': False})

        'logged_out': 'Anda telah logout.',
        'product_added': 'Produk berhasil ditambahkan!',
        'cannot_propose_own': 'Anda tidak dapat mengajukan barter untuk produk sendiri!',
        'only_own_products': 'Anda hanya dapat menawarkan produk milik sendiri!',
        'proposal_sent': 'Proposal barter berhasil dikirim!',
        'message_sent': 'Pesan berhasil dikirim!',
        'access_denied_admin': 'Akses ditolak. Diperlukan hak akses admin.',
        'cannot_deactivate_self': 'Anda tidak dapat menonaktifkan akun sendiri.',
        'user_activated': 'diaktifkan',
        'user_deactivated': 'dinonaktifkan',
        'message_to_admin': 'Pesan telah dikirim ke admin. Kami akan merespons segera.',
        'admin_not_found': 'Admin tidak ditemukan. Silakan coba lagi nanti.',
        'cannot_suspend_self': 'Anda tidak dapat mensuspend akun sendiri.',
        'user_suspended': 'User {username} telah disuspend. Toko ditutup sementara.',
        'user_unsuspended': 'User {username} telah dipulihkan. Toko dapat beroperasi kembali.',
        'access_denied': 'Akses ditolak.',
        'product_deleted': 'Produk berhasil dihapus.',
        'proposal_accepted': 'diterima',
        'proposal_rejected': 'ditolak',
        'proposal_responded': 'Proposal berhasil {action}.'
    }
}

def get_message(key, **kwargs):
    lang = get_user_language()
    message = MESSAGES.get(lang, MESSAGES['en']).get(key, MESSAGES['en'].get(key, key))
    return message.format(**kwargs) if kwargs else message

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Check for suspended users
@app.before_request
def check_suspended_user():
    if current_user.is_authenticated and current_user.is_suspended:
        # Allow access to logout and suspension notice pages only
        allowed_endpoints = ['logout', 'suspended_notice', 'static']
        if request.endpoint not in allowed_endpoints:
            return redirect(url_for('suspended_notice'))

# Update login manager messages to Indonesian
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
login_manager.login_message_category = 'info'


@app.route('/')
def index():
    # Get recent products for homepage
    recent_products = Product.query.filter_by(is_available=True).order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', recent_products=recent_products, categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.active:
            login_user(user)
            next_page = request.args.get('next')
            flash(get_message('login_successful'), 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash(get_message('invalid_credentials'), 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form.get('phone', '')
        role = request.form['role']

        # Validate role selection
        if role not in ['seller', 'buyer']:
            flash('Pilih peran yang valid: Penjual atau Pembeli', 'error')
            return render_template('register.html')

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash(get_message('username_exists'), 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash(get_message('email_registered'), 'error')
            return render_template('register.html')

        # Create new user - NEVER create admin through public registration
        user = User(
            username=username,


@app.route('/choose_role', methods=['GET', 'POST'])
@login_required
def choose_role():
    if request.method == 'POST':
        role = request.form.get('role')
        if role in ['seller', 'buyer']:
            current_user.user_role = role
            db.session.commit()
            flash(f'Peran berhasil dipilih sebagai {role.title()}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Pilihan peran tidak valid.', 'error')
    
    return render_template('choose_role.html')

            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            user_role=role,  # Store the selected role
            is_admin=False   # Always False for public registration
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash(get_message('registration_successful'), 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(get_message('logged_out'), 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Admin gets their own dashboard
    if current_user.is_admin:
        return redirect(url_for('owner_dashboard'))
    
    # Check if user has chosen a role
    if not current_user.user_role:
        flash('Silakan pilih peran Anda sebagai Pembeli atau Penjual.', 'info')
        return redirect(url_for('choose_role'))
    
    # Strict role-based routing
    if current_user.user_role == 'seller':
        return redirect(url_for('seller_dashboard'))
    elif current_user.user_role == 'buyer':
        return redirect(url_for('buyer_dashboard'))
    else:
        # Invalid role, force choose again
        flash('Peran tidak valid. Silakan pilih ulang.', 'error')
        return redirect(url_for('choose_role'))

@app.route('/seller_dashboard')
@login_required
def seller_dashboard():
    # Strict access control - only sellers and admins
    if current_user.user_role != 'seller' and not current_user.is_admin:
        flash('Akses ditolak. Hanya penjual yang dapat mengakses halaman ini.', 'error')
        if current_user.user_role == 'buyer':
            return redirect(url_for('buyer_dashboard'))
        else:
            return redirect(url_for('choose_role'))
    user_products = Product.query.filter_by(owner_id=current_user.id).all()
    received_proposals = BarterProposal.query.filter_by(receiver_id=current_user.id).order_by(BarterProposal.created_at.desc()).limit(5).all()
    sent_proposals = BarterProposal.query.filter_by(proposer_id=current_user.id).order_by(BarterProposal.created_at.desc()).limit(5).all()
    unread_messages = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()

    # Seller-specific stats
    total_proposals_received = BarterProposal.query.filter_by(receiver_id=current_user.id).count()
    successful_trades = BarterProposal.query.filter_by(receiver_id=current_user.id, status='completed').count()

    return render_template('seller_dashboard.html', 
                         user_products=user_products,
                         received_proposals=received_proposals,
                         sent_proposals=sent_proposals,
                         unread_messages=unread_messages,
                         total_proposals_received=total_proposals_received,
                         successful_trades=successful_trades)

@app.route('/buyer_dashboard')
@login_required 
def buyer_dashboard():
    # Strict access control - only buyers and admins
    if current_user.user_role != 'buyer' and not current_user.is_admin:
        flash('Akses ditolak. Hanya pembeli yang dapat mengakses halaman ini.', 'error')
        if current_user.user_role == 'seller':
            return redirect(url_for('seller_dashboard'))
        else:
            return redirect(url_for('choose_role'))
    # Recent products for buyers to browse
    recent_products = Product.query.filter(Product.owner_id != current_user.id, Product.is_available == True).order_by(Product.created_at.desc()).limit(12).all()
    categories = Category.query.all()
    sent_proposals = BarterProposal.query.filter_by(proposer_id=current_user.id).order_by(BarterProposal.created_at.desc()).limit(5).all()
    unread_messages = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()

    # Buyer-specific stats
    total_proposals_sent = BarterProposal.query.filter_by(proposer_id=current_user.id).count()
    successful_purchases = BarterProposal.query.filter_by(proposer_id=current_user.id, status='completed').count()

    return render_template('buyer_dashboard.html',
                         recent_products=recent_products,
                         categories=categories,
                         sent_proposals=sent_proposals,
                         unread_messages=unread_messages,
                         total_proposals_sent=total_proposals_sent,
                         successful_purchases=successful_purchases)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    # Only sellers can add products
    if current_user.user_role != 'seller' and not current_user.is_admin:
        flash('Hanya penjual yang dapat menambahkan produk.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        condition = request.form['condition']
        estimated_value = request.form.get('estimated_value')
        category_id = request.form['category_id']

        # Barter value factors
        utility_score = int(request.form.get('utility_score', 5))
        scarcity_score = int(request.form.get('scarcity_score', 5))
        durability_score = int(request.form.get('durability_score', 5))
        portability_score = int(request.form.get('portability_score', 5))
        seasonal_factor = float(request.form.get('seasonal_factor', 1.0))
        
        # Exchange preference
        exchange_preference = request.form.get('exchange_preference', '')

        # Handle file upload - keep for backward compatibility
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Generate unique filename
                image_filename = f"{uuid.uuid4()}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        product = Product(
            title=title,
            description=description,
            condition=condition,
            estimated_value=float(estimated_value) if estimated_value else None,
            category_id=int(category_id),
            owner_id=current_user.id,
            image_filename=image_filename,
            utility_score=utility_score,
            scarcity_score=scarcity_score,
            durability_score=durability_score,
            portability_score=portability_score,
            seasonal_factor=seasonal_factor,
            exchange_preference=exchange_preference
        )

        # Calculate and set barter value
        product.update_barter_value()

        db.session.add(product)
        db.session.commit()

        # Handle multiple images (up to 5)
        from models import ProductImage
        uploaded_images = request.files.getlist('product_images')
        image_count = 0
        
        for i, file in enumerate(uploaded_images[:5]):  # Limit to 5 images
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                
                # Create ProductImage record
                product_image = ProductImage(
                    product_id=product.id,
                    image_filename=unique_filename,
                    is_primary=(i == 0)  # First image is primary
                )
                db.session.add(product_image)
                image_count += 1
        
        # If no new images uploaded but old image exists, create ProductImage record
        if image_count == 0 and image_filename:
            product_image = ProductImage(
                product_id=product.id,
                image_filename=image_filename,
                is_primary=True
            )
            db.session.add(product_image)
        
        db.session.commit()

        flash(get_message('product_added'), 'success')
        return redirect(url_for('dashboard'))

    categories = Category.query.all()
    return render_template('add_product.html', categories=categories)

@app.route('/browse')
def browse_products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category')
    search = request.args.get('search', '')

    query = Product.query.filter_by(is_available=True)

    if category_id:
        query = query.filter_by(category_id=category_id)

    if search:
        query = query.filter(Product.title.contains(search) | Product.description.contains(search))

    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )

    categories = Category.query.all()
    return render_template('browse_products.html', products=products, categories=categories, 
                         current_category=int(category_id) if category_id else None, search=search)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/propose_barter/<int:product_id>', methods=['POST'])
@login_required
def propose_barter(product_id):
    wanted_product = Product.query.get_or_404(product_id)
    offered_product_id = request.form['offered_product_id']
    message = request.form.get('message', '')

    # Ensure user doesn't propose to themselves
    if wanted_product.owner_id == current_user.id:
        flash(get_message('cannot_propose_own'), 'error')
        return redirect(url_for('product_detail', product_id=product_id))

    offered_product = Product.query.get_or_404(offered_product_id)

    # Ensure the offered product belongs to current user
    if offered_product.owner_id != current_user.id:
        flash(get_message('only_own_products'), 'error')
        return redirect(url_for('product_detail', product_id=product_id))

    proposal = BarterProposal(
        proposer_id=current_user.id,
        receiver_id=wanted_product.owner_id,
        offered_product_id=offered_product_id,
        wanted_product_id=product_id,
        message=message
    )

    db.session.add(proposal)
    db.session.commit()

    flash(get_message('proposal_sent'), 'success')
    return redirect(url_for('product_detail', product_id=product_id))


@app.route('/messages')
@login_required
def messages():
    from models import ChatConversation, ChatMessage
    
    page = request.args.get('page', 1, type=int)
    
    # Get traditional messages
    received_messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).limit(10).all()
    
    # Get chat conversations
    conversations = ChatConversation.query.filter(
        (ChatConversation.seller_id == current_user.id) | 
        (ChatConversation.buyer_id == current_user.id)
    ).order_by(ChatConversation.last_message_at.desc()).all()
    
    # Add unread count for each conversation
    for conv in conversations:
        conv.unread_count = conv.get_unread_count_for_user(current_user.id)
    
    # Mark traditional messages as read
    for message in received_messages:
        if not message.is_read:
            message.is_read = True
    db.session.commit()

    return render_template('messages.html', 
                         messages=received_messages, 
                         conversations=conversations)

@app.route('/send_message/<int:user_id>', methods=['POST'])
@login_required
def send_message(user_id):
    content = request.form['content']

    message = Message(
        sender_id=current_user.id,
        receiver_id=user_id,
        content=content
    )

    db.session.add(message)
    db.session.commit()

    flash(get_message('message_sent'), 'success')
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/profile')
@login_required
def profile():
    user_products = Product.query.filter_by(owner_id=current_user.id).all()
    completed_barters = BarterProposal.query.filter(
        ((BarterProposal.proposer_id == current_user.id) | (BarterProposal.receiver_id == current_user.id)) &
        (BarterProposal.status == 'accepted')
    ).count()

    return render_template('profile.html', user_products=user_products, completed_barters=completed_barters)

# Owner routes
@app.route('/admin')
@login_required
def owner_dashboard():
    if not current_user.is_admin:
        flash(get_message('access_denied_admin'), 'error')
        return redirect(url_for('dashboard'))

    total_users = User.query.count()
    total_products = Product.query.count()
    total_proposals = BarterProposal.query.count()
    active_products = Product.query.filter_by(is_available=True).count()

    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()

    return render_template('owner/dashboard.html',
                         total_users=total_users,
                         total_products=total_products,
                         total_proposals=total_proposals,
                         active_products=active_products,
                         recent_users=recent_users,
                         recent_products=recent_products)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash(get_message('access_denied_admin'), 'error')
        return redirect(url_for('dashboard'))

    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('owner/users.html', users=users)

@app.route('/admin/toggle_user/<int:user_id>')
@login_required
def toggle_user_status(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'error')
        return redirect(url_for('admin_users'))

    user.active = not user.active
    db.session.commit()

    status = 'activated' if user.active else 'deactivated'
    flash(f'User {user.username} has been {status}.', 'success')

    return redirect(url_for('admin_users'))

@app.route('/admin/transactions')
@login_required
def admin_transactions():
    if not current_user.is_admin:
        flash(get_message('access_denied_admin'), 'error')
        return redirect(url_for('dashboard'))

    page = request.args.get('page', 1, type=int)
    proposals = BarterProposal.query.order_by(BarterProposal.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('owner/transactions.html', proposals=proposals)

@app.route('/contact_admin', methods=['GET', 'POST'])
@login_required
def contact_admin():
    if request.method == 'POST':
        content = request.form['content']
        subject = request.form['subject']

        # Find first admin user
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            message_content = f"Subject: {subject}\n\n{content}"
            message = Message(
                sender_id=current_user.id,
                receiver_id=admin.id,
                content=message_content
            )  # type: ignore

            db.session.add(message)
            db.session.commit()

            flash('Pesan telah dikirim ke admin. Kami akan merespons segera.', 'success')
            return redirect(url_for('contact_admin'))
        else:
            flash('Admin tidak ditemukan. Silakan coba lagi nanti.', 'error')

    return render_template('contact_admin.html')

@app.route('/admin/suspend_user/<int:user_id>', methods=['POST'])
@login_required
def suspend_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot suspend your own account.', 'error')
        return redirect(url_for('admin_users'))

    reason = request.form.get('reason', 'Pelanggaran kebijakan platform')
    user.is_suspended = True
    user.suspension_reason = reason
    user.active = False

    # Deactivate all user's products
    for product in user.products:
        product.is_available = False

    db.session.commit()

    flash(f'User {user.username} telah disuspend. Toko ditutup sementara.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/unsuspend_user/<int:user_id>')
@login_required
def unsuspend_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    user.is_suspended = False
    user.suspension_reason = None
    user.active = True

    db.session.commit()

    flash(f'User {user.username} telah dipulihkan. Toko dapat beroperasi kembali.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/create_owner', methods=['GET', 'POST'])
@login_required
def create_owner():
    # Only existing admins can create new admin accounts
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form.get('phone', '')

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username sudah ada', 'error')
            return render_template('owner/create_admin.html')

        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar', 'error')
            return render_template('owner/create_admin.html')

        # Create new admin user
        admin_user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            user_role='admin',
            is_admin=True
        )
        admin_user.set_password(password)

        db.session.add(admin_user)
        db.session.commit()

        flash(f'Admin baru {username} berhasil dibuat!', 'success')
        return redirect(url_for('admin_users'))

    return render_template('owner/create_admin.html')

@app.route('/admin/messages')
@login_required
def admin_messages():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))

    page = request.args.get('page', 1, type=int)

    # Get all messages sent to any admin
    admin_users = User.query.filter_by(is_admin=True).all()
    admin_ids = [admin.id for admin in admin_users]

    messages = Message.query.filter(Message.receiver_id.in_(admin_ids)).order_by(Message.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    # Mark messages as read
    for message in messages.items:
        if not message.is_read and message.receiver_id == current_user.id:
            message.is_read = True
    db.session.commit()

    return render_template('owner/messages.html', messages=messages)

@app.route('/suspended')
@login_required
def suspended_notice():
    if not current_user.is_suspended:
        return redirect(url_for('dashboard'))
    return render_template('suspended.html')

@app.route('/toggle_product_availability/<int:product_id>', methods=['POST'])
@login_required
def toggle_product_availability(product_id):
    product = Product.query.get_or_404(product_id)

    # Only owner can toggle availability
    if product.owner_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})

    product.is_available = not product.is_available
    db.session.commit()

    return jsonify({'success': True, 'is_available': product.is_available})

@app.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # Only owner can delete
    if product.owner_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    # Delete associated proposals first
    BarterProposal.query.filter(
        (BarterProposal.offered_product_id == product_id) |
        (BarterProposal.wanted_product_id == product_id)
    ).delete()

    db.session.delete(product)
    db.session.commit()

    flash('Produk berhasil dihapus.', 'success')
    return redirect(url_for('seller_dashboard'))

@app.route('/respond_proposal/<int:proposal_id>/<status>')
@login_required
def respond_proposal(proposal_id, status):
    proposal = BarterProposal.query.get_or_404(proposal_id)

    # Only receiver can respond
    if proposal.receiver_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    if status in ['accepted', 'rejected']:
        proposal.status = status
        db.session.commit()

        action = 'diterima' if status == 'accepted' else 'ditolak'
        flash(f'Proposal berhasil {action}.', 'success')

    return redirect(url_for('seller_dashboard'))

@app.route('/set_asking_price/<int:proposal_id>', methods=['POST'])
@login_required
def set_asking_price(proposal_id):
    proposal = BarterProposal.query.get_or_404(proposal_id)

    # Only receiver (seller) can set asking price
    if proposal.receiver_id != current_user.id:
        flash('Akses ditolak.', 'error')
        return redirect(url_for('dashboard'))

    asking_price = request.form.get('asking_price')
    additional_items = request.form.get('additional_items', '')
    message = request.form.get('message', '')

    if asking_price:
        proposal.seller_asking_price = float(asking_price)
        proposal.additional_items_requested = additional_items
        proposal.status = 'negotiating'
        proposal.negotiation_round += 1

        # Add negotiation record
        negotiation = Negotiation(
            proposal_id=proposal.id,
            sender_id=current_user.id,
            message=message,
            offer_price=float(asking_price),
            additional_items=additional_items
        )

        db.session.add(negotiation)
        db.session.commit()

        flash('Harga dan permintaan berhasil ditetapkan!', 'success')

    return redirect(url_for('seller_dashboard'))

@app.route('/make_counter_offer/<int:proposal_id>', methods=['POST'])
@login_required
def make_counter_offer(proposal_id):
    proposal = BarterProposal.query.get_or_404(proposal_id)

    # Only proposer (buyer) can make counter offer
    if proposal.proposer_id != current_user.id:
        flash('Akses ditolak.', 'error')
        return redirect(url_for('dashboard'))

    offer_price = request.form.get('offer_price')
    additional_items = request.form.get('additional_items', '')
    quantity = request.form.get('quantity', 1)
    message = request.form.get('message', '')

    if offer_price:
        proposal.buyer_offer_price = float(offer_price)
        proposal.quantity_requested = int(quantity)
        proposal.status = 'negotiating'
        proposal.negotiation_round += 1

        # Add negotiation record
        negotiation = Negotiation(
            proposal_id=proposal.id,
            sender_id=current_user.id,
            message=message,
            offer_price=float(offer_price),
            additional_items=additional_items,
            quantity_offered=int(quantity)
        )

        db.session.add(negotiation)
        db.session.commit()

        flash('Tawaran balasan berhasil dikirim!', 'success')

    return redirect(url_for('buyer_dashboard'))

@app.route('/proposal_detail/<int:proposal_id>')
@login_required
def proposal_detail(proposal_id):
    proposal = BarterProposal.query.get_or_404(proposal_id)

    # Only involved parties can view
    if proposal.proposer_id != current_user.id and proposal.receiver_id != current_user.id:
        flash('Akses ditolak.', 'error')
        return redirect(url_for('dashboard'))

    negotiations = Negotiation.query.filter_by(proposal_id=proposal.id).order_by(Negotiation.created_at.asc()).all()

    return render_template('proposal_detail.html', proposal=proposal, negotiations=negotiations)



@app.route('/transaction_receipt/<int:receipt_id>')
@login_required
def transaction_receipt(receipt_id):
    receipt = TransactionReceipt.query.get_or_404(receipt_id)
    proposal = receipt.proposal

    # Only involved parties can view
    if proposal.proposer_id != current_user.id and proposal.receiver_id != current_user.id:
        flash('Akses ditolak.', 'error')
        return redirect(url_for('dashboard'))

    return render_template('transaction_receipt.html', receipt=receipt)

@app.route('/setup_shipping/<int:receipt_id>', methods=['GET', 'POST'])
@login_required
def setup_shipping(receipt_id):
    receipt = TransactionReceipt.query.get_or_404(receipt_id)
    proposal = receipt.proposal

    # Only buyer can setup shipping (buyer pays shipping)
    if proposal.proposer_id != current_user.id:
        flash('Hanya pembeli yang dapat mengatur pengiriman.', 'error')
        return redirect(url_for('transaction_receipt', receipt_id=receipt_id))

    if request.method == 'POST':
        # Create shipping details
        shipping = ShippingDetail(
            receipt_id=receipt.id,
            sender_name=current_user.get_full_name(),
            sender_address=request.form['sender_address'],
            sender_phone=request.form['sender_phone'],
            receiver_name=proposal.proposal_receiver.get_full_name(),
            receiver_address=request.form['receiver_address'],
            receiver_phone=request.form['receiver_phone'],
            package_weight=float(request.form.get('package_weight', 0)),
            package_dimensions=request.form.get('package_dimensions'),
            insurance_value=float(request.form.get('insurance_value', 0)),
            courier_service=request.form['courier_service'],
            service_type=request.form['service_type'],
            estimated_delivery=int(request.form.get('estimated_delivery', 0))
        )

        # Update receipt with shipping cost
        receipt.shipping_cost = float(request.form['shipping_cost'])
        receipt.shipping_method = f"{shipping.courier_service} {shipping.service_type}"
        receipt.shipping_address = shipping.receiver_address
        receipt.transaction_status = 'shipping_arranged'

        db.session.add(shipping)
        db.session.commit()

        flash('Pengiriman berhasil diatur! Silakan lakukan pembayaran dan pengiriman.', 'success')
        return redirect(url_for('transaction_receipt', receipt_id=receipt_id))

    return render_template('setup_shipping.html', receipt=receipt)

@app.route('/update_tracking/<int:receipt_id>', methods=['POST'])
@login_required
def update_tracking(receipt_id):
    receipt = TransactionReceipt.query.get_or_404(receipt_id)
    proposal = receipt.proposal

    # Only buyer can update tracking
    if proposal.proposer_id != current_user.id:
        flash('Akses ditolak.', 'error')
        return redirect(url_for('transaction_receipt', receipt_id=receipt_id))

    receipt.tracking_number = request.form['tracking_number']
    receipt.transaction_status = 'shipped'

    db.session.commit()

    flash('Nomor resi berhasil diperbarui!', 'success')
    return redirect(url_for('transaction_receipt', receipt_id=receipt_id))

# Cart Management Routes
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    from models import Cart
    
    # Strict role verification
    if current_user.user_role != 'buyer' and not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Hanya pembeli yang dapat menggunakan keranjang'})
    
    try:
        product = Product.query.get_or_404(product_id)
        
        # Validation checks
        if not product.is_available:
            return jsonify({'success': False, 'error': 'Produk tidak tersedia'})
        
        if product.owner_id == current_user.id:
            return jsonify({'success': False, 'error': 'Tidak dapat menambahkan produk sendiri ke keranjang'})
        
        # Check if already in cart
        existing_cart = Cart.query.filter_by(buyer_id=current_user.id, product_id=product_id).first()
        if existing_cart:
            return jsonify({'success': False, 'error': 'Produk sudah ada di keranjang'})
        
        # Add to cart
        cart_item = Cart(buyer_id=current_user.id, product_id=product_id)
        db.session.add(cart_item)
        db.session.commit()
        
        cart_count = Cart.query.filter_by(buyer_id=current_user.id).count()
        return jsonify({
            'success': True, 
            'cart_count': cart_count, 
            'message': 'Produk berhasil ditambahkan ke keranjang'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Gagal menambahkan ke keranjang: {str(e)}'})

@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    from models import Cart
    
    cart_item = Cart.query.get_or_404(cart_id)
    
    if cart_item.buyer_id != current_user.id:
        return jsonify({'success': False, 'error': 'Akses ditolak'})
    
    db.session.delete(cart_item)
    db.session.commit()
    
    cart_count = Cart.query.filter_by(buyer_id=current_user.id).count()
    return jsonify({'success': True, 'cart_count': cart_count})

@app.route('/cart')
@login_required
def view_cart():
    from models import Cart
    
    cart_items = Cart.query.filter_by(buyer_id=current_user.id).all()
    
    # Group cart items by seller
    sellers_cart = {}
    for item in cart_items:
        seller_id = item.product.owner_id
        seller_name = item.product.owner.get_full_name()
        
        if seller_id not in sellers_cart:
            sellers_cart[seller_id] = {
                'seller_name': seller_name,
                'seller': item.product.owner,
                'items': [],
                'total_value': 0
            }
        
        sellers_cart[seller_id]['items'].append(item)
        sellers_cart[seller_id]['total_value'] += item.product.get_final_barter_value()
    
    return render_template('cart.html', cart_items=cart_items, sellers_cart=sellers_cart)

# Chat Management Routes
@app.route('/send_chat_message', methods=['POST'])
@login_required
def send_chat_message():
    from models import ChatMessage, ChatConversation
    
    try:
        receiver_id = int(request.form['receiver_id'])
        product_id = request.form.get('product_id')
        message = request.form['message'].strip()
        message_type = request.form.get('message_type', 'text')
        offer_price = request.form.get('offer_price')
        offer_quantity = request.form.get('offer_quantity', 1)
        
        # Validate message
        if not message:
            return jsonify({'success': False, 'error': 'Pesan tidak boleh kosong'})
        
        # Prevent self-messaging
        if receiver_id == current_user.id:
            return jsonify({'success': False, 'error': 'Tidak dapat mengirim pesan ke diri sendiri'})
    
    except (ValueError, KeyError) as e:
        return jsonify({'success': False, 'error': 'Data tidak valid'})
    
    try:
    
    # Create chat message
        chat_message = ChatMessage(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            product_id=int(product_id) if product_id else None,
            message=message,
            message_type=message_type,
            offer_price=float(offer_price) if offer_price else None,
            offer_quantity=int(offer_quantity)
        )
        
        # Generate conversation ID
        chat_message.conversation_id = chat_message.generate_conversation_id()
        
        # Set expiration for offers (24 hours)
        if message_type in ['offer', 'deal']:
            from datetime import timedelta
            chat_message.expires_at = datetime.utcnow() + timedelta(hours=24)
        
        db.session.add(chat_message)
        
        # Update or create conversation
        conversation = ChatConversation.query.filter_by(
            conversation_id=chat_message.conversation_id
        ).first()
        
        if not conversation:
            # Determine seller and buyer
            if product_id:
                product = Product.query.get(int(product_id))
                if product:
                    seller_id = product.owner_id
                    buyer_id = current_user.id if current_user.id != seller_id else receiver_id
                else:
                    seller_id = receiver_id
                    buyer_id = current_user.id
            else:
                # For general chat, determine roles based on user_role
                if current_user.user_role == 'seller':
                    seller_id = current_user.id
                    buyer_id = receiver_id
                else:
                    seller_id = receiver_id
                    buyer_id = current_user.id
            
            conversation = ChatConversation(
                conversation_id=chat_message.conversation_id,
                seller_id=seller_id,
                buyer_id=buyer_id,
                product_id=int(product_id) if product_id else None
            )
            db.session.add(conversation)
        
        # Update conversation
        conversation.last_message_at = datetime.utcnow()
        conversation.last_message_by = current_user.id
        
        if message_type == 'offer':
            conversation.status = 'negotiating'
            conversation.current_offer_price = float(offer_price) if offer_price else None
            conversation.current_offer_by = current_user.id
        elif message_type == 'deal':
            conversation.status = 'deal_pending'
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Pesan berhasil dikirim',
            'conversation_id': chat_message.conversation_id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Gagal mengirim pesan: {str(e)}'})

@app.route('/get_chat_messages/<conversation_id>')
@login_required
def get_chat_messages(conversation_id):
    from models import ChatMessage, ChatConversation
    
    # Verify user is part of this conversation
    conversation = ChatConversation.query.filter_by(conversation_id=conversation_id).first()
    if not conversation or (conversation.seller_id != current_user.id and conversation.buyer_id != current_user.id):
        return jsonify({'error': 'Akses ditolak'}), 403
    
    # Get messages for this conversation
    messages = ChatMessage.query.filter_by(
        conversation_id=conversation_id
    ).order_by(ChatMessage.created_at.asc()).all()
    
    # Mark messages as read
    ChatMessage.query.filter_by(
        conversation_id=conversation_id,
        receiver_id=current_user.id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()
    
    message_data = []
    for msg in messages:
        message_data.append({
            'id': msg.id,
            'sender_id': msg.sender_id,
            'sender_name': msg.sender.get_full_name(),
            'message': msg.message,
            'message_type': msg.message_type,
            'offer_price': msg.offer_price,
            'offer_quantity': msg.offer_quantity,
            'is_deal': msg.is_deal,
            'deal_accepted': msg.deal_accepted,
            'expires_at': msg.expires_at.strftime('%Y-%m-%d %H:%M') if msg.expires_at else None,
            'is_expired': msg.is_expired(),
            'created_at': msg.created_at.strftime('%H:%M'),
            'product_title': msg.product.title if msg.product else None,
            'product_id': msg.product_id
        })
    
    return jsonify({
        'messages': message_data,
        'conversation': {
            'id': conversation.conversation_id,
            'status': conversation.status,
            'current_offer_price': conversation.current_offer_price,
            'deal_finalized': conversation.deal_finalized,
            'product_title': conversation.product.title if conversation.product else None
        }
    })

@app.route('/chat_with_seller/<int:seller_id>')
@login_required
def chat_with_seller(seller_id):
    from models import ChatConversation
    
    seller = User.query.get_or_404(seller_id)
    product_id = request.args.get('product_id')
    
    # Get seller's products for context
    seller_products = Product.query.filter_by(owner_id=seller_id, is_available=True).limit(5).all()
    
    # Get or create conversation
    if product_id:
        # Create conversation ID for product-specific chat
        participants = sorted([current_user.id, seller_id])
        conversation_id = f"conv_{participants[0]}_{participants[1]}_product_{product_id}"
        product = Product.query.get(product_id)
    else:
        # General conversation
        participants = sorted([current_user.id, seller_id])
        conversation_id = f"conv_{participants[0]}_{participants[1]}_general"
        product = None
    
    # Get existing conversation
    conversation = ChatConversation.query.filter_by(conversation_id=conversation_id).first()
    
    return render_template('chat.html', 
                         other_user=seller, 
                         products=seller_products, 
                         chat_type='seller',
                         conversation_id=conversation_id,
                         current_product=product,
                         conversation=conversation)

@app.route('/chat_with_buyer/<int:buyer_id>')
@login_required
def chat_with_buyer(buyer_id):
    from models import Cart, ChatConversation
    
    buyer = User.query.get_or_404(buyer_id)
    
    # Get buyer's recent cart items for context
    buyer_cart = Cart.query.filter_by(buyer_id=buyer_id).limit(5).all()
    
    # Create general conversation ID
    participants = sorted([current_user.id, buyer_id])
    conversation_id = f"conv_{participants[0]}_{participants[1]}_general"
    
    # Get existing conversation
    conversation = ChatConversation.query.filter_by(conversation_id=conversation_id).first()
    
    return render_template('chat.html', 
                         other_user=buyer, 
                         cart_items=buyer_cart, 
                         chat_type='buyer',
                         conversation_id=conversation_id,
                         conversation=conversation)

@app.route('/my_conversations')
@login_required
def my_conversations():
    from models import ChatConversation
    
    # Get all conversations for current user
    conversations = ChatConversation.query.filter(
        (ChatConversation.seller_id == current_user.id) | 
        (ChatConversation.buyer_id == current_user.id)
    ).order_by(ChatConversation.last_message_at.desc()).all()
    
    # Add unread count for each conversation
    for conv in conversations:
        conv.unread_count = conv.get_unread_count_for_user(current_user.id)
    
    return render_template('conversations.html', conversations=conversations)

@app.route('/get_unread_chat_count')
@login_required
def get_unread_chat_count():
    from models import ChatMessage
    
    unread_count = ChatMessage.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    return jsonify({'unread_count': unread_count})

@app.route('/checkout_seller/<int:seller_id>')
@login_required
def checkout_seller(seller_id):
    from models import Cart
    
    # Get cart items for specific seller
    cart_items = Cart.query.filter_by(buyer_id=current_user.id).join(Product).filter(Product.owner_id == seller_id).all()
    
    if not cart_items:
        flash('Tidak ada item dari penjual ini di keranjang Anda.', 'error')
        return redirect(url_for('view_cart'))
    
    seller = User.query.get_or_404(seller_id)
    total_value = sum(item.product.get_final_barter_value() for item in cart_items)
    
    return render_template('checkout_seller.html', 
                         cart_items=cart_items, 
                         seller=seller, 
                         total_value=total_value)

@app.route('/process_checkout_seller/<int:seller_id>', methods=['POST'])
@login_required
def process_checkout_seller(seller_id):
    from models import Cart, TransactionReceipt
    
    # Get cart items for specific seller
    cart_items = Cart.query.filter_by(buyer_id=current_user.id).join(Product).filter(Product.owner_id == seller_id).all()
    
    if not cart_items:
        flash('Tidak ada item dari penjual ini di keranjang Anda.', 'error')
        return redirect(url_for('view_cart'))
    
    # Get form data
    payment_method = request.form.get('payment_method')
    cash_amount = request.form.get('cash_amount', 0)
    message = request.form.get('message', '')
    topup_commitment = request.form.get('topup_commitment')
    
    seller = User.query.get_or_404(seller_id)
    
    # Calculate totals
    total_points = sum(item.product.get_final_barter_value() for item in cart_items)
    total_estimated_value = sum(item.product.estimated_value or 0 for item in cart_items)
    
    # Create transaction receipt directly (skip proposal step)
    receipt = TransactionReceipt(
        proposal_id=None,  # Topup system doesn't use proposals
        seller_name=seller.get_full_name(),
        buyer_name=current_user.get_full_name(),
        seller_email=seller.email,
        buyer_email=current_user.email,
        main_item_offered='Topup System - ' + ('Barang Sesuai Permintaan' if payment_method == 'topup_item' else 'Pembayaran Tunai'),
        main_item_wanted=', '.join([item.product.title for item in cart_items]),
        offered_product_title='Sistem Topup',
        offered_product_condition='Sesuai Kesepakatan',
        wanted_product_title=f'{len(cart_items)} item dari {seller.get_full_name()}',
        wanted_product_condition='Campuran',
        final_agreed_price=float(cash_amount) if cash_amount else total_estimated_value,
        exchange_terms=f"Total {total_points} poin. " + message,
        payment_method='Topup Barang' if payment_method == 'topup_item' else 'Tunai',
        transaction_status='topup_pending',
        additional_items_detail=message,
        is_permanent=True
    )
    
    # Generate receipt number
    receipt.generate_receipt_number()
    db.session.add(receipt)
    
    # Store detailed topup requirements in exchange_terms
    topup_details = []
    for item in cart_items:
        detail = f"• {item.product.title} ({item.product.get_final_barter_value()} pts)"
        if item.product.exchange_preference:
            detail += f" - Penjual ingin: {item.product.exchange_preference}"
        topup_details.append(detail)
    
    receipt.exchange_terms = f"TOPUP REQUIREMENTS:\n" + "\n".join(topup_details) + f"\n\nPesan: {message}"
    
    # Clear cart items
    for cart_item in cart_items:
        db.session.delete(cart_item)
    
    db.session.commit()
    
    # Send notification to seller via chat system
    from models import ChatMessage, ChatConversation
    participants = sorted([current_user.id, seller_id])
    conversation_id = f"conv_{participants[0]}_{participants[1]}_checkout_{receipt.id}"
    
    # Create conversation
    conversation = ChatConversation(
        conversation_id=conversation_id,
        seller_id=seller_id,
        buyer_id=current_user.id,
        product_id=cart_items[0].product_id if cart_items else None,
        status='deal_pending'
    )
    db.session.add(conversation)
    
    # Send deal message
    deal_message = f"🛒 CHECKOUT DEAL - Receipt #{receipt.receipt_number}\n\n"
    deal_message += f"📦 Item: {len(cart_items)} produk (Total: {total_points} poin)\n"
    deal_message += f"💰 Metode: {receipt.payment_method}\n"
    if payment_method == 'topup_item':
        deal_message += f"📋 Komitmen: Pembeli akan menyediakan barang sesuai permintaan dalam 7 hari\n"
    else:
        deal_message += f"💵 Jumlah: Rp {cash_amount:,.0f}\n"
    deal_message += f"\n📝 Catatan: {message}\n\n"
    deal_message += "✅ Setuju dengan deal ini? Konfirmasi untuk melanjutkan."
    
    chat_msg = ChatMessage(
        sender_id=current_user.id,
        receiver_id=seller_id,
        product_id=cart_items[0].product_id if cart_items else None,
        conversation_id=conversation_id,
        message=deal_message,
        message_type='deal',
        offer_price=float(cash_amount) if cash_amount else total_estimated_value,
        is_deal=True
    )
    
    # Set expiration (72 hours for checkout deals)
    from datetime import timedelta
    chat_msg.expires_at = datetime.utcnow() + timedelta(hours=72)
    
    db.session.add(chat_msg)
    db.session.commit()
    
    flash(f'Deal checkout berhasil dibuat! Receipt #{receipt.receipt_number} telah dikirim ke {seller.get_full_name()}. Silakan lengkapi detail barang topup.', 'success')
    
    # If topup method, redirect to detail form
    if payment_method == 'topup_item':
        return redirect(url_for('topup_item_form', receipt_id=receipt.id))
    else:
        return redirect(url_for('transaction_receipt', receipt_id=receipt.id))

@app.route('/respond_to_offer', methods=['POST'])
@login_required
def respond_to_offer():
    from models import ChatMessage, ChatConversation
    
    message_id = request.form['message_id']
    action = request.form['action']  # accept, reject, counter
    counter_price = request.form.get('counter_price')
    response_message = request.form.get('response_message', '')
    
    original_message = ChatMessage.query.get_or_404(message_id)
    
    # Verify user can respond to this offer
    if original_message.receiver_id != current_user.id:
        return jsonify({'success': False, 'error': 'Akses ditolak'})
    
    conversation = ChatConversation.query.filter_by(
        conversation_id=original_message.conversation_id
    ).first()
    
    if action == 'accept':
        # Accept the offer
        original_message.deal_accepted = True
        original_message.deal_accepted_at = datetime.utcnow()
        
        # Update conversation
        conversation.status = 'completed'
        conversation.deal_finalized = True
        conversation.deal_price = original_message.offer_price
        
        # Send confirmation message
        confirmation_msg = ChatMessage(
            sender_id=current_user.id,
            receiver_id=original_message.sender_id,
            product_id=original_message.product_id,
            conversation_id=original_message.conversation_id,
            message=f"✅ Deal diterima! Harga: Rp {original_message.offer_price:,.0f}. {response_message}",
            message_type='deal'
        )
        db.session.add(confirmation_msg)
        
    elif action == 'reject':
        # Reject the offer
        original_message.deal_accepted = False
        original_message.deal_accepted_at = datetime.utcnow()
        
        conversation.status = 'active'
        
        # Send rejection message
        rejection_msg = ChatMessage(
            sender_id=current_user.id,
            receiver_id=original_message.sender_id,
            product_id=original_message.product_id,
            conversation_id=original_message.conversation_id,
            message=f"❌ Penawaran ditolak. {response_message}",
            message_type='text'
        )
        db.session.add(rejection_msg)
        
    elif action == 'counter' and counter_price:
        # Make counter offer
        counter_msg = ChatMessage(
            sender_id=current_user.id,
            receiver_id=original_message.sender_id,
            product_id=original_message.product_id,
            conversation_id=original_message.conversation_id,
            message=f"🔄 Counter offer: Rp {float(counter_price):,.0f}. {response_message}",
            message_type='offer',
            offer_price=float(counter_price),
            offer_quantity=original_message.offer_quantity
        )
        
        # Set expiration
        from datetime import timedelta
        counter_msg.expires_at = datetime.utcnow() + timedelta(hours=24)
        
        db.session.add(counter_msg)
        
        # Update conversation
        conversation.current_offer_price = float(counter_price)
        conversation.current_offer_by = current_user.id
    
    # Update conversation
    conversation.last_message_at = datetime.utcnow()
    conversation.last_message_by = current_user.id
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Respons berhasil dikirim'})

@app.route('/finalize_deal', methods=['POST'])
@login_required
def finalize_deal():
    from models import ChatMessage, ChatConversation, TransactionReceipt
    
    conversation_id = request.form['conversation_id']
    final_price = request.form['final_price']
    quantity = request.form.get('quantity', 1)
    payment_method = request.form.get('payment_method', 'transfer')
    shipping_address = request.form.get('shipping_address', '')
    shipping_service = request.form.get('shipping_service', 'jne')
    shipping_cost = request.form.get('shipping_cost', 0)
    notes = request.form.get('notes', '')
    
    conversation = ChatConversation.query.filter_by(conversation_id=conversation_id).first()
    
    if not conversation or (conversation.seller_id != current_user.id and conversation.buyer_id != current_user.id):
        return jsonify({'success': False, 'error': 'Akses ditolak'})
    
    # Update conversation status to pending deal (waiting for other party confirmation)
    conversation.status = 'deal_pending'
    conversation.current_offer_price = float(final_price)
    conversation.current_offer_by = current_user.id
    
    # Send deal proposal message
    deal_msg = ChatMessage(
        sender_id=current_user.id,
        receiver_id=conversation.seller_id if current_user.id == conversation.buyer_id else conversation.buyer_id,
        product_id=conversation.product_id,
        conversation_id=conversation_id,
        message=f"🤝 Proposal Deal:\n💰 Harga: Rp {float(final_price):,.0f}\n📦 Jumlah: {quantity}\n💳 Pembayaran: {payment_method.title()}\n🚚 Jasa Kirim: {shipping_service.upper()}\n📍 Alamat: {shipping_address[:50]}{'...' if len(shipping_address) > 50 else ''}\n\n{notes}",
        message_type='deal',
        offer_price=float(final_price),
        offer_quantity=int(quantity),
        is_deal=True
    )
    
    # Set expiration for deal (48 hours)
    from datetime import timedelta
    deal_msg.expires_at = datetime.utcnow() + timedelta(hours=48)
    
    db.session.add(deal_msg)
    
    conversation.last_message_at = datetime.utcnow()
    conversation.last_message_by = current_user.id
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Proposal deal berhasil dikirim! Menunggu konfirmasi dari pihak lain.',
        'deal_message_id': deal_msg.id
    })

@app.route('/confirm_deal', methods=['POST'])
@login_required
def confirm_deal():
    """Confirm a deal proposal and create transaction receipt"""
    from models import ChatMessage, ChatConversation, TransactionReceipt
    
    message_id = request.form['message_id']
    action = request.form['action']  # accept or reject
    
    deal_message = ChatMessage.query.get_or_404(message_id)
    
    if deal_message.receiver_id != current_user.id:
        return jsonify({'success': False, 'error': 'Akses ditolak'})
    
    conversation = ChatConversation.query.filter_by(
        conversation_id=deal_message.conversation_id
    ).first()
    
    if action == 'accept':
        # Accept the deal
        deal_message.deal_accepted = True
        deal_message.deal_accepted_at = datetime.utcnow()
        
        # Update conversation
        conversation.status = 'completed'
        conversation.deal_finalized = True
        conversation.deal_price = deal_message.offer_price
        
        # Create transaction receipt with permanent storage
        receipt = TransactionReceipt(
            proposal_id=None,  # Chat-based deal
            seller_name=conversation.seller.get_full_name(),
            buyer_name=conversation.buyer.get_full_name(),
            seller_email=conversation.seller.email,
            buyer_email=conversation.buyer.email,
            main_item_offered='Chat Deal',
            main_item_wanted=conversation.product.title if conversation.product else 'General Deal',
            offered_product_title='Chat-based offer',
            wanted_product_title=conversation.product.title if conversation.product else 'General item',
            offered_product_condition='As discussed',
            wanted_product_condition=conversation.product.condition if conversation.product else 'As described',
            final_agreed_price=deal_message.offer_price,
            shipping_cost=0,  # Will be calculated later
            shipping_method='To be determined',
            shipping_address='To be confirmed',
            exchange_terms=f"Chat deal for {conversation.product.title if conversation.product else 'general item'}",
            payment_method='Barter + Cash',
            currency_type='IDR',
            transaction_status='deal_confirmed',
            is_permanent=True
        )
        receipt.generate_receipt_number()
        db.session.add(receipt)
        
        # Send confirmation message
        confirmation_msg = ChatMessage(
            sender_id=current_user.id,
            receiver_id=deal_message.sender_id,
            product_id=deal_message.product_id,
            conversation_id=deal_message.conversation_id,
            message=f"✅ Deal DITERIMA! 🎉\n\n💰 Harga Final: Rp {deal_message.offer_price:,.0f}\n📋 Receipt Number: {receipt.receipt_number}\n\n🚀 Langkah selanjutnya:\n1. Konfirmasi detail pengiriman\n2. Proses pembayaran\n3. Pengiriman barang\n\nTerima kasih atas kesepakatan ini!",
            message_type='deal'
        )
        db.session.add(confirmation_msg)
        
        success_message = 'Deal berhasil diterima! Transaction receipt telah dibuat.'
        
    elif action == 'reject':
        # Reject the deal
        deal_message.deal_accepted = False
        deal_message.deal_accepted_at = datetime.utcnow()
        
        conversation.status = 'active'
        
        # Send rejection message
        rejection_msg = ChatMessage(
            sender_id=current_user.id,
            receiver_id=deal_message.sender_id,
            product_id=deal_message.product_id,
            conversation_id=deal_message.conversation_id,
            message=f"❌ Deal DITOLAK\n\nMaaf, saya tidak bisa menerima deal ini saat ini. Mari kita lanjutkan negosiasi atau buat penawaran baru.\n\nTerima kasih atas pengertiannya.",
            message_type='text'
        )
        db.session.add(rejection_msg)
        
        success_message = 'Deal berhasil ditolak. Percakapan kembali aktif.'
    
    # Update conversation
    conversation.last_message_at = datetime.utcnow()
    conversation.last_message_by = current_user.id
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': success_message})

@app.route('/confirm_order/<int:receipt_id>', methods=['POST'])
@login_required
def confirm_order():
    """Seller confirms the order and prepares for shipping"""
    receipt_id = request.form['receipt_id']
    estimated_shipping_days = request.form.get('estimated_shipping_days', 3)
    seller_notes = request.form.get('seller_notes', '')
    
    receipt = TransactionReceipt.query.get_or_404(receipt_id)
    
    # Verify seller ownership through product or direct receipt
    if hasattr(receipt, 'proposal') and receipt.proposal:
        seller_id = receipt.proposal.wanted_product.owner_id
    else:
        # For chat-based deals, find through conversation
        conversation = ChatConversation.query.filter_by(
            product_id=receipt.main_item_wanted
        ).first()
        seller_id = conversation.seller_id if conversation else None
    
    if not seller_id or seller_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    # Update receipt status
    receipt.transaction_status = 'confirmed_by_seller'
    receipt.additional_items_detail = seller_notes
    
    # Calculate estimated delivery date
    estimated_delivery = datetime.utcnow() + timedelta(days=int(estimated_shipping_days))
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Pesanan berhasil dikonfirmasi!',
        'estimated_delivery': estimated_delivery.strftime('%Y-%m-%d')
    })

@app.route('/ship_order/<int:receipt_id>', methods=['POST'])
@login_required
def ship_order():
    """Seller ships the order and provides tracking"""
    receipt_id = request.form['receipt_id']
    tracking_number = request.form['tracking_number']
    actual_shipping_cost = request.form.get('actual_shipping_cost')
    shipping_notes = request.form.get('shipping_notes', '')
    
    receipt = TransactionReceipt.query.get_or_404(receipt_id)
    
    # Verify seller ownership
    if hasattr(receipt, 'proposal') and receipt.proposal:
        seller_id = receipt.proposal.wanted_product.owner_id
    else:
        conversation = ChatConversation.query.filter_by(
            product_id=receipt.main_item_wanted
        ).first()
        seller_id = conversation.seller_id if conversation else None
    
    if not seller_id or seller_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    # Update receipt with shipping info
    receipt.tracking_number = tracking_number
    receipt.transaction_status = 'shipped'
    if actual_shipping_cost:
        receipt.shipping_cost = float(actual_shipping_cost)
    if shipping_notes:
        receipt.additional_items_detail += f"\n\nCatatan Pengiriman: {shipping_notes}"
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Pesanan berhasil dikirim!',
        'tracking_number': tracking_number
    })

@app.route('/get_shipping_rates', methods=['POST'])
@login_required
def get_shipping_rates():
    """Get shipping rates for different couriers"""
    origin_city = request.form.get('origin_city', 'Jakarta')
    destination_city = request.form.get('destination_city')
    weight = float(request.form.get('weight', 1))  # in kg
    
    # Simulate shipping rates (in real app, integrate with courier APIs)
    shipping_rates = {
        'JNE': {
            'REG': {'price': int(weight * 15000), 'days': '2-3', 'service': 'JNE REG'},
            'OKE': {'price': int(weight * 12000), 'days': '3-4', 'service': 'JNE OKE'},
            'YES': {'price': int(weight * 25000), 'days': '1-2', 'service': 'JNE YES'}
        },
        'TIKI': {
            'REG': {'price': int(weight * 14000), 'days': '2-3', 'service': 'TIKI REG'},
            'ONS': {'price': int(weight * 22000), 'days': '1', 'service': 'TIKI ONS'}
        },
        'POS': {
            'REG': {'price': int(weight * 13000), 'days': '3-4', 'service': 'POS REG'},
            'NEXTDAY': {'price': int(weight * 20000), 'days': '1', 'service': 'POS NEXTDAY'}
        },
        'J&T': {
            'REG': {'price': int(weight * 11000), 'days': '2-4', 'service': 'J&T REG'},
            'EXPRESS': {'price': int(weight * 18000), 'days': '1-2', 'service': 'J&T EXPRESS'}
        }
    }
    
    return jsonify({
        'success': True,
        'rates': shipping_rates,
        'origin': origin_city,
        'destination': destination_city,
        'weight': weight
    })

@app.route('/seller_orders')
@login_required
def seller_orders():
    """Display seller's orders and shipping management"""
    # Get receipts where current user is the seller
    orders = []
    
    # From barter proposals
    proposals = BarterProposal.query.filter_by(receiver_id=current_user.id, status='accepted').all()
    for proposal in proposals:
        if hasattr(proposal, 'receipt') and proposal.receipt:
            orders.append({
                'receipt': proposal.receipt,
                'type': 'barter',
                'product': proposal.wanted_product,
                'customer': proposal.proposer
            })
    
    # From chat deals
    conversations = ChatConversation.query.filter_by(
        seller_id=current_user.id, 
        deal_finalized=True
    ).all()
    
    for conv in conversations:
        # Find receipt for this conversation
        receipt = TransactionReceipt.query.filter(
            TransactionReceipt.main_item_wanted.contains(conv.product.title)
        ).first()
        
        if receipt:
            orders.append({
                'receipt': receipt,
                'type': 'chat_deal',
                'product': conv.product,
                'customer': conv.buyer
            })
    
    return render_template('seller_orders.html', orders=orders)

@app.route('/topup_guide')
def topup_guide():
    return render_template('topup_instructions.html')

@app.route('/topup_item_form/<int:receipt_id>')
@login_required
def topup_item_form(receipt_id):
    """Form untuk mengisi detail barang topup"""
    from models import TransactionReceipt
    
    receipt = TransactionReceipt.query.get_or_404(receipt_id)
    
    # Verify this is buyer's receipt
    if receipt.buyer_email != current_user.email:
        flash('Akses ditolak.', 'error')
        return redirect(url_for('dashboard'))
    
    from datetime import date
    today = date.today().isoformat()
    
    return render_template('topup_item_form.html', receipt=receipt, today=today)

@app.route('/submit_topup_item/<int:receipt_id>', methods=['POST'])
@login_required
def submit_topup_item(receipt_id):
    """Submit detailed topup item information"""
    from models import TransactionReceipt, TopupItem, TopupItemImage
    
    receipt = TransactionReceipt.query.get_or_404(receipt_id)
    
    # Verify this is buyer's receipt
    if receipt.buyer_email != current_user.email:
        flash('Akses ditolak.', 'error')
        return redirect(url_for('dashboard'))
    
    # Create TopupItem
    topup_item = TopupItem(
        receipt_id=receipt.id,
        buyer_id=current_user.id,
        item_title=request.form['item_title'],
        item_description=request.form['item_description'],
        item_condition=request.form['item_condition'],
        estimated_value=float(request.form['estimated_value']),
        brand=request.form.get('brand'),
        model=request.form.get('model'),
        year_purchased=int(request.form['year_purchased']) if request.form.get('year_purchased') else None,
        original_price=float(request.form['original_price']) if request.form.get('original_price') else None,
        physical_condition_notes=request.form.get('physical_condition_notes'),
        functional_condition_notes=request.form.get('functional_condition_notes'),
        defects_or_issues=request.form.get('defects_or_issues'),
        additional_accessories=request.form.get('additional_accessories'),
        delivery_method=request.form['delivery_method']
    )
    
    # Parse delivery date
    delivery_date_str = request.form.get('estimated_delivery_date')
    if delivery_date_str:
        from datetime import datetime
        topup_item.estimated_delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d')
    
    db.session.add(topup_item)
    db.session.flush()  # Get the ID
    
    # Handle file uploads
    file_types = [
        ('main_images', 'main'),
        ('detail_images', 'detail'), 
        ('condition_images', 'condition'),
        ('accessory_images', 'accessory'),
        ('purchase_proof', 'proof'),
        ('authenticity_proof', 'proof')
    ]
    
    for file_key, image_type in file_types:
        files = request.files.getlist(file_key)
        for i, file in enumerate(files):
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                
                # Determine description based on file type
                if file_key == 'purchase_proof':
                    description = 'Bukti pembelian / invoice'
                elif file_key == 'authenticity_proof':
                    description = 'Bukti keaslian / garansi'
                else:
                    description = f'{image_type.title()} image {i+1}'
                
                topup_image = TopupItemImage(
                    topup_item_id=topup_item.id,
                    image_filename=unique_filename,
                    image_type=image_type,
                    description=description,
                    is_primary=(image_type == 'main' and i == 0)
                )
                db.session.add(topup_image)
    
    # Update receipt status
    receipt.transaction_status = 'topup_details_submitted'
    
    db.session.commit()
    
    # Notify seller via chat
    from models import ChatMessage, ChatConversation, User
    
    # Find seller from receipt
    seller = User.query.filter_by(email=receipt.seller_email).first()
    if seller:
        # Create notification message
        notification_msg = f"""
🎯 DETAIL BARANG TOPUP DITERIMA

📦 **{topup_item.item_title}**
🏷️ Merek: {topup_item.brand or 'N/A'}
💎 Kondisi: {topup_item.item_condition}
💰 Estimasi Nilai: Rp {topup_item.estimated_value:,.0f}

📝 **Deskripsi:**
{topup_item.item_description[:200]}{'...' if len(topup_item.item_description) > 200 else ''}

📸 **Foto:** {len(topup_item.images)} foto tersedia
🚚 **Pengiriman:** {topup_item.delivery_method}
📅 **Estimasi Kirim:** {topup_item.estimated_delivery_date.strftime('%d %B %Y') if topup_item.estimated_delivery_date else 'TBD'}

✅ Silakan review detail lengkap dan berikan persetujuan.
"""
        
        chat_msg = ChatMessage(
            sender_id=current_user.id,
            receiver_id=seller.id,
            message=notification_msg,
            message_type='topup_details'
        )
        db.session.add(chat_msg)
        db.session.commit()
    
    flash(f'Detail barang "{topup_item.item_title}" berhasil dikirim! Menunggu persetujuan penjual.', 'success')
    return redirect(url_for('topup_item_detail', item_id=topup_item.id))

@app.route('/topup_item_detail/<int:item_id>')
@login_required
def topup_item_detail(item_id):
    """View detailed topup item information"""
    from models import TopupItem
    
    topup_item = TopupItem.query.get_or_404(item_id)
    
    # Check access rights
    is_buyer = topup_item.buyer_id == current_user.id
    is_seller = topup_item.receipt.seller_email == current_user.email
    
    if not (is_buyer or is_seller):
        flash('Akses ditolak.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('topup_item_detail.html', 
                         topup_item=topup_item, 
                         is_buyer=is_buyer, 
                         is_seller=is_seller)

@app.route('/approve_topup_item/<int:item_id>', methods=['POST'])
@login_required
def approve_topup_item(item_id):
    """Seller approves or rejects topup item"""
    from models import TopupItem, ChatMessage, User
    
    topup_item = TopupItem.query.get_or_404(item_id)
    
    # Verify seller access
    if topup_item.receipt.seller_email != current_user.email:
        flash('Akses ditolak.', 'error')
        return redirect(url_for('dashboard'))
    
    action = request.form['action']  # approve or reject
    feedback = request.form.get('feedback', '')
    
    if action == 'approve':
        topup_item.seller_approval = True
        topup_item.status = 'approved'
        topup_item.receipt.transaction_status = 'topup_approved'
        
        notification = f"✅ **BARANG TOPUP DISETUJUI**\n\n🎉 Selamat! Barang '{topup_item.item_title}' telah disetujui oleh penjual.\n\n📝 Catatan penjual: {feedback}\n\n🚀 Silakan kirim barang sesuai jadwal yang telah ditentukan."
        
    else:  # reject
        topup_item.seller_approval = False
        topup_item.status = 'rejected'
        topup_item.receipt.transaction_status = 'topup_rejected'
        
        notification = f"❌ **BARANG TOPUP DITOLAK**\n\n😔 Maaf, barang '{topup_item.item_title}' ditolak oleh penjual.\n\n📝 Alasan: {feedback}\n\n🔄 Silakan submit ulang dengan barang yang lebih sesuai atau diskusikan alternatif lain."
    
    topup_item.seller_feedback = feedback
    
    # Send notification to buyer
    buyer = topup_item.buyer
    chat_msg = ChatMessage(
        sender_id=current_user.id,
        receiver_id=buyer.id,
        message=notification,
        message_type='approval_result'
    )
    
    db.session.add(chat_msg)
    db.session.commit()
    
    status_text = 'disetujui' if action == 'approve' else 'ditolak'
    flash(f'Barang topup berhasil {status_text}!', 'success')
    
    return redirect(url_for('topup_item_detail', item_id=item_id))

@app.route('/support', methods=['GET', 'POST'])
def admin_support():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        access_code = request.form['access_code']
        
        # Kode akses khusus untuk keamanan tambahan
        ADMIN_ACCESS_CODE = "FAJARMANDIRI2025"
        
        if access_code != ADMIN_ACCESS_CODE:
            flash('Kode akses sistem tidak valid.', 'error')
            return render_template('admin_support.html')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_admin and user.active:
            login_user(user)
            flash('Login administrator berhasil!', 'success')
            return redirect(url_for('owner_dashboard'))
        else:
            flash('Kredensial administrator tidak valid atau akun tidak aktif.', 'error')

    return render_template('admin_support.html')