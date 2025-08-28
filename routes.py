import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Product, Category, Message, BarterProposal
import uuid

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
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
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
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        user.set_password(password)
        
        # Make first user admin
        if User.query.count() == 0:
            user.is_admin = True
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Redirect to role-specific dashboard
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Check if user is more of a seller (has products) or buyer
    user_products_count = Product.query.filter_by(owner_id=current_user.id).count()
    
    if user_products_count > 0:
        return redirect(url_for('seller_dashboard'))
    else:
        return redirect(url_for('buyer_dashboard'))

@app.route('/seller_dashboard')
@login_required
def seller_dashboard():
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
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                if file.filename:
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
            seasonal_factor=seasonal_factor
        )
        
        # Calculate and set barter value
        product.update_barter_value()
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
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
        flash("You cannot propose a barter for your own product!", 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    offered_product = Product.query.get_or_404(offered_product_id)
    
    # Ensure the offered product belongs to current user
    if offered_product.owner_id != current_user.id:
        flash("You can only offer your own products!", 'error')
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
    
    flash('Barter proposal sent successfully!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))


@app.route('/messages')
@login_required
def messages():
    page = request.args.get('page', 1, type=int)
    received_messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Mark messages as read
    for message in received_messages.items:
        if not message.is_read:
            message.is_read = True
    db.session.commit()
    
    return render_template('messages.html', messages=received_messages)

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
    
    flash('Message sent successfully!', 'success')
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

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    total_users = User.query.count()
    total_products = Product.query.count()
    total_proposals = BarterProposal.query.count()
    active_products = Product.query.filter_by(is_available=True).count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
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
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users)

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
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    page = request.args.get('page', 1, type=int)
    proposals = BarterProposal.query.order_by(BarterProposal.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/transactions.html', proposals=proposals)

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
    
    return render_template('admin/messages.html', messages=messages)

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

