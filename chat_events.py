from flask_socketio import emit, join_room, leave_room, disconnect
from flask_login import current_user
from datetime import datetime, timedelta
from app import socketio, db
from models import ChatMessage, ChatConversation, User, Product
import logging

# Dictionary to track active users in rooms
active_users = {}

@socketio.on('connect')
def on_connect():
    if current_user.is_authenticated:
        # Update user online status
        current_user.is_online = True
        current_user.last_seen = datetime.utcnow()
        try:
            db.session.commit()
        except:
            db.session.rollback()
        
        logging.info(f'User {current_user.username} connected to chat')
        emit('connection_status', {'status': 'connected', 'user': current_user.username})
    else:
        disconnect()

@socketio.on('disconnect')
def on_disconnect():
    if current_user.is_authenticated:
        # Update user offline status
        current_user.is_online = False
        current_user.last_seen = datetime.utcnow()
        try:
            db.session.commit()
        except:
            db.session.rollback()
        
        # Remove from all active rooms
        user_id = str(current_user.id)
        for room_id in list(active_users.keys()):
            if user_id in active_users.get(room_id, []):
                active_users[room_id].remove(user_id)
                if not active_users[room_id]:
                    del active_users[room_id]
        
        logging.info(f'User {current_user.username} disconnected from chat')

@socketio.on('join_conversation')
def on_join_conversation(data):
    if not current_user.is_authenticated:
        return
    
    conversation_id = data.get('conversation_id')
    if not conversation_id:
        return
    
    # Verify user is part of this conversation
    conversation = ChatConversation.query.filter_by(conversation_id=conversation_id).first()
    if not conversation or (conversation.seller_id != current_user.id and conversation.buyer_id != current_user.id):
        emit('error', {'message': 'Access denied to this conversation'})
        return
    
    # Join the room
    join_room(conversation_id)
    
    # Track active users in room
    if conversation_id not in active_users:
        active_users[conversation_id] = []
    if str(current_user.id) not in active_users[conversation_id]:
        active_users[conversation_id].append(str(current_user.id))
    
    # Mark messages as read
    unread_messages = ChatMessage.query.filter_by(
        conversation_id=conversation_id,
        receiver_id=current_user.id,
        is_read=False
    ).all()
    
    for msg in unread_messages:
        msg.is_read = True
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
    
    # Notify user they joined
    emit('joined_conversation', {'conversation_id': conversation_id, 'status': 'success'})
    
    # Notify other users in room about online status
    emit('user_online', {
        'user_id': current_user.id,
        'username': current_user.username,
        'full_name': current_user.get_full_name()
    }, room=conversation_id, include_self=False)
    
    logging.info(f'User {current_user.username} joined conversation {conversation_id}')

@socketio.on('leave_conversation')
def on_leave_conversation(data):
    if not current_user.is_authenticated:
        return
    
    conversation_id = data.get('conversation_id')
    if not conversation_id:
        return
    
    leave_room(conversation_id)
    
    # Remove from active users
    if conversation_id in active_users and str(current_user.id) in active_users[conversation_id]:
        active_users[conversation_id].remove(str(current_user.id))
        if not active_users[conversation_id]:
            del active_users[conversation_id]
    
    # Notify other users
    emit('user_offline', {
        'user_id': current_user.id,
        'username': current_user.username
    }, room=conversation_id, include_self=False)
    
    logging.info(f'User {current_user.username} left conversation {conversation_id}')

@socketio.on('send_message')
def on_send_message(data):
    if not current_user.is_authenticated:
        emit('error', {'message': 'Authentication required'})
        return
    
    try:
        # Extract message data
        receiver_id = data.get('receiver_id')
        product_id = data.get('product_id')
        message_text = data.get('message', '').strip()
        message_type = data.get('message_type', 'text')
        offer_price = data.get('offer_price')
        offer_quantity = data.get('offer_quantity', 1)
        
        if not message_text:
            emit('error', {'message': 'Message cannot be empty'})
            return
        
        if not receiver_id:
            emit('error', {'message': 'Receiver ID required'})
            return
        
        # Verify receiver exists
        receiver = User.query.get(receiver_id)
        if not receiver:
            emit('error', {'message': 'Receiver not found'})
            return
        
        # Generate or get conversation ID
        if product_id:
            participants = sorted([current_user.id, receiver_id])
            conversation_id = f"conv_{participants[0]}_{participants[1]}_product_{product_id}"
        else:
            participants = sorted([current_user.id, receiver_id])
            conversation_id = f"conv_{participants[0]}_{participants[1]}_general"
        
        # Create or update conversation
        conversation = ChatConversation.query.filter_by(conversation_id=conversation_id).first()
        if not conversation:
            conversation = ChatConversation(
                conversation_id=conversation_id,
                seller_id=current_user.id if current_user.user_role == 'seller' else receiver_id,
                buyer_id=receiver_id if current_user.user_role == 'seller' else current_user.id,
                product_id=product_id if product_id else None,
                status='active'
            )
            db.session.add(conversation)
        
        # Update conversation
        conversation.last_message_at = datetime.utcnow()
        conversation.last_message_by = current_user.id
        
        # Set expiration for offers (24 hours)
        expires_at = None
        if message_type == 'offer':
            expires_at = datetime.utcnow() + timedelta(hours=24)
        
        # Create chat message
        chat_message = ChatMessage(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            product_id=product_id if product_id else None,
            message=message_text,
            message_type=message_type,
            offer_price=float(offer_price) if offer_price else None,
            offer_quantity=int(offer_quantity) if offer_quantity else 1,
            expires_at=expires_at,
            conversation_id=conversation_id
        )
        
        db.session.add(chat_message)
        db.session.commit()
        
        # Prepare message data for broadcast
        message_data = {
            'id': chat_message.id,
            'sender_id': current_user.id,
            'sender_name': current_user.get_full_name(),
            'sender_username': current_user.username,
            'receiver_id': receiver_id,
            'message': message_text,
            'message_type': message_type,
            'offer_price': chat_message.offer_price,
            'offer_quantity': chat_message.offer_quantity,
            'created_at': chat_message.created_at.strftime('%H:%M'),
            'conversation_id': conversation_id,
            'is_expired': False,
            'deal_accepted': None
        }
        
        # Emit to conversation room
        emit('new_message', message_data, room=conversation_id)
        
        # Send confirmation to sender
        emit('message_sent', {
            'status': 'success',
            'message_id': chat_message.id,
            'conversation_id': conversation_id
        })
        
        logging.info(f'Message sent from {current_user.username} to {receiver.username}')
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error sending message: {str(e)}')
        emit('error', {'message': 'Failed to send message'})

@socketio.on('respond_to_offer')
def on_respond_to_offer(data):
    if not current_user.is_authenticated:
        emit('error', {'message': 'Authentication required'})
        return
    
    try:
        message_id = data.get('message_id')
        action = data.get('action')  # 'accept', 'reject', 'counter'
        counter_price = data.get('counter_price')
        
        if not message_id or not action:
            emit('error', {'message': 'Message ID and action required'})
            return
        
        # Get the original offer message
        offer_message = ChatMessage.query.get(message_id)
        if not offer_message or offer_message.receiver_id != current_user.id:
            emit('error', {'message': 'Offer not found or access denied'})
            return
        
        if offer_message.message_type != 'offer':
            emit('error', {'message': 'This is not an offer message'})
            return
        
        # Check if offer is expired
        if offer_message.expires_at and offer_message.expires_at < datetime.utcnow():
            emit('error', {'message': 'This offer has expired'})
            return
        
        if action == 'accept':
            # Accept the offer
            offer_message.deal_accepted = True
            offer_message.deal_accepted_at = datetime.utcnow()
            
            # Create deal confirmation message
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
            
            # Update conversation status
            conversation = ChatConversation.query.filter_by(conversation_id=offer_message.conversation_id).first()
            if conversation:
                conversation.status = 'completed'
                conversation.deal_finalized = True
                conversation.deal_price = offer_message.offer_price
            
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
            
            # Update conversation status
            conversation = ChatConversation.query.filter_by(conversation_id=offer_message.conversation_id).first()
            if conversation:
                conversation.status = 'negotiating'
                conversation.current_offer_price = float(counter_price)
                conversation.current_offer_by = current_user.id
        
        db.session.commit()
        
        # Broadcast update to conversation room
        emit('offer_response', {
            'message_id': message_id,
            'action': action,
            'user_id': current_user.id,
            'user_name': current_user.get_full_name()
        }, room=offer_message.conversation_id)
        
        emit('response_sent', {'status': 'success', 'action': action})
        
        logging.info(f'User {current_user.username} responded to offer {message_id} with action: {action}')
        
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error responding to offer: {str(e)}')
        emit('error', {'message': 'Failed to respond to offer'})

@socketio.on('typing')
def on_typing(data):
    if not current_user.is_authenticated:
        return
    
    conversation_id = data.get('conversation_id')
    is_typing = data.get('is_typing', False)
    
    if conversation_id:
        emit('user_typing', {
            'user_id': current_user.id,
            'username': current_user.username,
            'is_typing': is_typing
        }, room=conversation_id, include_self=False)

@socketio.on('get_online_users')
def on_get_online_users(data):
    conversation_id = data.get('conversation_id')
    if conversation_id and conversation_id in active_users:
        emit('online_users', {
            'conversation_id': conversation_id,
            'online_users': active_users[conversation_id]
        })
    else:
        emit('online_users', {
            'conversation_id': conversation_id,
            'online_users': []
        })