
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import app, db
from models import User, Product, ChatMessage, ChatConversation
from datetime import datetime, timedelta
import logging

@app.route('/chat')
@login_required
def chat_conversations():
    """Display all conversations for the current user"""
    # Get all conversations where user is either seller or buyer
    conversations = ChatConversation.query.filter(
        (ChatConversation.seller_id == current_user.id) | 
        (ChatConversation.buyer_id == current_user.id)
    ).order_by(ChatConversation.last_message_at.desc()).all()
    
    # Add unread count for each conversation
    for conv in conversations:
        conv.unread_count = conv.get_unread_count_for_user(current_user.id)
        
        # Determine the other user
        if conv.seller_id == current_user.id:
            conv.other_user = User.query.get(conv.buyer_id)
            conv.user_role = 'seller'
        else:
            conv.other_user = User.query.get(conv.seller_id)
            conv.user_role = 'buyer'
    
    return render_template('conversations.html', conversations=conversations)

@app.route('/chat/<int:user_id>')
@app.route('/chat/<int:user_id>/<int:product_id>')
@login_required
def chat_with_specific_user(user_id, product_id=None):
    """Start or continue chat with a specific user, optionally about a product"""
    other_user = User.query.get_or_404(user_id)
    
    if other_user.id == current_user.id:
        flash('Anda tidak dapat chat dengan diri sendiri', 'error')
        return redirect(url_for('chat_conversations'))
    
    # Get or create conversation
    if product_id:
        participants = sorted([current_user.id, user_id])
        conversation_id = f"conv_{participants[0]}_{participants[1]}_product_{product_id}"
        product = Product.query.get_or_404(product_id)
    else:
        participants = sorted([current_user.id, user_id])
        conversation_id = f"conv_{participants[0]}_{participants[1]}_general"
        product = None
    
    conversation = ChatConversation.query.filter_by(conversation_id=conversation_id).first()
    if not conversation:
        # Determine roles
        if product and product.owner_id == current_user.id:
            seller_id, buyer_id = current_user.id, user_id
            chat_type = 'seller'
        elif product and product.owner_id == user_id:
            seller_id, buyer_id = user_id, current_user.id
            chat_type = 'buyer'
        else:
            # General chat - assign based on user roles
            if current_user.user_role == 'seller':
                seller_id, buyer_id = current_user.id, user_id
                chat_type = 'seller'
            else:
                seller_id, buyer_id = user_id, current_user.id
                chat_type = 'buyer'
        
        conversation = ChatConversation(
            conversation_id=conversation_id,
            seller_id=seller_id,
            buyer_id=buyer_id,
            product_id=product_id,
            status='active'
        )
        db.session.add(conversation)
        db.session.commit()
    else:
        # Determine user role in existing conversation
        if conversation.seller_id == current_user.id:
            chat_type = 'seller'
        else:
            chat_type = 'buyer'
    
    return render_template('chat.html', 
                         other_user=other_user,
                         current_product=product,
                         conversation=conversation,
                         conversation_id=conversation_id,
                         chat_type=chat_type)

@app.route('/send_chat_message', methods=['POST'])
@login_required
def send_chat_message():
    """Send a chat message"""
    try:
        receiver_id = request.form.get('receiver_id')
        product_id = request.form.get('product_id')
        message_text = request.form.get('message', '').strip()
        message_type = request.form.get('message_type', 'text')
        offer_price = request.form.get('offer_price')
        offer_quantity = request.form.get('offer_quantity', 1)
        
        if not message_text:
            return jsonify({'success': False, 'error': 'Message cannot be empty'})
        
        if not receiver_id:
            return jsonify({'success': False, 'error': 'Receiver ID required'})
        
        # Verify receiver exists
        receiver = User.query.get(receiver_id)
        if not receiver:
            return jsonify({'success': False, 'error': 'Receiver not found'})
        
        # Generate conversation ID
        if product_id and product_id != '':
            participants = sorted([current_user.id, int(receiver_id)])
            conversation_id = f"conv_{participants[0]}_{participants[1]}_product_{product_id}"
        else:
            participants = sorted([current_user.id, int(receiver_id)])
            conversation_id = f"conv_{participants[0]}_{participants[1]}_general"
        
        # Create or update conversation
        conversation = ChatConversation.query.filter_by(conversation_id=conversation_id).first()
        if not conversation:
            # Determine roles for new conversation
            if product_id:
                product = Product.query.get(product_id)
                if product and product.owner_id == current_user.id:
                    seller_id, buyer_id = current_user.id, int(receiver_id)
                else:
                    seller_id, buyer_id = int(receiver_id), current_user.id
            else:
                # General chat
                if current_user.user_role == 'seller':
                    seller_id, buyer_id = current_user.id, int(receiver_id)
                else:
                    seller_id, buyer_id = int(receiver_id), current_user.id
            
            conversation = ChatConversation(
                conversation_id=conversation_id,
                seller_id=seller_id,
                buyer_id=buyer_id,
                product_id=int(product_id) if product_id and product_id != '' else None,
                status='active'
            )
            db.session.add(conversation)
        
        # Update conversation
        conversation.last_message_at = datetime.utcnow()
        conversation.last_message_by = current_user.id
        
        # Set expiration for offers
        expires_at = None
        if message_type == 'offer':
            expires_at = datetime.utcnow() + timedelta(hours=24)
        
        # Create chat message
        chat_message = ChatMessage(
            sender_id=current_user.id,
            receiver_id=int(receiver_id),
            product_id=int(product_id) if product_id and product_id != '' else None,
            message=message_text,
            message_type=message_type,
            offer_price=float(offer_price) if offer_price else None,
            offer_quantity=int(offer_quantity) if offer_quantity else 1,
            expires_at=expires_at,
            conversation_id=conversation_id
        )
        
        db.session.add(chat_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message_id': chat_message.id,
            'conversation_id': conversation_id
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error sending message: {str(e)}')
        return jsonify({'success': False, 'error': 'Failed to send message'})

@app.route('/get_chat_messages/<conversation_id>')
@login_required
def get_chat_messages(conversation_id):
    """Get all messages for a conversation"""
    try:
        # Verify user access to conversation
        conversation = ChatConversation.query.filter_by(conversation_id=conversation_id).first()
        if not conversation or (conversation.seller_id != current_user.id and conversation.buyer_id != current_user.id):
            return jsonify({'success': False, 'error': 'Access denied'})
        
        # Get messages
        messages = ChatMessage.query.filter_by(conversation_id=conversation_id)\
                                  .order_by(ChatMessage.created_at.asc()).all()
        
        # Mark messages as read
        unread_messages = ChatMessage.query.filter_by(
            conversation_id=conversation_id,
            receiver_id=current_user.id,
            is_read=False
        ).all()
        
        for msg in unread_messages:
            msg.is_read = True
        
        db.session.commit()
        
        # Format messages for response
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                'id': msg.id,
                'sender_id': msg.sender_id,
                'sender_name': msg.sender.get_full_name(),
                'receiver_id': msg.receiver_id,
                'message': msg.message,
                'message_type': msg.message_type,
                'offer_price': msg.offer_price,
                'offer_quantity': msg.offer_quantity,
                'is_deal': msg.is_deal,
                'deal_accepted': msg.deal_accepted,
                'created_at': msg.created_at.strftime('%H:%M'),
                'created_at_full': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'is_expired': msg.is_expired() if msg.expires_at else False,
                'expires_at': msg.expires_at.strftime('%d/%m/%Y %H:%M') if msg.expires_at else None
            })
        
        return jsonify({
            'success': True,
            'messages': formatted_messages,
            'conversation': {
                'id': conversation.conversation_id,
                'status': conversation.status,
                'last_message_at': conversation.last_message_at.isoformat() if conversation.last_message_at else None
            }
        })
        
    except Exception as e:
        logging.error(f'Error getting messages: {str(e)}')
        return jsonify({'success': False, 'error': 'Failed to get messages'})

@app.route('/respond_to_offer', methods=['POST'])
@login_required
def respond_to_offer():
    """Respond to an offer (accept/reject/counter)"""
    try:
        message_id = request.form.get('message_id')
        action = request.form.get('action')  # accept, reject, counter
        counter_price = request.form.get('counter_price')
        
        if not message_id or not action:
            return jsonify({'success': False, 'error': 'Message ID and action required'})
        
        # Get the offer message
        offer_message = ChatMessage.query.get(message_id)
        if not offer_message or offer_message.receiver_id != current_user.id:
            return jsonify({'success': False, 'error': 'Offer not found or access denied'})
        
        if offer_message.message_type != 'offer':
            return jsonify({'success': False, 'error': 'This is not an offer message'})
        
        # Check if expired
        if offer_message.expires_at and offer_message.expires_at < datetime.utcnow():
            return jsonify({'success': False, 'error': 'This offer has expired'})
        
        if action == 'accept':
            # Accept the offer
            offer_message.deal_accepted = True
            offer_message.deal_accepted_at = datetime.utcnow()
            
            # Create deal message
            deal_message = ChatMessage(
                sender_id=current_user.id,
                receiver_id=offer_message.sender_id,
                product_id=offer_message.product_id,
                message=f"Deal diterima! Harga: Rp {int(offer_message.offer_price):,}",
                message_type='deal',
                is_deal=True,
                deal_accepted=True,
                conversation_id=offer_message.conversation_id
            )
            db.session.add(deal_message)
            
            # Update conversation
            conversation = ChatConversation.query.filter_by(conversation_id=offer_message.conversation_id).first()
            if conversation:
                conversation.status = 'completed'
                conversation.deal_finalized = True
                conversation.deal_price = offer_message.offer_price
            
            message = 'Penawaran diterima!'
            
        elif action == 'reject':
            # Reject the offer
            offer_message.deal_accepted = False
            offer_message.deal_accepted_at = datetime.utcnow()
            
            # Create rejection message
            rejection_message = ChatMessage(
                sender_id=current_user.id,
                receiver_id=offer_message.sender_id,
                product_id=offer_message.product_id,
                message="Penawaran ditolak",
                message_type='text',
                conversation_id=offer_message.conversation_id
            )
            db.session.add(rejection_message)
            
            message = 'Penawaran ditolak'
            
        elif action == 'counter' and counter_price:
            # Counter offer
            counter_message = ChatMessage(
                sender_id=current_user.id,
                receiver_id=offer_message.sender_id,
                product_id=offer_message.product_id,
                message=f"Counter offer: Rp {int(float(counter_price)):,}",
                message_type='offer',
                offer_price=float(counter_price),
                offer_quantity=offer_message.offer_quantity,
                expires_at=datetime.utcnow() + timedelta(hours=24),
                conversation_id=offer_message.conversation_id
            )
            db.session.add(counter_message)
            
            # Update conversation
            conversation = ChatConversation.query.filter_by(conversation_id=offer_message.conversation_id).first()
            if conversation:
                conversation.status = 'negotiating'
                conversation.current_offer_price = float(counter_price)
                conversation.current_offer_by = current_user.id
            
            message = 'Counter offer dikirim!'
        else:
            return jsonify({'success': False, 'error': 'Invalid action'})
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': message})
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error responding to offer: {str(e)}')
        return jsonify({'success': False, 'error': 'Failed to respond to offer'})

@app.route('/get_unread_chat_count')
@login_required 
def get_unread_chat_count():
    """Get total unread chat messages count"""
    try:
        unread_count = ChatMessage.query.filter_by(
            receiver_id=current_user.id,
            is_read=False
        ).count()
        
        return jsonify({'success': True, 'unread_count': unread_count})
        
    except Exception as e:
        logging.error(f'Error getting unread count: {str(e)}')
        return jsonify({'success': False, 'unread_count': 0})

@app.route('/update_online_status', methods=['POST'])
@login_required
def update_online_status():
    """Update user online status"""
    try:
        data = request.get_json()
        status = data.get('status', 'online')
        
        current_user.is_online = (status == 'online')
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})
