import random
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Product, Category, ProductImage, BarterProposal, Cart, ChatMessage, ChatConversation
from datetime import datetime, timedelta

def create_dummy_data():
    """Create comprehensive dummy stores with detailed barter preferences"""

    with app.app_context():
        # Drop all tables and recreate to ensure proper structure
        db.drop_all()
        db.create_all()

        print("Database tables recreated successfully")

        # Create dummy sellers (25 complete stores)
        dummy_sellers = [
            {
                'username': 'elektronik_jakarta',
                'email': 'elektronik.jkt@example.com',
                'password': 'password123',
                'first_name': 'Andi',
                'last_name': 'Elektronik',
                'phone': '081234567890',
                'role': 'seller'
            },
            {
                'username': 'fashion_bandung',
                'email': 'fashion.bdg@example.com',
                'password': 'password123',
                'first_name': 'Sari',
                'last_name': 'Fashion',
                'phone': '082234567891',
                'role': 'seller'
            },
            {
                'username': 'rumah_tangga_solo',
                'email': 'rumah.solo@example.com',
                'password': 'password123',
                'first_name': 'Budi',
                'last_name': 'Prasetyo',
                'phone': '083234567892',
                'role': 'seller'
            },
            {
                'username': 'olahraga_surabaya',
                'email': 'sport.sby@example.com',
                'password': 'password123',
                'first_name': 'Rini',
                'last_name': 'Sport',
                'phone': '084234567893',
                'role': 'seller'
            },
            {
                'username': 'buku_yogya',
                'email': 'buku.jogja@example.com',
                'password': 'password123',
                'first_name': 'Dani',
                'last_name': 'Bookstore',
                'phone': '085234567894',
                'role': 'seller'
            },
            {
                'username': 'mainan_medan',
                'email': 'toys.medan@example.com',
                'password': 'password123',
                'first_name': 'Lisa',
                'last_name': 'Toys',
                'phone': '086234567895',
                'role': 'seller'
            },
            {
                'username': 'otomotif_makassar',
                'email': 'auto.mks@example.com',
                'password': 'password123',
                'first_name': 'Agus',
                'last_name': 'Motor',
                'phone': '087234567896',
                'role': 'seller'
            },
            {
                'username': 'kecantikan_bali',
                'email': 'beauty.bali@example.com',
                'password': 'password123',
                'first_name': 'Dewi',
                'last_name': 'Beauty',
                'phone': '088234567897',
                'role': 'seller'
            },
            {
                'username': 'koleksi_semarang',
                'email': 'koleksi.smg@example.com',
                'password': 'password123',
                'first_name': 'Eko',
                'last_name': 'Collector',
                'phone': '089234567898',
                'role': 'seller'
            },
            {
                'username': 'vintage_palembang',
                'email': 'vintage.plg@example.com',
                'password': 'password123',
                'first_name': 'Maya',
                'last_name': 'Vintage',
                'phone': '080234567899',
                'role': 'seller'
            },
            {
                'username': 'furniture_jakarta',
                'email': 'furniture.jkt@example.com',
                'password': 'password123',
                'first_name': 'Bambang',
                'last_name': 'Furniture',
                'phone': '081234567800',
                'role': 'seller'
            },
            {
                'username': 'komputer_surabaya',
                'email': 'computer.sby@example.com',
                'password': 'password123',
                'first_name': 'Indra',
                'last_name': 'Tech',
                'phone': '082234567801',
                'role': 'seller'
            },
            {
                'username': 'sepatu_bandung',
                'email': 'shoes.bdg@example.com',
                'password': 'password123',
                'first_name': 'Rina',
                'last_name': 'Shoes',
                'phone': '083234567802',
                'role': 'seller'
            },
            {
                'username': 'kuliner_medan',
                'email': 'food.medan@example.com',
                'password': 'password123',
                'first_name': 'Hendra',
                'last_name': 'Kuliner',
                'phone': '084234567803',
                'role': 'seller'
            },
            {
                'username': 'gadget_yogya',
                'email': 'gadget.jogja@example.com',
                'password': 'password123',
                'first_name': 'Sinta',
                'last_name': 'Gadget',
                'phone': '085234567804',
                'role': 'seller'
            },
            # Tambahan 10 penjual baru
            {
                'username': 'musik_jakarta',
                'email': 'musik.jkt@example.com',
                'password': 'password123',
                'first_name': 'Rian',
                'last_name': 'Music',
                'phone': '086234567805',
                'role': 'seller'
            },
            {
                'username': 'outdoor_bandung',
                'email': 'outdoor.bdg@example.com',
                'password': 'password123',
                'first_name': 'Toni',
                'last_name': 'Adventure',
                'phone': '087234567806',
                'role': 'seller'
            },
            {
                'username': 'crafts_solo',
                'email': 'crafts.solo@example.com',
                'password': 'password123',
                'first_name': 'Yanti',
                'last_name': 'Handmade',
                'phone': '088234567807',
                'role': 'seller'
            },
            {
                'username': 'photography_sby',
                'email': 'photo.sby@example.com',
                'password': 'password123',
                'first_name': 'Dimas',
                'last_name': 'Photo',
                'phone': '089234567808',
                'role': 'seller'
            },
            {
                'username': 'gaming_medan',
                'email': 'gaming.medan@example.com',
                'password': 'password123',
                'first_name': 'Rizal',
                'last_name': 'Gaming',
                'phone': '080234567809',
                'role': 'seller'
            },
            {
                'username': 'art_supplies_jogja',
                'email': 'art.jogja@example.com',
                'password': 'password123',
                'first_name': 'Luna',
                'last_name': 'Artist',
                'phone': '081234567810',
                'role': 'seller'
            },
            {
                'username': 'hobby_makassar',
                'email': 'hobby.mks@example.com',
                'password': 'password123',
                'first_name': 'Farid',
                'last_name': 'Hobby',
                'phone': '082234567811',
                'role': 'seller'
            },
            {
                'username': 'tools_palembang',
                'email': 'tools.plg@example.com',
                'password': 'password123',
                'first_name': 'Bayu',
                'last_name': 'Tools',
                'phone': '083234567812',
                'role': 'seller'
            },
            {
                'username': 'watches_bali',
                'email': 'watches.bali@example.com',
                'password': 'password123',
                'first_name': 'Kadek',
                'last_name': 'Timepiece',
                'phone': '084234567813',
                'role': 'seller'
            },
            {
                'username': 'plants_semarang',
                'email': 'plants.smg@example.com',
                'password': 'password123',
                'first_name': 'Sari',
                'last_name': 'Garden',
                'phone': '085234567814',
                'role': 'seller'
            }
        ]

        # Create dummy buyers (30)
        dummy_buyers = [
            {
                'username': 'pembeli_rian',
                'email': 'rian.buyer@example.com',
                'password': 'password123',
                'first_name': 'Rian',
                'last_name': 'Hermawan',
                'phone': '081345678900',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_sinta',
                'email': 'sinta.buyer@example.com',
                'password': 'password123',
                'first_name': 'Sinta',
                'last_name': 'Maharani',
                'phone': '082345678901',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_dedi',
                'email': 'dedi.buyer@example.com',
                'password': 'password123',
                'first_name': 'Dedi',
                'last_name': 'Kurniawan',
                'phone': '083345678902',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_wati',
                'email': 'wati.buyer@example.com',
                'password': 'password123',
                'first_name': 'Wati',
                'last_name': 'Sari',
                'phone': '084345678903',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_joko',
                'email': 'joko.buyer@example.com',
                'password': 'password123',
                'first_name': 'Joko',
                'last_name': 'Susilo',
                'phone': '085345678904',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_nina',
                'email': 'nina.buyer@example.com',
                'password': 'password123',
                'first_name': 'Nina',
                'last_name': 'Anggraini',
                'phone': '086345678905',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_tono',
                'email': 'tono.buyer@example.com',
                'password': 'password123',
                'first_name': 'Tono',
                'last_name': 'Wijaya',
                'phone': '087345678906',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_lia',
                'email': 'lia.buyer@example.com',
                'password': 'password123',
                'first_name': 'Lia',
                'last_name': 'Fitri',
                'phone': '088345678907',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_hadi',
                'email': 'hadi.buyer@example.com',
                'password': 'password123',
                'first_name': 'Hadi',
                'last_name': 'Santoso',
                'phone': '089345678908',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_yuni',
                'email': 'yuni.buyer@example.com',
                'password': 'password123',
                'first_name': 'Yuni',
                'last_name': 'Rahayu',
                'phone': '080345678909',
                'role': 'buyer'
            },
            # Tambahan 20 pembeli baru
            {
                'username': 'pembeli_andi',
                'email': 'andi.buyer@example.com',
                'password': 'password123',
                'first_name': 'Andi',
                'last_name': 'Pratama',
                'phone': '081345678910',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_sari',
                'email': 'sari.buyer@example.com',
                'password': 'password123',
                'first_name': 'Sari',
                'last_name': 'Indah',
                'phone': '082345678911',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_budi',
                'email': 'budi.buyer@example.com',
                'password': 'password123',
                'first_name': 'Budi',
                'last_name': 'Santoso',
                'phone': '083345678912',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_dewi',
                'email': 'dewi.buyer@example.com',
                'password': 'password123',
                'first_name': 'Dewi',
                'last_name': 'Lestari',
                'phone': '084345678913',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_rudi',
                'email': 'rudi.buyer@example.com',
                'password': 'password123',
                'first_name': 'Rudi',
                'last_name': 'Hartono',
                'phone': '085345678914',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_maya',
                'email': 'maya.buyer@example.com',
                'password': 'password123',
                'first_name': 'Maya',
                'last_name': 'Sari',
                'phone': '086345678915',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_fajar',
                'email': 'fajar.buyer@example.com',
                'password': 'password123',
                'first_name': 'Fajar',
                'last_name': 'Ramadan',
                'phone': '087345678916',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_lina',
                'email': 'lina.buyer@example.com',
                'password': 'password123',
                'first_name': 'Lina',
                'last_name': 'Wati',
                'phone': '088345678917',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_agus',
                'email': 'agus.buyer@example.com',
                'password': 'password123',
                'first_name': 'Agus',
                'last_name': 'Setiawan',
                'phone': '089345678918',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_eka',
                'email': 'eka.buyer@example.com',
                'password': 'password123',
                'first_name': 'Eka',
                'last_name': 'Putri',
                'phone': '080345678919',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_dika',
                'email': 'dika.buyer@example.com',
                'password': 'password123',
                'first_name': 'Dika',
                'last_name': 'Mahendra',
                'phone': '081345678920',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_nita',
                'email': 'nita.buyer@example.com',
                'password': 'password123',
                'first_name': 'Nita',
                'last_name': 'Sari',
                'phone': '082345678921',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_ivan',
                'email': 'ivan.buyer@example.com',
                'password': 'password123',
                'first_name': 'Ivan',
                'last_name': 'Gunawan',
                'phone': '083345678922',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_riska',
                'email': 'riska.buyer@example.com',
                'password': 'password123',
                'first_name': 'Riska',
                'last_name': 'Amelia',
                'phone': '084345678923',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_aldo',
                'email': 'aldo.buyer@example.com',
                'password': 'password123',
                'first_name': 'Aldo',
                'last_name': 'Pratama',
                'phone': '085345678924',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_gita',
                'email': 'gita.buyer@example.com',
                'password': 'password123',
                'first_name': 'Gita',
                'last_name': 'Savitri',
                'phone': '086345678925',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_reza',
                'email': 'reza.buyer@example.com',
                'password': 'password123',
                'first_name': 'Reza',
                'last_name': 'Firdaus',
                'phone': '087345678926',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_mila',
                'email': 'mila.buyer@example.com',
                'password': 'password123',
                'first_name': 'Mila',
                'last_name': 'Kartika',
                'phone': '088345678927',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_aris',
                'email': 'aris.buyer@example.com',
                'password': 'password123',
                'first_name': 'Aris',
                'last_name': 'Munandar',
                'phone': '089345678928',
                'role': 'buyer'
            },
            {
                'username': 'pembeli_dina',
                'email': 'dina.buyer@example.com',
                'password': 'password123',
                'first_name': 'Dina',
                'last_name': 'Oktavia',
                'phone': '080345678929',
                'role': 'buyer'
            }
        ]

        # Create admin/owner
        admin_user = {
            'username': 'admin',
            'email': 'admin@barterhub.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'BarterHub',
            'phone': '+6281234567890',
            'is_admin': True
        }

        # Combine all users
        all_users = dummy_sellers + dummy_buyers + [admin_user]
        created_users = []

        for user_data in all_users:
            # Check if user already exists
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    phone=user_data['phone'],
                    user_role=user_data.get('role', 'buyer'),
                    is_admin=user_data.get('is_admin', False)
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                created_users.append(user)
            else:
                created_users.append(existing_user)

        db.session.commit()
        print(f"Created users - Sellers: {len(dummy_sellers)}, Buyers: {len(dummy_buyers)}, Admin: 1")

        # Get categories
        categories = Category.query.all()
        if not categories:
            # Create categories if they don't exist
            categories_data = [
                'Elektronik', 'Pakaian & Aksesoris', 'Rumah & Taman',
                'Olahraga & Outdoor', 'Buku & Media', 'Mainan & Permainan',
                'Otomotif', 'Kesehatan & Kecantikan', 'Koleksi', 'Lainnya'
            ]
            for category_name in categories_data:
                category = Category(name=category_name)
                db.session.add(category)
            db.session.commit()
            categories = Category.query.all()
            print(f"Created {len(categories_data)} categories")

        # Comprehensive products data with specific barter information
        products_data = [
            # ELEKTRONIK STORE (elektronik_jakarta)
            {
                'title': 'Samsung Galaxy S24 Ultra 512GB Titanium',
                'description': 'Samsung Galaxy S24 Ultra flagship terbaru, RAM 12GB, storage 512GB, kamera 200MP dengan AI zoom 100x, S-Pen included, kondisi mulus seperti baru masih garansi resmi.',
                'condition': 'Like New',
                'estimated_value': 19500000,
                'category': 'Elektronik',
                'utility_score': 10,
                'scarcity_score': 9,
                'durability_score': 9,
                'portability_score': 9,
                'seller_index': 0,
                'barter_with': [
                    'iPhone 15 Pro + uang Rp 3.000.000',
                    'MacBook Air M3 13 inch',
                    'Gaming laptop RTX 4060 + monitor gaming',
                    'Kombinasi iPad Pro + Apple Watch Ultra + cash Rp 5.000.000'
                ],
                'images': [
                    'https://images.samsung.com/is/image/samsung/p6pim/id/2401/gallery/id-galaxy-s24-ultra-s928-491187-sm-s928bztgxid-539467766?$650_519_PNG$',
                    'https://images.samsung.com/is/image/samsung/p6pim/id/sm-s928bztgxid/gallery/id-galaxy-s24-ultra-s928-sm-s928bztgxid-thumb-539467769?wid=520&hei=520&fmt=png',
                    'https://images.unsplash.com/photo-1711532718276-c96905a22498?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            {
                'title': 'MacBook Pro M3 Max 14 inch 1TB Space Black',
                'description': 'MacBook Pro dengan chip M3 Max untuk performa maksimal, RAM 36GB unified memory, SSD 1TB, perfect untuk video editing 4K, 3D rendering, programming berat.',
                'condition': 'New',
                'estimated_value': 45000000,
                'category': 'Elektronik',
                'utility_score': 10,
                'scarcity_score': 10,
                'durability_score': 10,
                'portability_score': 8,
                'seller_index': 0,
                'barter_with': [
                    'Gaming PC RTX 4080 Super + monitor 4K + mechanical keyboard set',
                    'iPhone 15 Pro Max + iPad Pro M4 + Apple Watch Ultra + cash Rp 10.000.000',
                    'Workstation desktop Threadripper + professional monitor 32 inch',
                    'Server hardware untuk home lab + networking equipment'
                ],
                'images': [
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697230830200',
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-gallery4-202310?wid=2000&hei=1536&fmt=jpeg&qlt=80&.v=1697230842915',
                    'https://images.unsplash.com/photo-1695671351510-03d8797915e2?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            {
                'title': 'Sony Alpha A7R V Mirrorless Camera Body',
                'description': 'Kamera mirrorless Sony A7R V dengan sensor full frame 61MP, perfect untuk photography profesional, video 8K, image stabilization 8 stops, kondisi mint.',
                'condition': 'Like New',
                'estimated_value': 32000000,
                'category': 'Elektronik',
                'utility_score': 9,
                'scarcity_score': 9,
                'durability_score': 9,
                'portability_score': 7,
                'seller_index': 0,
                'barter_with': [
                    'Lensa Sony FE 70-200mm f/2.8 GM II + cash Rp 8.000.000',
                    'MacBook Pro M3 Pro 16 inch',
                    'Gaming setup RTX 4070 + monitor',
                    'Drone DJI Mavic 3 Pro + accessories professional kit'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1617005082133-548c4dd27f35?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1606981780295-1c9c18093c95?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # FASHION STORE (fashion_bandung)
            {
                'title': 'Tas Hermes Kelly 25 Black Epsom Leather',
                'description': 'Tas Hermes Kelly 25cm warna hitam dengan kulit Epsom, hardware gold, kondisi excellent, include box, dustbag, ribbon, authenticity card. Investasi fashion terbaik.',
                'condition': 'Like New',
                'estimated_value': 85000000,
                'category': 'Pakaian & Aksesoris',
                'utility_score': 8,
                'scarcity_score': 10,
                'durability_score': 10,
                'portability_score': 9,
                'seller_index': 1,
                'barter_with': [
                    'Rolex Submariner Date + cash Rp 20.000.000',
                    'Chanel Classic Flap Medium + Chanel Boy Bag',
                    'Louis Vuitton Neverfull MM + Speedy 30 + Pochette + cash Rp 30.000.000',
                    'Investasi emas batangan 100 gram + jewelry set berlian'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1584917865442-de89df76afd3?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1517704079434-d05717a7f2f6?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            {
                'title': 'Sepatu Nike Air Jordan 1 Retro High Chicago (2015)',
                'description': 'Sepatu legend Nike Air Jordan 1 Chicago colorway release 2015, ukuran US 9, kondisi very good dengan aging natural, box original masih ada, sneakerhead dream.',
                'condition': 'Good',
                'estimated_value': 8500000,
                'category': 'Pakaian & Aksesoris',
                'utility_score': 8,
                'scarcity_score': 10,
                'durability_score': 9,
                'portability_score': 9,
                'seller_index': 1,
                'barter_with': [
                    'Nike Air Jordan 4 Black Cat + Nike Air Jordan 11 Bred',
                    'Yeezy Boost 350 V2 (3 pairs berbeda colorway)',
                    'Off-White x Nike collaboration (any model) + cash Rp 2.000.000',
                    'Supreme hoodie + Palace tee collection + Stussy jacket'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # RUMAH TANGGA STORE (rumah_tangga_solo)
            {
                'title': 'KitchenAid Stand Mixer Artisan 5 Quart Candy Apple Red',
                'description': 'Stand mixer KitchenAid Artisan 5 quart warna Candy Apple Red, 10 speed, include bowl stainless steel, dough hook, wire whip, flat beater. Perfect untuk baking enthusiast.',
                'condition': 'New',
                'estimated_value': 6500000,
                'category': 'Rumah & Taman',
                'utility_score': 8,
                'scarcity_score': 7,
                'durability_score': 10,
                'portability_score': 5,
                'seller_index': 2,
                'barter_with': [
                    'Coffee machine Breville Barista Express + coffee grinder',
                    'Vitamix blender + food processor KitchenAid',
                    'Set panci Le Creuset Dutch oven + wok premium',
                    'Air fryer Philips XXL + rice cooker premium + cash Rp 1.500.000'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1556909114-35ba1a810fec?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1585515656811-1b98e591ad25?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1506619216599-9d16d0903dfd?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            {
                'title': 'Sofa Sectional L-Shape Premium Fabric Scandinavian',
                'description': 'Sofa sectional bentuk L dengan design Scandinavian modern, fabric premium tahan noda, foam high density, ukuran 3x2.5 meter, warna light grey, sangat nyaman.',
                'condition': 'Like New',
                'estimated_value': 12000000,
                'category': 'Rumah & Taman',
                'utility_score': 9,
                'scarcity_score': 6,
                'durability_score': 8,
                'portability_score': 2,
                'seller_index': 2,
                'barter_with': [
                    'Dining set meja kayu solid 6 kursi + buffet cabinet',
                    'TV 75 inch Samsung QLED + sound system + TV stand',
                    'Bed set king size + spring bed premium + lemari sliding door',
                    'AC split 2PK + AC 1PK + kulkas side by side + cash Rp 3.000.000'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1549497538-303791108f95?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # OLAHRAGA STORE (olahraga_surabaya)
            {
                'title': 'Sepeda Road Bike Specialized Tarmac SL7 Expert',
                'description': 'Road bike Specialized Tarmac SL7 Expert dengan frame carbon fiber, groupset Shimano Ultegra Di2 electronic shifting, wheelset carbon, perfect untuk road cycling serious.',
                'condition': 'Like New',
                'estimated_value': 48000000,
                'category': 'Olahraga & Outdoor',
                'utility_score': 9,
                'scarcity_score': 9,
                'durability_score': 8,
                'portability_score': 6,
                'seller_index': 3,
                'barter_with': [
                    'Honda PCX 160 2024 + top box + windshield + cash Rp 10.000.000',
                    'Motor trail Kawasaki KLX 150 + gear set lengkap',
                    'Gaming PC RTX 4080 + monitor 4K + racing simulator setup',
                    'Drone DJI Air 3 + gimbal + accessories + MacBook Air M3'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1544191696-15693be5494?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1573790247793-251a25e02982?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            {
                'title': 'Home Gym Set Complete Premium Equipment',
                'description': 'Set gym lengkap untuk home workout: power rack, Olympic barbell, dumbell adjustable 50kg, bench adjustable, pull-up station, resistance bands, yoga mat premium.',
                'condition': 'New',
                'estimated_value': 25000000,
                'category': 'Olahraga & Outdoor',
                'utility_score': 9,
                'scarcity_score': 7,
                'durability_score': 10,
                'portability_score': 3,
                'seller_index': 3,
                'barter_with': [
                    'Treadmill commercial grade + rowing machine',
                    'Sepeda indoor trainer smart + bike computer Garmin',
                    'Pool table 9 feet + air hockey table + ping pong table',
                    'Projector 4K + screen motorized + sound system + cash Rp 5.000.000'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1571019613454-1cb2f98b2d8b?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1517963628607-2055c774e0c?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1599570401097-e0194a432c32?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # BUKU STORE (buku_yogya)
            {
                'title': 'Koleksi Buku Programming Complete Library (50 Judul)',
                'description': 'Library programming terlengkap 50 judul: Python, JavaScript, React, Node.js, Machine Learning, AI, Data Science, Cloud Computing, DevOps, semua kondisi excellent.',
                'condition': 'Like New',
                'estimated_value': 3500000,
                'category': 'Buku & Media',
                'utility_score': 9,
                'scarcity_score': 8,
                'durability_score': 7,
                'portability_score': 5,
                'seller_index': 4,
                'barter_with': [
                    'iPad Pro 12.9 inch + Apple Pencil + keyboard case',
                    'MacBook Air M2 + external monitor + keyboard mechanical',
                    'Gaming laptop RTX 4060 untuk programming',
                    'Online course bundle (Udemy, Coursera, Pluralsight) + Notion Pro + cash'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1450101371691-6a306761936e?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # MAINAN STORE (mainan_medan)
            {
                'title': 'LEGO Architecture Collection Complete (15 Sets)',
                'description': 'Koleksi LEGO Architecture lengkap 15 sets: Statue of Liberty, Eiffel Tower, Big Ben, Empire State Building, dll. Semua sealed/MISB, perfect untuk collector adult.',
                'condition': 'New',
                'estimated_value': 12000000,
                'category': 'Mainan & Permainan',
                'utility_score': 7,
                'scarcity_score': 9,
                'durability_score': 10,
                'portability_score': 6,
                'seller_index': 5,
                'barter_with': [
                    'Nintendo Switch OLED + games collection + Pro controller',
                    'PlayStation 5 + games AAA + extra controller + headset',
                    'Gaming PC mid-range RTX 4060 + monitor gaming',
                    'Drone DJI Mini 4 Pro + accessories + iPad untuk controller'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1558060370-d644479cb6f7?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1587654780291-39c9404d746b?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1599597431277-040621393077?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # OTOMOTIF STORE (otomotif_makassar)
            {
                'title': 'Helm Arai RX-7V Racing Samurai Spirit Limited Edition',
                'description': 'Helm Arai RX-7V edisi terbatas Samurai Spirit, size M, Snell approved, fiberglass shell, kondisi mint dengan visor clear dan dark, sangat rare untuk collector.',
                'condition': 'Like New',
                'estimated_value': 8500000,
                'category': 'Otomotif',
                'utility_score': 9,
                'scarcity_score': 10,
                'durability_score': 10,
                'portability_score': 8,
                'seller_index': 6,
                'barter_with': [
                    'Shoei X-Fifteen + Shoei GT-Air 3 + cash Rp 2.000.000',
                    'Riding gear set lengkap (jacket, pants, boots, gloves)',
                    'Action camera GoPro Hero 12 + mount set + microSD + charger',
                    'Smartphone flagship + smartwatch + wireless earbuds + power bank'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1609630875171-b1321377ee65?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1609630875403-8e36661c0b4e?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1586059491619-a36548046911?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # KECANTIKAN STORE (kecantikan_bali)
            {
                'title': 'Skincare Set La Mer Complete Luxury Collection',
                'description': 'Set skincare La Mer luxury complete: The Moisturizing Cream, The Treatment Lotion, The Eye Concentrate, The Renewal Oil, semua size full, authentic dengan receipt.',
                'condition': 'New',
                'estimated_value': 15000000,
                'category': 'Kesehatan & Kecantikan',
                'utility_score': 8,
                'scarcity_score': 8,
                'durability_score': 6,
                'portability_score': 9,
                'seller_index': 7,
                'barter_with': [
                    'Skincare set SK-II Pitera Essentials + treatments',
                    'Chanel makeup collection + perfume + skincare set',
                    'iPhone 15 Pro + Apple Watch + AirPods Pro',
                    'Jewelry set emas 18K + berlian + tas branded'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1596462502278-27bfdc45048?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1541719445730-3b462784f35b?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # KOLEKSI STORE (koleksi_semarang)
            {
                'title': 'Pokemon Cards Complete Base Set 1st Edition Shadowless',
                'description': 'Kartu Pokemon complete Base Set 1st Edition Shadowless termasuk Charizard, Blastoise, Venusaur, semua grade NM-M, perfect untuk serious collector, very rare.',
                'condition': 'Like New',
                'estimated_value': 45000000,
                'category': 'Koleksi',
                'utility_score': 6,
                'scarcity_score': 10,
                'durability_score': 9,
                'portability_score': 9,
                'seller_index': 8,
                'barter_with': [
                    'Rolex Submariner vintage + cash Rp 10.000.000',
                    'MacBook Pro M3 Max + iPad Pro + Apple Watch Ultra',
                    'Honda Civic Type R 2024 + cash Rp 200.000.000',
                    'Investment gold bars 200 gram + jewelry diamond set'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1601814933824-fd0b574dd592?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1622980435270-205d1d91554?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1573082316967-154222e4255b?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # VINTAGE STORE (vintage_palembang)
            {
                'title': 'Rolex Submariner Date 16610 Vintage 1995',
                'description': 'Rolex Submariner Date ref 16610 tahun 1995, kondisi unpolished original, patina natural pada dial, include box papers, service history complete, investment grade.',
                'condition': 'Good',
                'estimated_value': 95000000,
                'category': 'Koleksi',
                'utility_score': 8,
                'scarcity_score': 10,
                'durability_score': 10,
                'portability_score': 10,
                'seller_index': 9,
                'barter_with': [
                    'Patek Philippe Calatrava vintage + cash Rp 50.000.000',
                    'Honda Civic Type R 2024 + BMW X1 + cash Rp 100.000.000',
                    'Investment property apartment 2BR Jakarta Selatan',
                    'Gold bars 500 gram + diamond jewelry set + luxury watch collection'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1622434641406-a158123450f9?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1627392032022-4d10ff5c5fb6?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1599750993126-1755795197e2?ixlib=rb-4.0.3&w=800&q=80'
                ]
            }
        ]

        # Get sellers (non-admin users from the first 25)
        sellers = [u for u in created_users if not u.is_admin][:25]

        # Create products
        created_products_count = 0
        for product_data in products_data:
            # Find category
            category = Category.query.filter_by(name=product_data['category']).first()
            if not category:
                print(f"Warning: Category '{product_data['category']}' not found for product '{product_data['title']}'")
                continue

            # Assign to specific seller
            if product_data['seller_index'] >= len(sellers):
                print(f"Warning: Seller index out of bounds for product '{product_data['title']}'")
                continue
            seller = sellers[product_data['seller_index']]

            # Enhanced description with detailed barter preferences
            enhanced_description = f"{product_data['description']}\n\n"
            enhanced_description += f"💰 **ESTIMATED VALUE**: Rp {product_data['estimated_value']:,}\n\n"
            enhanced_description += f"🔄 **SAYA INGIN BARTER DENGAN**:\n"

            for i, barter_option in enumerate(product_data['barter_with'], 1):
                enhanced_description += f"{i}. {barter_option}\n"

            enhanced_description += f"\n✨ **MENGAPA PILIH PRODUK INI**:\n"
            enhanced_description += f"• Utility Score: {product_data['utility_score']}/10 (tingkat kebutuhan)\n"
            enhanced_description += f"• Scarcity Score: {product_data['scarcity_score']}/10 (tingkat kelangkaan)\n"
            enhanced_description += f"• Durability Score: {product_data['durability_score']}/10 (daya tahan)\n"
            enhanced_description += f"• Portability Score: {product_data['portability_score']}/10 (mudah dibawa)\n\n"

            enhanced_description += f"💬 **READY TO NEGOTIATE**: Hubungi saya via chat untuk diskusi detail barter, bisa kombinasi barang + cash, atau pure barter sesuai kesepakatan!\n\n"
            enhanced_description += f"📍 **LOKASI**: {seller.first_name} {seller.last_name} - Trusted Seller dengan rating 5⭐"

            product = Product(
                title=product_data['title'],
                description=enhanced_description,
                condition=product_data['condition'],
                estimated_value=product_data['estimated_value'],
                category_id=category.id,
                owner_id=seller.id,
                utility_score=product_data['utility_score'],
                scarcity_score=product_data['scarcity_score'],
                durability_score=product_data['durability_score'],
                portability_score=product_data['portability_score'],
                seasonal_factor=random.uniform(0.9, 1.1),
                exchange_preference=" | ".join(product_data['barter_with']),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )

            # Calculate barter value
            product.update_barter_value()

            db.session.add(product)
            db.session.flush() # Flush to get product.id before creating ProductImage

            # Create ProductImage records
            images = product_data.get('images', [])

            for idx, image_url in enumerate(images[:3]):  # Limit to a maximum of 3 images per product
                product_image = ProductImage(
                    product_id=product.id,
                    image_url=image_url,
                    is_primary=(idx == 0) # Set the first image as primary
                )
                db.session.add(product_image)

            created_products_count += 1

        # Create additional products for remaining sellers to ensure each seller has at least one product
        additional_products_data = [
            # FURNITURE STORE (furniture_jakarta) - seller index 10
            {
                'title': 'Meja Kerja Standing Desk Electric Height Adjustable',
                'description': 'Standing desk dengan motor electric untuk adjust tinggi, desktop kayu oak solid, memory preset, cable management, perfect untuk WFH ergonomis.',
                'condition': 'Like New',
                'estimated_value': 8500000,
                'category': 'Rumah & Taman',
                'utility_score': 9,
                'scarcity_score': 7,
                'durability_score': 9,
                'portability_score': 4,
                'seller_index': 10,
                'barter_with': [
                    'Herman Miller chair + monitor arm dual',
                    'MacBook Pro + external monitor 4K + keyboard mechanical',
                    'Gaming chair premium + gaming desk + LED strip setup'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1549497538-303791108f95?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # KOMPUTER TECH STORE (komputer_surabaya) - seller index 11
            {
                'title': 'Gaming PC RTX 4080 Super Complete Setup',
                'description': 'PC Gaming ultimate: Intel i7-14700K, RTX 4080 Super, 32GB DDR5, SSD 2TB, custom water cooling, RGB everything, monitor 27inch 240Hz, keyboard, mouse gaming.',
                'condition': 'Like New',
                'estimated_value': 35000000,
                'category': 'Elektronik',
                'utility_score': 10,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 3,
                'seller_index': 11,
                'barter_with': [
                    'MacBook Pro M3 Max + iPad Pro + accessories',
                    'Honda PCX 160 2024 + top box + cash Rp 5.000.000',
                    'PlayStation 5 + Nintendo Switch + games collection + TV 55inch'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1587831990711-23ca6441447b?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1593640408182-31c70c8268f5?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # SEPATU STORE (sepatu_bandung) - seller index 12
            {
                'title': 'Nike Air Force 1 White Classic Collection',
                'description': 'Koleksi Nike Air Force 1 putih classic, berbagai ukuran 40-45, kondisi deadstock, include box original, perfect untuk sneakerhead collector.',
                'condition': 'New',
                'estimated_value': 2500000,
                'category': 'Pakaian & Aksesoris',
                'utility_score': 8,
                'scarcity_score': 7,
                'durability_score': 9,
                'portability_score': 9,
                'seller_index': 12,
                'barter_with': [
                    'Adidas Yeezy 350 V2 + cash Rp 500.000',
                    'Nike Dunk Low collection (3 pairs)',
                    'Supreme clothing + skateboard deck'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # KULINER STORE (kuliner_medan) - seller index 13
            {
                'title': 'Coffee Machine Breville Barista Express + Grinder Set',
                'description': 'Mesin espresso Breville Barista Express dengan built-in grinder, steam wand, pressure gauge, perfect untuk home barista, like new condition.',
                'condition': 'Like New',
                'estimated_value': 7500000,
                'category': 'Rumah & Taman',
                'utility_score': 8,
                'scarcity_score': 7,
                'durability_score': 9,
                'portability_score': 6,
                'seller_index': 13,
                'barter_with': [
                    'KitchenAid Stand Mixer + coffee beans premium',
                    'Air fryer + rice cooker + blender set',
                    'Dining set 4 kursi + meja kayu solid'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1506619216599-9d16d0903dfd?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # GADGET STORE (gadget_yogya) - seller index 14
            {
                'title': 'iPad Pro M4 12.9 inch 1TB + Apple Pencil Pro + Magic Keyboard',
                'description': 'iPad Pro M4 terbaru 12.9 inch storage 1TB, include Apple Pencil Pro dan Magic Keyboard, perfect untuk digital artist dan professional work.',
                'condition': 'Like New',
                'estimated_value': 22000000,
                'category': 'Elektronik',
                'utility_score': 9,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 8,
                'seller_index': 14,
                'barter_with': [
                    'MacBook Air M3 + external monitor',
                    'Gaming laptop RTX 4060 + drawing tablet',
                    'iPhone 15 Pro Max + AirPods Pro + Apple Watch'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # MUSIK STORE (musik_jakarta) - seller index 15
            {
                'title': 'Gibson Les Paul Standard Electric Guitar + Marshall Amp',
                'description': 'Gibson Les Paul Standard electric guitar warna sunburst dengan Marshall amplifier 50W, include cable dan pick set, perfect untuk rock musician.',
                'condition': 'Good',
                'estimated_value': 18000000,
                'category': 'Lainnya',
                'utility_score': 8,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 5,
                'seller_index': 15,
                'barter_with': [
                    'Fender Stratocaster + effects pedal set',
                    'Electronic drum kit + keyboard piano',
                    'Home studio equipment + microphone set'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1511735111819-9a3f7709049c?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # OUTDOOR STORE (outdoor_bandung) - seller index 16
            {
                'title': 'Camping Gear Complete Set: Tent + Sleeping Bag + Backpack',
                'description': 'Set camping lengkap: tenda 4 orang, sleeping bag down, backpack 60L, kompor portable, matras, headlamp, perfect untuk adventure outdoor.',
                'condition': 'Good',
                'estimated_value': 8500000,
                'category': 'Olahraga & Outdoor',
                'utility_score': 9,
                'scarcity_score': 7,
                'durability_score': 8,
                'portability_score': 7,
                'seller_index': 16,
                'barter_with': [
                    'Mountain bike + helmet + gear set',
                    'Drone DJI + action camera + tripod',
                    'Fishing equipment complete set'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1551632811-561732d1e306?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # CRAFTS STORE (crafts_solo) - seller index 17
            {
                'title': 'Handmade Batik Art Collection + Woodcarving Set',
                'description': 'Koleksi seni batik tulis tangan original Solo + set alat ukir kayu lengkap, perfect untuk art collector atau craft enthusiast.',
                'condition': 'New',
                'estimated_value': 5500000,
                'category': 'Lainnya',
                'utility_score': 7,
                'scarcity_score': 9,
                'durability_score': 8,
                'portability_score': 6,
                'seller_index': 17,
                'barter_with': [
                    'Painting set + easel + canvas collection',
                    'Pottery wheel + kiln + clay supplies',
                    'Jewelry making tools + precious stones'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1452457807411-4979b707c5be?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # PHOTOGRAPHY STORE (photography_sby) - seller index 18
            {
                'title': 'Canon EOS R6 Mark II + RF 24-70mm f/2.8L + Accessories',
                'description': 'Canon EOS R6 Mark II mirrorless camera dengan lensa RF 24-70mm f/2.8L, battery grip, flash, tripod carbon fiber, perfect untuk professional photography.',
                'condition': 'Like New',
                'estimated_value': 42000000,
                'category': 'Elektronik',
                'utility_score': 9,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 7,
                'seller_index': 18,
                'barter_with': [
                    'Sony A7R V + lensa collection',
                    'MacBook Pro M3 Max + monitor 4K + editing suite',
                    'Honda PCX 160 + top box + cash Rp 15.000.000'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1617005082133-548c4dd27f35?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1606981780295-1c9c18093c95?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # GAMING STORE (gaming_medan) - seller index 19
            {
                'title': 'PlayStation 5 Pro + Games Collection + Racing Wheel Setup',
                'description': 'PS5 Pro dengan 15 games AAA, racing wheel Logitech G923, gaming headset, extra controller, racing chair, complete gaming station.',
                'condition': 'Like New',
                'estimated_value': 25000000,
                'category': 'Mainan & Permainan',
                'utility_score': 9,
                'scarcity_score': 8,
                'durability_score': 8,
                'portability_score': 5,
                'seller_index': 19,
                'barter_with': [
                    'Gaming PC RTX 4070 + monitor + peripherals',
                    'Nintendo Switch OLED + Steam Deck + games',
                    'VR headset Meta Quest 3 + accessories + games'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1511512578047-dfb367046420?ixlib=rb-4.0.3&w=800&q=80'
                ]
            }
        ]

        # Add remaining sellers with basic products to ensure everyone has at least one product
        for i in range(20, 25):  # seller indices 20-24
            additional_products_data.append({
                'title': f'Premium Item Collection from {sellers[i].get_full_name()}',
                'description': f'Special premium item collection dari {sellers[i].get_full_name()}, kondisi excellent, ready untuk barter dengan berbagai kategori barang sesuai kebutuhan.',
                'condition': 'Like New',
                'estimated_value': random.randint(2000000, 15000000),
                'category': random.choice(['Elektronik', 'Pakaian & Aksesoris', 'Rumah & Taman', 'Lainnya']),
                'utility_score': random.randint(7, 10),
                'scarcity_score': random.randint(6, 9),
                'durability_score': random.randint(8, 10),
                'portability_score': random.randint(6, 9),
                'seller_index': i,
                'barter_with': [
                    'Electronics dan gadgets terbaru',
                    'Fashion items premium brand',
                    'Home appliances dan furniture'
                ],
                'images': [
                    'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-4.0.3&w=800&q=80'
                ]
            })

        # Combine all products data
        all_products_data = products_data + additional_products_data

        # Create products from the combined data
        for product_data in all_products_data:
            # Find category
            category = Category.query.filter_by(name=product_data['category']).first()
            if not category:
                print(f"Warning: Category '{product_data['category']}' not found for product '{product_data['title']}'")
                continue

            # Assign to specific seller
            if product_data['seller_index'] >= len(sellers):
                print(f"Warning: Seller index out of bounds for product '{product_data['title']}'")
                continue
            seller = sellers[product_data['seller_index']]

            # Enhanced description with detailed barter preferences
            enhanced_description = f"{product_data['description']}\n\n"
            enhanced_description += f"💰 **ESTIMATED VALUE**: Rp {product_data['estimated_value']:,}\n\n"
            enhanced_description += f"🔄 **SAYA INGIN BARTER DENGAN**:\n"

            for i, barter_option in enumerate(product_data['barter_with'], 1):
                enhanced_description += f"{i}. {barter_option}\n"

            enhanced_description += f"\n✨ **MENGAPA PILIH PRODUK INI**:\n"
            enhanced_description += f"• Utility Score: {product_data['utility_score']}/10 (tingkat kebutuhan)\n"
            enhanced_description += f"• Scarcity Score: {product_data['scarcity_score']}/10 (tingkat kelangkaan)\n"
            enhanced_description += f"• Durability Score: {product_data['durability_score']}/10 (daya tahan)\n"
            enhanced_description += f"• Portability Score: {product_data['portability_score']}/10 (mudah dibawa)\n\n"

            enhanced_description += f"💬 **READY TO NEGOTIATE**: Hubungi saya via chat untuk diskusi detail barter, bisa kombinasi barang + cash, atau pure barter sesuai kesepakatan!\n\n"
            enhanced_description += f"📍 **LOKASI**: {seller.first_name} {seller.last_name} - Trusted Seller dengan rating 5⭐"

            product = Product(
                title=product_data['title'],
                description=enhanced_description,
                condition=product_data['condition'],
                estimated_value=product_data['estimated_value'],
                category_id=category.id,
                owner_id=seller.id,
                utility_score=product_data['utility_score'],
                scarcity_score=product_data['scarcity_score'],
                durability_score=product_data['durability_score'],
                portability_score=product_data['portability_score'],
                seasonal_factor=random.uniform(0.9, 1.1),
                exchange_preference=" | ".join(product_data['barter_with']),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )

            # Calculate barter value
            product.update_barter_value()

            db.session.add(product)
            db.session.flush() # Flush to get product.id before creating ProductImage

            # Create ProductImage records
            images = product_data.get('images', [])

            for idx, image_url in enumerate(images[:3]):  # Limit to a maximum of 3 images per product
                product_image = ProductImage(
                    product_id=product.id,
                    image_url=image_url,
                    is_primary=(idx == 0) # Set the first image as primary
                )
                db.session.add(product_image)

            created_products_count += 1


        # Create realistic cart entries for buyers
        buyers = [u for u in created_users if u.user_role == 'buyer'][:30]
        all_products = Product.query.all()

        cart_entries = 0
        for buyer in buyers[:15]:  # First 15 buyers have items in cart
            # Each buyer adds 2-4 random products to cart
            num_items = random.randint(2, 4)
            selected_products = random.sample(all_products, min(num_items, len(all_products)))

            for product in selected_products:
                if product.owner_id != buyer.id:  # Don't add own products
                    cart_item = Cart(
                        buyer_id=buyer.id,
                        product_id=product.id,
                        quantity=1
                    )
                    db.session.add(cart_item)
                    cart_entries += 1

        # Create realistic barter proposals and negotiations
        proposals_created = 0
        for i in range(30):  # Create 30 realistic proposals
            buyer = random.choice(buyers)
            product = random.choice(all_products)

            if product.owner_id != buyer.id:
                proposal_messages = [
                    f'Halo! Saya tertarik dengan {product.title}. Saya punya beberapa opsi untuk barter, bisa diskusi?',
                    f'Hi, produk {product.title} masih available? Saya ada barang yang mungkin cocok untuk tukar.',
                    f'Selamat siang, saya lihat produk Anda {product.title} sangat menarik. Apakah bisa dibarter dengan barang elektronik?',
                    f'Permisi, untuk {product.title} apakah bisa tukar dengan kombinasi barang + cash? Mari diskusi detailnya.',
                ]

                proposal = BarterProposal(
                    proposer_id=buyer.id,
                    receiver_id=product.owner_id,
                    offered_product_id=product.id,  # Simplified for demo
                    wanted_product_id=product.id,
                    message=random.choice(proposal_messages),
                    status=random.choice(['pending', 'accepted', 'rejected', 'negotiating']),
                    buyer_offer_price=random.randint(int(product.estimated_value * 0.7), int(product.estimated_value * 1.1)),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
                )
                db.session.add(proposal)
                proposals_created += 1

        # Create chat conversations and messages with barter focus
        conversations_created = 0
        for i in range(25):  # Create 25 chat conversations
            seller = random.choice(sellers)
            buyer = random.choice(buyers)
            # Ensure the selected product belongs to the selected seller
            # Filter products to only include those owned by the chosen seller
            seller_products = [p for p in all_products if p.owner_id == seller.id]
            if not seller_products:
                continue # Skip if the seller has no products

            product = random.choice(seller_products)


            # Generate conversation ID
            participants = sorted([seller.id, buyer.id])
            conversation_id = f"conv_{participants[0]}_{participants[1]}_product_{product.id}"

            # Create conversation
            conversation = ChatConversation(
                conversation_id=conversation_id,
                seller_id=seller.id,
                buyer_id=buyer.id,
                product_id=product.id,
                status=random.choice(['active', 'negotiating', 'completed']),
                last_message_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
            )
            db.session.add(conversation)

            # Create realistic barter-focused chat messages
            barter_messages = [
                f'Halo, saya tertarik dengan {product.title}. Apakah bisa barter?',
                f'Saya punya {random.choice(["iPhone", "MacBook", "Gaming PC", "Motor", "Sepeda", "Kamera"])} yang mungkin cocok untuk tukar.',
                f'Untuk nilai barter, apakah bisa kombinasi barang + cash?',
                f'Kondisi barang saya {random.choice(["Like New", "Good", "Excellent"])}, ready untuk inspeksi.',
                f'Lokasi saya di {random.choice(["Jakarta", "Bandung", "Surabaya", "Medan"])}, gimana untuk meetup?',
                f'Deal! Saya setuju dengan barter ini. Kapan bisa ketemuan?'
            ]

            # Create chat messages for this conversation
            for j in range(random.randint(4, 10)):
                sender_id = random.choice([seller.id, buyer.id])
                receiver_id = seller.id if sender_id == buyer.id else buyer.id

                message_types = ['text', 'offer'] if j < 7 else ['text', 'offer', 'deal']
                message_type = random.choice(message_types)

                if message_type == 'text':
                    message_content = random.choice(barter_messages)
                    offer_price = None
                elif message_type == 'offer':
                    offer_price = random.randint(int(product.estimated_value * 0.7), int(product.estimated_value * 1.2))
                    message_content = f'Saya tawarkan barter dengan nilai setara Rp {offer_price:,.0f} untuk {product.title}'
                else:  # deal
                    offer_price = random.randint(int(product.estimated_value * 0.8), int(product.estimated_value * 1.1))
                    message_content = f'Deal untuk barter dengan nilai Rp {offer_price:,.0f}! Lanjut ke proses selanjutnya.'

                chat_message = ChatMessage(
                    sender_id=sender_id,
                    receiver_id=receiver_id,
                    product_id=product.id,
                    conversation_id=conversation_id,
                    message=message_content,
                    message_type=message_type,
                    offer_price=offer_price,
                    is_read=random.choice([True, False]),
                    created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72))
                )
                db.session.add(chat_message)

            conversations_created += 1

        db.session.commit()

        print(f"✅ Created {created_products_count} products with detailed barter information")
        print(f"✅ Created {cart_entries} cart entries")
        print(f"✅ Created {proposals_created} barter proposals")
        print(f"✅ Created {conversations_created} chat conversations")

        print("\n" + "="*80)
        print("🔑 LOGIN CREDENTIALS - BARTERHUB PLATFORM")
        print("="*80)
        print("👑 ADMIN/OWNER:")
        print("   Username: admin | Password: admin123")
        print("   Role: Platform Administrator")
        print("\n🏪 SELLERS (25 Complete Stores with Premium Products):")
        for i, seller in enumerate(dummy_sellers):
            print(f"   {i+1:2d}. {seller['username']} | password123 | {seller['first_name']} {seller['last_name']}")

        print("\n👥 BUYERS (30 Active Buyers):")
        for i, buyer in enumerate(dummy_buyers):
            print(f"   {i+1:2d}. {buyer['username']} | password123 | {buyer['first_name']} {buyer['last_name']}")

        print("\n" + "="*80)
        print("🎯 FITUR BARTER SYSTEM YANG TERSEDIA")
        print("="*80)
        print("✅ Produk premium dengan informasi barter spesifik")
        print("✅ Multi-image products (sampai 3 gambar per produk)")
        print("✅ Sistem keranjang dengan add/remove functionality")
        print("✅ Barter proposals dengan sistem negosiasi")
        print("✅ Chat system dengan fitur offer/deal/counter-offer")
        print("✅ Exchange preferences yang detail untuk setiap produk")
        print("✅ Point system untuk valuasi barter yang fair")
        print("✅ Transaction receipts dan shipping details")
        print("✅ Real-time messaging dan notifications")
        print("✅ Sistem topup untuk balance barter")

        print("\n🏷️ SAMPLE BARTER SCENARIOS:")
        print("📱 Electronics ↔ Gadgets, Gaming PC, Laptops")
        print("👗 Fashion ↔ Luxury bags, Sneakers, Watches")
        print("🏠 Furniture ↔ Appliances, Electronics, Home decor")
        print("🚴 Sports ↔ Motorbikes, Gaming setups, Tech gadgets")
        print("📚 Books ↔ Tablets, Courses, Educational content")
        print("🎮 Toys ↔ Gaming consoles, Electronics, Collectibles")

        print(f"\n🎉 TOTAL DATA CREATED: {len(created_users)} Users, {created_products_count} Products")
        print("="*80)

if __name__ == '__main__':
    create_dummy_data()