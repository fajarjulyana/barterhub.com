import random
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Product, Category, ProductImage
from datetime import datetime, timedelta

def create_dummy_data():
    """Create dummy users and products for testing"""

    with app.app_context():
        # Drop all tables and recreate to ensure proper structure
        db.drop_all()
        db.create_all()

        print("Database tables recreated successfully")

        # Create dummy sellers (10)
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
            }
        ]

        # Create dummy buyers (10)
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
            }
        ]

        # Create admin/owner
        admin_user = {
            'username': 'admin',
            'email': 'admin@fajarmandiri.store',
            'password': 'admin123',
            'first_name': 'Fajar',
            'last_name': 'Julyana',
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
        print(f"Created users - Sellers: 10, Buyers: 10, Admin: 1")

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

        # Realistic products data for bartering with images
        # Note: seller_index maps to the index in the dummy_sellers list
        # Note: category maps to the category name
        products_data = [
            # Elektronik (andi_elektronik)
            {
                'title': 'Samsung Galaxy A54 5G',
                'description': 'HP Android flagship samsung, RAM 8GB, storage 256GB, kondisi mulus, fullset box charger',
                'condition': 'Like New',
                'estimated_value': 4500000,
                'category': 'Elektronik',
                'utility_score': 9,
                'scarcity_score': 6,
                'durability_score': 8,
                'portability_score': 9,
                'seller_index': 0,
                'images': [
                    'https://images.samsung.com/is/image/samsung/p6pim/id/2302/gallery/id-galaxy-a54-5g-a546-sm-a546elvgxid-535072803',
                    'https://images.samsung.com/is/image/samsung/p6pim/id/sm-a546elvgxid/gallery/id-galaxy-a54-5g-a546-sm-a546elvgxid-thumb-535072801',
                    'https://images.samsung.com/is/image/samsung/p6pim/id/sm-a546elvgxid/gallery/id-galaxy-a54-5g-a546-sm-a546elvgxid-thumb-535072802'
                ]
            },
            {
                'title': 'MacBook Air M1 2020',
                'description': 'Laptop Apple silicon M1, RAM 8GB, SSD 256GB, untuk kerja dan desain grafis, battery health 92%',
                'condition': 'Good',
                'estimated_value': 12000000,
                'category': 'Elektronik',
                'utility_score': 10,
                'scarcity_score': 7,
                'durability_score': 9,
                'portability_score': 8,
                'seller_index': 0,
                'images': [
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-space-gray-select-201810',
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-m2-midnight-gallery5-202206?wid=1000&hei=800&fmt=jpeg&qlt=90&.v=1654720222143'
                ]
            },

            # Fashion (sari_fashion)
            {
                'title': 'Dress Batik Modern Premium',
                'description': 'Dress batik kombinasi modern, bahan katun premium, ukuran M, cocok untuk acara formal dan casual',
                'condition': 'New',
                'estimated_value': 350000,
                'category': 'Pakaian & Aksesoris',
                'utility_score': 7,
                'scarcity_score': 8,
                'durability_score': 7,
                'portability_score': 9,
                'seller_index': 1,
                'images': [
                    'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
                ]
            },
            {
                'title': 'Tas Kulit Asli Handmade',
                'description': 'Tas selempang kulit sapi asli, handmade, warna coklat vintage, ukuran sedang',
                'condition': 'New',
                'estimated_value': 450000,
                'category': 'Pakaian & Aksesoris',
                'utility_score': 8,
                'scarcity_score': 9,
                'durability_score': 9,
                'portability_score': 8,
                'seller_index': 1,
                'images': [
                    'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                    'https://images.unsplash.com/photo-1573869475268-748b86d1f13e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },

            # Rumah Tangga (budi_prasetyo)
            {
                'title': 'Rice Cooker Miyako 1.8L',
                'description': 'Rice cooker digital, kapasitas 1.8L, fungsi warming, anti lengket, garansi masih berlaku 6 bulan',
                'condition': 'Like New',
                'estimated_value': 280000,
                'category': 'Rumah & Taman',
                'utility_score': 9,
                'scarcity_score': 4,
                'durability_score': 8,
                'portability_score': 6,
                'seller_index': 2,
                'images': [
                    'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },
            {
                'title': 'Set Peralatan Masak Teflon',
                'description': 'Set lengkap wajan, panci, spatula teflon anti lengket, 7 pieces, kondisi terawat',
                'condition': 'Good',
                'estimated_value': 320000,
                'category': 'Rumah & Taman',
                'utility_score': 8,
                'scarcity_score': 5,
                'durability_score': 7,
                'portability_score': 5,
                'seller_index': 2,
                'images': [
                    'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
                    'https://images.unsplash.com/photo-1621704582869-8630196309f5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },

            # Olahraga (rini_sport)
            {
                'title': 'Sepeda Lipat United Stylo',
                'description': 'Sepeda lipat 20 inch, 7 speed, cocok untuk commuting dan rekreasi, berat 12kg',
                'condition': 'Good',
                'estimated_value': 1800000,
                'category': 'Olahraga & Outdoor',
                'utility_score': 8,
                'scarcity_score': 6,
                'durability_score': 8,
                'portability_score': 7,
                'seller_index': 3,
                'images': [
                    'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },
            {
                'title': 'Matras Yoga Premium + Tas',
                'description': 'Matras yoga anti slip, tebal 6mm, eco-friendly material, bonus tas bawaan',
                'condition': 'New',
                'estimated_value': 180000,
                'category': 'Olahraga & Outdoor',
                'utility_score': 7,
                'scarcity_score': 5,
                'durability_score': 8,
                'portability_score': 8,
                'seller_index': 3,
                'images': [
                    'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },

            # Buku (dani_bookstore)
            {
                'title': 'Koleksi Buku Programming 10 Judul',
                'description': 'Set buku programming: Python, JavaScript, React, Node.js, database, algoritma, kondisi sangat baik',
                'condition': 'Like New',
                'estimated_value': 650000,
                'category': 'Buku & Media',
                'utility_score': 8,
                'scarcity_score': 7,
                'durability_score': 6,
                'portability_score': 6,
                'seller_index': 4,
                'images': [
                    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },
            {
                'title': 'Novel Tere Liye Set 12 Buku',
                'description': 'Koleksi lengkap novel Tere Liye, termasuk serial Bumi, Bulan, Matahari, kondisi mint',
                'condition': 'New',
                'estimated_value': 480000,
                'category': 'Buku & Media',
                'utility_score': 6,
                'scarcity_score': 8,
                'durability_score': 7,
                'portability_score': 7,
                'seller_index': 4,
                'images': [
                    'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },

            # Mainan (lisa_toys)
            {
                'title': 'LEGO Creator 3-in-1 Deep Sea',
                'description': 'LEGO Creator set 31088, 3 model dalam 1 set, lengkap semua pieces, box original',
                'condition': 'Like New',
                'estimated_value': 420000,
                'category': 'Mainan & Permainan',
                'utility_score': 6,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 7,
                'seller_index': 5,
                'images': [
                    'https://images.unsplash.com/photo-1558060370-d644479cb6f7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },
            {
                'title': 'Drone Mini untuk Pemula',
                'description': 'Drone kamera HD, mudah dikontrol, battery life 15 menit, cocok untuk belajar',
                'condition': 'Good',
                'estimated_value': 380000,
                'category': 'Mainan & Permainan',
                'utility_score': 7,
                'scarcity_score': 6,
                'durability_score': 6,
                'portability_score': 8,
                'seller_index': 5,
                'images': [
                    'https://images.unsplash.com/photo-1473968512647-3e447244af8f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                    'https://images.unsplash.com/photo-1517976478377-437c0406a76c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },

            # Otomotif (agus_motor)
            {
                'title': 'Helm Full Face KYT RC7',
                'description': 'Helm full face racing, ukuran L, SNI certified, visor jernih, padding masih empuk',
                'condition': 'Good',
                'estimated_value': 650000,
                'category': 'Otomotif',
                'utility_score': 9,
                'scarcity_score': 5,
                'durability_score': 9,
                'portability_score': 7,
                'seller_index': 6,
                'images': [
                    'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80' # Re-using an image, but this would be a different product image
                ]
            },
            {
                'title': 'Toolkit Motor Lengkap 42 Pcs',
                'description': 'Set peralatan service motor, kunci ring, pas, obeng, socket, dalam box organizer',
                'condition': 'New',
                'estimated_value': 280000,
                'category': 'Otomotif',
                'utility_score': 8,
                'scarcity_score': 4,
                'durability_score': 9,
                'portability_score': 6,
                'seller_index': 6,
                'images': [
                    'https://images.unsplash.com/photo-1581094794329-c8112a89af12?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },

            # Kesehatan & Kecantikan (dewi_beauty)
            {
                'title': 'Skincare Set Korea Lengkap',
                'description': 'Set skincare 7 step: cleanser, toner, serum, moisturizer, sunscreen, eye cream, sleeping mask',
                'condition': 'New',
                'estimated_value': 450000,
                'category': 'Kesehatan & Kecantikan',
                'utility_score': 8,
                'scarcity_score': 7,
                'durability_score': 5,
                'portability_score': 8,
                'seller_index': 7,
                'images': [
                    'https://images.unsplash.com/photo-1596462502278-27bfdc403348?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },
            {
                'title': 'Hair Dryer Professional 2000W',
                'description': 'Hair dryer salon grade, 3 speed 2 heat, ionic technology, diffuser attachment',
                'condition': 'Like New',
                'estimated_value': 320000,
                'category': 'Kesehatan & Kecantikan',
                'utility_score': 7,
                'scarcity_score': 5,
                'durability_score': 8,
                'portability_score': 6,
                'seller_index': 7,
                'images': [
                    'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },

            # Koleksi (eko_collector)
            {
                'title': 'Action Figure Naruto Set 6 Karakter',
                'description': 'Figure Naruto, Sasuke, Sakura, Kakashi, Gaara, Itachi, tinggi 15cm, detail bagus',
                'condition': 'New',
                'estimated_value': 380000,
                'category': 'Koleksi',
                'utility_score': 5,
                'scarcity_score': 9,
                'durability_score': 8,
                'portability_score': 8,
                'seller_index': 8,
                'images': [
                    'https://images.unsplash.com/photo-1601814933824-fd0b574dd592?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                    'https://images.unsplash.com/photo-1622980435270-2999201d1554?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },
            {
                'title': 'Kartu Pokemon TCG Booster Box',
                'description': '1 box booster Pokemon TCG Paldea Evolved, 36 pack, sealed, perfect untuk collector',
                'condition': 'New',
                'estimated_value': 1200000,
                'category': 'Koleksi',
                'utility_score': 4,
                'scarcity_score': 10,
                'durability_score': 9,
                'portability_score': 9,
                'seller_index': 8,
                'images': [
                    'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },

            # Vintage (maya_vintage)
            {
                'title': 'Kamera Film Analog Canon AE-1',
                'description': 'Kamera film vintage Canon AE-1, kondisi fungsi normal, lensa 50mm f/1.4, light meter ok',
                'condition': 'Good',
                'estimated_value': 2800000,
                'category': 'Koleksi',
                'utility_score': 6,
                'scarcity_score': 9,
                'durability_score': 7,
                'portability_score': 7,
                'seller_index': 9,
                'images': [
                    'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                    'https://images.unsplash.com/photo-1517047161187-b1959875836e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            },
            {
                'title': 'Jam Dinding Antik Kayu Jati',
                'description': 'Jam dinding vintage kayu jati ukir, mesin normal, pendulum berfungsi, diameter 35cm',
                'condition': 'Good',
                'estimated_value': 850000,
                'category': 'Rumah & Taman',
                'utility_score': 6,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 4,
                'seller_index': 9,
                'images': [
                    'https://images.unsplash.com/photo-1563861826100-9cb8668fdbe1c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
                ]
            }
        ]

        # Get sellers (non-admin users from the first 10)
        sellers = [u for u in created_users if not u.is_admin][:10]

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

            product = Product(
                title=product_data['title'],
                description=product_data['description'],
                condition=product_data['condition'],
                estimated_value=product_data['estimated_value'],
                category_id=category.id,
                owner_id=seller.id,
                image_url=product_data.get('image_url'),  # Keep for backward compatibility, though less used now
                utility_score=product_data['utility_score'],
                scarcity_score=product_data['scarcity_score'],
                durability_score=product_data['durability_score'],
                portability_score=product_data['portability_score'],
                seasonal_factor=random.uniform(0.9, 1.1),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
            )

            # Calculate barter value
            product.update_barter_value()

            db.session.add(product)
            db.session.flush() # Flush to get product.id before creating ProductImage

            # Create ProductImage records if images are provided
            images = product_data.get('images', [])
            
            # If no 'images' list but 'image_url' exists, use that as the primary image
            if not images and product_data.get('image_url'):
                images = [product_data['image_url']]

            for idx, image_url in enumerate(images[:5]):  # Limit to a maximum of 5 images per product
                product_image = ProductImage(
                    product_id=product.id,
                    image_url=image_url,
                    is_primary=(idx == 0) # Set the first image as primary
                )
                db.session.add(product_image)
            
            created_products_count += 1

        db.session.commit()
        print(f"Created {created_products_count} realistic products for bartering")
        print("\n=== LOGIN CREDENTIALS ===")
        print("ADMIN/OWNER:")
        print("Username: admin | Password: admin123")
        print("Developer: Fajar Julyana (fajarmandiri.store)")
        print("\nSELLERS (10):")
        for i, seller in enumerate(dummy_sellers):
            print(f"{i+1}. {seller['username']} | password123 | {seller['first_name']} {seller['last_name']}")
        print("\nBUYERS (10):")
        for i, buyer in enumerate(dummy_buyers):
            print(f"{i+1}. {buyer['username']} | password123 | {buyer['first_name']} {buyer['last_name']}")
        print("\n=== BARTER ITEMS SUMMARY ===")
        print("✓ Elektronik: Samsung Galaxy, MacBook Air")
        print("✓ Fashion: Dress Batik, Tas Kulit")
        print("✓ Rumah Tangga: Rice Cooker, Set Teflon")
        print("✓ Olahraga: Sepeda Lipat, Matras Yoga")
        print("✓ Buku: Programming Books, Novel Tere Liye")
        print("✓ Mainan: LEGO Creator, Drone Mini")
        print("✓ Otomotif: Helm KYT, Toolkit Motor")
        print("✓ Kecantikan: Skincare Korea, Hair Dryer")
        print("✓ Koleksi: Figure Naruto, Pokemon TCG")
        print("✓ Vintage: Kamera Canon, Jam Antik")

if __name__ == '__main__':
    create_dummy_data()