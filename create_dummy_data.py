
import random
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Product, Category, ProductImage, BarterProposal, Cart, ChatMessage, ChatConversation
from datetime import datetime, timedelta

def create_dummy_data():
    """Create complete dummy stores with multi-image products and full cart system"""

    with app.app_context():
        # Drop all tables and recreate to ensure proper structure
        db.drop_all()
        db.create_all()

        print("Database tables recreated successfully")

        # Create dummy sellers (15 complete stores)
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
            }
        ]

        # Create dummy buyers (20)
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
        print(f"Created users - Sellers: 15, Buyers: 20, Admin: 1")

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

        # Complete products data with multiple images
        products_data = [
            # Elektronik Store (elektronik_jakarta)
            {
                'title': 'Samsung Galaxy S23 Ultra 256GB',
                'description': 'HP Samsung flagship terbaru, RAM 12GB, storage 256GB, kamera 200MP, S-Pen included, kondisi mulus seperti baru',
                'condition': 'Like New',
                'estimated_value': 15000000,
                'category': 'Elektronik',
                'utility_score': 10,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 9,
                'seller_index': 0,
                'images': [
                    'https://images.samsung.com/is/image/samsung/p6pim/id/2302/gallery/id-galaxy-s23-ultra-s918-sm-s918bzkgxid-534848995?$650_519_PNG$',
                    'https://images.samsung.com/is/image/samsung/p6pim/id/sm-s918bzkgxid/gallery/id-galaxy-s23-ultra-s918-sm-s918bzkgxid-thumb-534849004?wid=520&hei=520&fmt=png',
                    'https://images.samsung.com/is/image/samsung/p6pim/id/sm-s918bzkgxid/gallery/id-galaxy-s23-ultra-s918-sm-s918bzkgxid-thumb-534849005?wid=520&hei=520&fmt=png',
                    'https://images.samsung.com/is/image/samsung/p6pim/id/sm-s918bzkgxid/gallery/id-galaxy-s23-ultra-s918-sm-s918bzkgxid-thumb-534849006?wid=520&hei=520&fmt=png'
                ]
            },
            {
                'title': 'MacBook Pro M2 14 inch 512GB',
                'description': 'Laptop Apple silicon M2 Pro, RAM 16GB, SSD 512GB, untuk kerja berat dan editing video, battery cycle count rendah',
                'condition': 'Good',
                'estimated_value': 28000000,
                'category': 'Elektronik',
                'utility_score': 10,
                'scarcity_score': 9,
                'durability_score': 10,
                'portability_score': 8,
                'seller_index': 0,
                'images': [
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp-spacegray-select-202206?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1664497359481',
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-gallery3-202206?wid=2000&hei=1536&fmt=jpeg&qlt=80&.v=1664497374218',
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-gallery4-202206?wid=2000&hei=1536&fmt=jpeg&qlt=80&.v=1664497374121'
                ]
            },
            {
                'title': 'iPad Pro 11 inch M2 WiFi 128GB',
                'description': 'Tablet Apple iPad Pro dengan chip M2, layar Liquid Retina, support Apple Pencil 2, kondisi sangat baik',
                'condition': 'Like New',
                'estimated_value': 12000000,
                'category': 'Elektronik',
                'utility_score': 9,
                'scarcity_score': 7,
                'durability_score': 9,
                'portability_score': 10,
                'seller_index': 0,
                'images': [
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-pro-11-select-wifi-spacegray-202210?wid=940&hei=1112&fmt=png-alpha&.v=1664411207213',
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-pro-11-gallery2-202210?wid=2000&hei=1500&fmt=jpeg&qlt=80&.v=1664578394544',
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-pro-11-gallery3-202210?wid=2000&hei=1500&fmt=jpeg&qlt=80&.v=1664578394544'
                ]
            },

            # Fashion Store (fashion_bandung)
            {
                'title': 'Dress Batik Modern Premium Kombinasi',
                'description': 'Dress batik kombinasi modern dengan aksen bordir, bahan katun premium, ukuran M, cocok untuk acara formal dan casual',
                'condition': 'New',
                'estimated_value': 450000,
                'category': 'Pakaian & Aksesoris',
                'utility_score': 8,
                'scarcity_score': 9,
                'durability_score': 7,
                'portability_score': 9,
                'seller_index': 1,
                'images': [
                    'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1566479179817-c98b9e0de31f?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1469334031218-e382a71b716b?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            {
                'title': 'Tas Kulit Asli Handmade Vintage',
                'description': 'Tas selempang kulit sapi asli, handmade berkualitas tinggi, warna coklat vintage, ukuran sedang dengan banyak compartment',
                'condition': 'New',
                'estimated_value': 650000,
                'category': 'Pakaian & Aksesoris',
                'utility_score': 8,
                'scarcity_score': 9,
                'durability_score': 10,
                'portability_score': 8,
                'seller_index': 1,
                'images': [
                    'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1573869475268-748b86d1f13e?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1584917865442-de89df76afd3?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1590736969955-71cc94901144?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # Rumah Tangga Store (rumah_tangga_solo)
            {
                'title': 'Rice Cooker Digital Miyako 1.8L Premium',
                'description': 'Rice cooker digital premium, kapasitas 1.8L, 8 fungsi masak, anti lengket, garansi resmi masih berlaku 1 tahun',
                'condition': 'Like New',
                'estimated_value': 380000,
                'category': 'Rumah & Taman',
                'utility_score': 9,
                'scarcity_score': 5,
                'durability_score': 8,
                'portability_score': 6,
                'seller_index': 2,
                'images': [
                    'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1585515656811-1b98e591ad25?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1556909114-35ba1a813fec?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            {
                'title': 'Set Peralatan Masak Teflon Premium 12 Pcs',
                'description': 'Set lengkap peralatan masak teflon premium: wajan, panci berbagai ukuran, spatula, tutup kaca, anti lengket berkualitas tinggi',
                'condition': 'Good',
                'estimated_value': 520000,
                'category': 'Rumah & Taman',
                'utility_score': 8,
                'scarcity_score': 6,
                'durability_score': 7,
                'portability_score': 5,
                'seller_index': 2,
                'images': [
                    'https://images.unsplash.com/photo-1621704582869-8630196309f5?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1556909114-35ba1a813fec?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1609501676725-7186f734b3fa?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # Olahraga Store (olahraga_surabaya)
            {
                'title': 'Sepeda Lipat United Stylo 7 Speed',
                'description': 'Sepeda lipat 20 inch, 7 speed Shimano, rangka alloy, cocok untuk commuting dan rekreasi, berat 12kg, sangat mudah dilipat',
                'condition': 'Good',
                'estimated_value': 2200000,
                'category': 'Olahraga & Outdoor',
                'utility_score': 9,
                'scarcity_score': 6,
                'durability_score': 8,
                'portability_score': 8,
                'seller_index': 3,
                'images': [
                    'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1544191696-15693be54e94?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1571068316344-75bc76f77890?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1571068316273-9013f9e2e2cd?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            {
                'title': 'Set Gym Equipment Home Workout Complete',
                'description': 'Set lengkap alat gym rumahan: dumbell adjustable, matras yoga, resistance band, pull up bar, push up board',
                'condition': 'New',
                'estimated_value': 1800000,
                'category': 'Olahraga & Outdoor',
                'utility_score': 8,
                'scarcity_score': 7,
                'durability_score': 9,
                'portability_score': 6,
                'seller_index': 3,
                'images': [
                    'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1517963628607-235ccdd5476c?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # Buku Store (buku_yogya)
            {
                'title': 'Koleksi Buku Programming Complete 15 Judul',
                'description': 'Set buku programming terlengkap: Python, JavaScript, React, Node.js, database, algoritma, machine learning, kondisi sangat baik semua',
                'condition': 'Like New',
                'estimated_value': 850000,
                'category': 'Buku & Media',
                'utility_score': 9,
                'scarcity_score': 8,
                'durability_score': 6,
                'portability_score': 6,
                'seller_index': 4,
                'images': [
                    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # Mainan Store (mainan_medan)
            {
                'title': 'LEGO Creator 3-in-1 Deep Sea Creatures',
                'description': 'LEGO Creator set 31088, 3 model dalam 1 set (hiu, cumi-cumi, ikan koi), lengkap semua pieces 230 pcs, box original masih ada',
                'condition': 'Like New',
                'estimated_value': 520000,
                'category': 'Mainan & Permainan',
                'utility_score': 7,
                'scarcity_score': 8,
                'durability_score': 10,
                'portability_score': 7,
                'seller_index': 5,
                'images': [
                    'https://images.unsplash.com/photo-1558060370-d644479cb6f7?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1587654780291-39c9404d746b?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1566041510394-cf7c8fe21800?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # Otomotif Store (otomotif_makassar)
            {
                'title': 'Helm Full Face KYT RC7 Size L',
                'description': 'Helm full face racing KYT RC7, ukuran L, SNI dan DOT certified, visor jernih anti fog, padding masih empuk dan bersih',
                'condition': 'Good',
                'estimated_value': 750000,
                'category': 'Otomotif',
                'utility_score': 10,
                'scarcity_score': 6,
                'durability_score': 9,
                'portability_score': 7,
                'seller_index': 6,
                'images': [
                    'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1609630875171-b1321377ee65?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1609630875403-8e36661c0b4e?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # Kecantikan Store (kecantikan_bali)
            {
                'title': 'Skincare Set Korea K-Beauty Lengkap 10 Step',
                'description': 'Set skincare Korea lengkap 10 step: oil cleanser, foam cleanser, toner, essence, serum, moisturizer, sunscreen, eye cream, sleeping mask',
                'condition': 'New',
                'estimated_value': 650000,
                'category': 'Kesehatan & Kecantikan',
                'utility_score': 8,
                'scarcity_score': 7,
                'durability_score': 5,
                'portability_score': 8,
                'seller_index': 7,
                'images': [
                    'https://images.unsplash.com/photo-1596462502278-27bfdc403348?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # Koleksi Store (koleksi_semarang)
            {
                'title': 'Action Figure Naruto Shippuden Set 8 Karakter',
                'description': 'Figure Naruto Shippuden: Naruto, Sasuke, Sakura, Kakashi, Gaara, Itachi, Minato, Jiraiya, tinggi 15cm, detail sangat bagus, original',
                'condition': 'New',
                'estimated_value': 580000,
                'category': 'Koleksi',
                'utility_score': 6,
                'scarcity_score': 9,
                'durability_score': 8,
                'portability_score': 8,
                'seller_index': 8,
                'images': [
                    'https://images.unsplash.com/photo-1601814933824-fd0b574dd592?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1622980435270-2999201d1554?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },

            # Vintage Store (vintage_palembang)
            {
                'title': 'Kamera Film Analog Canon AE-1 Program',
                'description': 'Kamera film vintage Canon AE-1 Program, kondisi fungsi normal semua, lensa 50mm f/1.4, light meter akurat, include case kulit',
                'condition': 'Good',
                'estimated_value': 3200000,
                'category': 'Koleksi',
                'utility_score': 7,
                'scarcity_score': 10,
                'durability_score': 7,
                'portability_score': 7,
                'seller_index': 9,
                'images': [
                    'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1517047161187-b1959875836e?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?ixlib=rb-4.0.3&w=800&q=80'
                ]
            }
        ]

        # Create more products for all sellers
        additional_products = [
            # More Elektronik products
            {
                'title': 'iPhone 14 Pro Max 256GB Purple',
                'description': 'iPhone 14 Pro Max warna Deep Purple, storage 256GB, kondisi sangat baik, fullset box charger, garansi iBox',
                'condition': 'Like New',
                'estimated_value': 18000000,
                'category': 'Elektronik',
                'utility_score': 10,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 9,
                'seller_index': 0,
                'images': [
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-14-pro-model-unselect-gallery-1-202209?wid=5120&hei=2880&fmt=webp&qlt=90&.v=1660753617560',
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-14-pro-model-unselect-gallery-2-202209?wid=5120&hei=2880&fmt=webp&qlt=90&.v=1660753617475'
                ]
            },
            # More Fashion products
            {
                'title': 'Jaket Kulit Premium Motor Biker Style',
                'description': 'Jaket kulit asli untuk motor, style biker classic, warna hitam, ukuran L, banyak zipper detail, sangat stylish',
                'condition': 'Good',
                'estimated_value': 850000,
                'category': 'Pakaian & Aksesoris',
                'utility_score': 7,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 8,
                'seller_index': 1,
                'images': [
                    'https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1520975954732-35dd22299614?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # Furniture products
            {
                'title': 'Sofa Minimalis 3 Seater Fabric Premium',
                'description': 'Sofa minimalis 3 dudukan, bahan fabric premium abu-abu, rangka kayu solid, sangat nyaman dan berkualitas',
                'condition': 'Like New',
                'estimated_value': 3500000,
                'category': 'Rumah & Taman',
                'utility_score': 8,
                'scarcity_score': 6,
                'durability_score': 9,
                'portability_score': 3,
                'seller_index': 10,
                'images': [
                    'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # Computer products
            {
                'title': 'Gaming PC RTX 4070 i7-13700F Complete',
                'description': 'PC Gaming lengkap: i7-13700F, RTX 4070, 32GB RAM, SSD 1TB, monitor 27 inch 144Hz, keyboard mechanical, mouse gaming',
                'condition': 'Like New',
                'estimated_value': 25000000,
                'category': 'Elektronik',
                'utility_score': 10,
                'scarcity_score': 8,
                'durability_score': 9,
                'portability_score': 4,
                'seller_index': 11,
                'images': [
                    'https://images.unsplash.com/photo-1587831990711-23ca6441447b?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1593640408182-31c70c8268f5?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # Shoes products
            {
                'title': 'Sepatu Sneakers Nike Air Jordan 1 Mid',
                'description': 'Sepatu Nike Air Jordan 1 Mid warna Chicago, ukuran 42, kondisi sangat baik, original 100%, box masih ada',
                'condition': 'Good',
                'estimated_value': 2800000,
                'category': 'Pakaian & Aksesoris',
                'utility_score': 8,
                'scarcity_score': 9,
                'durability_score': 8,
                'portability_score': 9,
                'seller_index': 12,
                'images': [
                    'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&w=800&q=80',
                    'https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&w=800&q=80'
                ]
            },
            # Gadget products
            {
                'title': 'Apple Watch Series 8 45mm GPS Cellular',
                'description': 'Apple Watch Series 8 ukuran 45mm, GPS + Cellular, warna Midnight, include sport band dan milanese loop, kondisi mulus',
                'condition': 'Like New',
                'estimated_value': 8500000,
                'category': 'Elektronik',
                'utility_score': 9,
                'scarcity_score': 7,
                'durability_score': 8,
                'portability_score': 10,
                'seller_index': 14,
                'images': [
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/watch-s8-gps-cellular-midnight-aluminum-midnight-sport-band-unselect-gallery-1-202209?wid=5120&hei=3280&fmt=webp&qlt=90&.v=1660783244772',
                    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/watch-s8-gps-cellular-midnight-aluminum-midnight-sport-band-unselect-gallery-2-202209?wid=5120&hei=3280&fmt=webp&qlt=90&.v=1660783239815'
                ]
            }
        ]

        # Combine all products
        all_products_data = products_data + additional_products

        # Get sellers (non-admin users from the first 15)
        sellers = [u for u in created_users if not u.is_admin][:15]

        # Create products
        created_products_count = 0
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

            # Add exchange preferences to description for clear seller intent
            enhanced_description = f"{product_data['description']}\n\n💡 **YANG SAYA INGINKAN UNTUK TUKAR:**\n"
            
            # Generate realistic exchange preferences based on product category and value
            if product_data['category'] == 'Elektronik':
                if product_data['estimated_value'] > 10000000:  # High value electronics
                    enhanced_description += f"• Smartphone flagship + uang Rp {random.randint(1000000, 5000000):,}\n• Laptop gaming setara nilai\n• Kombinasi elektronik + cash"
                else:
                    enhanced_description += f"• Smartphone kondisi baik + uang Rp {random.randint(500000, 2000000):,}\n• Tablet/iPad + aksesoris\n• Kamera mirrorless"
            elif product_data['category'] == 'Pakaian & Aksesoris':
                enhanced_description += f"• Tas branded original\n• Sepatu sneakers limited edition\n• Aksesoris emas/perak + uang Rp {random.randint(200000, 1000000):,}"
            elif product_data['category'] == 'Rumah & Taman':
                enhanced_description += f"• Peralatan elektronik rumah tangga\n• Furniture setara + ongkir\n• Uang cash Rp {random.randint(300000, 1500000):,}"
            elif product_data['category'] == 'Olahraga & Outdoor':
                enhanced_description += f"• Sepeda lipat/gunung\n• Peralatan fitness + uang Rp {random.randint(500000, 2000000):,}\n• Gadget olahraga (smartwatch, dll)"
            elif product_data['category'] == 'Buku & Media':
                enhanced_description += f"• Koleksi buku programming/bisnis\n• Tablet untuk baca + uang Rp {random.randint(200000, 800000):,}\n• Kindle/e-reader"
            elif product_data['category'] == 'Mainan & Permainan':
                enhanced_description += f"• LEGO set lain ukuran setara\n• Console game + games\n• Action figure premium + cash Rp {random.randint(150000, 600000):,}"
            elif product_data['category'] == 'Otomotif':
                enhanced_description += f"• Aksesoris motor original\n• Helm branded + jaket touring\n• Tools otomotif professional + cash"
            elif product_data['category'] == 'Kesehatan & Kecantikan':
                enhanced_description += f"• Skincare set Korea premium\n• Alat kecantikan + produk branded\n• Supplement kesehatan + cash Rp {random.randint(200000, 800000):,}"
            elif product_data['category'] == 'Koleksi':
                enhanced_description += f"• Action figure/collectible setara nilai\n• Kamera vintage + aksesoris\n• Koleksi hobi lain + cash Rp {random.randint(300000, 2000000):,}"
            else:
                enhanced_description += f"• Barang setara nilai dan kondisi\n• Uang cash Rp {random.randint(200000, 1000000):,}\n• Nego via chat untuk diskusi detail"
            
            enhanced_description += f"\n📝 **CATATAN**: Bisa nego dan diskusi alternatif lain. Hubungi saya via chat untuk detail lebih lanjut!"

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
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )

            # Calculate barter value
            product.update_barter_value()

            db.session.add(product)
            db.session.flush() # Flush to get product.id before creating ProductImage

            # Create ProductImage records
            images = product_data.get('images', [])
            
            for idx, image_url in enumerate(images[:5]):  # Limit to a maximum of 5 images per product
                product_image = ProductImage(
                    product_id=product.id,
                    image_url=image_url,
                    is_primary=(idx == 0) # Set the first image as primary
                )
                db.session.add(product_image)
            
            created_products_count += 1

        db.session.commit()

        # Create realistic cart entries for buyers
        buyers = [u for u in created_users if u.user_role == 'buyer'][:20]
        all_products = Product.query.all()
        
        cart_entries = 0
        for buyer in buyers[:10]:  # First 10 buyers have items in cart
            # Each buyer adds 2-5 random products to cart
            num_items = random.randint(2, 5)
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
        for i in range(20):  # Create 20 realistic proposals
            buyer = random.choice(buyers)
            product = random.choice(all_products)
            
            if product.owner_id != buyer.id:
                # Buyer's own products for offering
                buyer_products = Product.query.filter_by(owner_id=buyer.id).all()
                if not buyer_products:
                    # If buyer has no products, create one for them
                    dummy_product = Product(
                        title=f'Produk {buyer.first_name}',
                        description=f'Produk yang dimiliki oleh {buyer.get_full_name()}',
                        condition='Good',
                        estimated_value=random.randint(100000, 1000000),
                        category_id=random.choice(categories).id,
                        owner_id=buyer.id,
                        utility_score=random.randint(5, 8),
                        scarcity_score=random.randint(4, 7),
                        durability_score=random.randint(5, 8),
                        portability_score=random.randint(6, 9)
                    )
                    dummy_product.update_barter_value()
                    db.session.add(dummy_product)
                    db.session.flush()
                    buyer_products = [dummy_product]
                
                offered_product = random.choice(buyer_products)
                
                proposal = BarterProposal(
                    proposer_id=buyer.id,
                    receiver_id=product.owner_id,
                    offered_product_id=offered_product.id,
                    wanted_product_id=product.id,
                    message=f'Halo, saya tertarik dengan {product.title}. Apakah bisa ditukar dengan {offered_product.title}?',
                    status=random.choice(['pending', 'accepted', 'rejected', 'negotiating']),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
                )
                db.session.add(proposal)
                proposals_created += 1

        # Create chat conversations and messages
        conversations_created = 0
        for i in range(15):  # Create 15 chat conversations
            seller = random.choice(sellers)
            buyer = random.choice(buyers)
            product = random.choice([p for p in all_products if p.owner_id == seller.id])
            
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
            
            # Create chat messages for this conversation
            for j in range(random.randint(3, 8)):
                sender_id = random.choice([seller.id, buyer.id])
                receiver_id = seller.id if sender_id == buyer.id else buyer.id
                
                message_types = ['text', 'offer'] if j < 5 else ['text', 'offer', 'deal']
                message_type = random.choice(message_types)
                
                if message_type == 'text':
                    message_content = random.choice([
                        f'Halo, saya tertarik dengan {product.title}',
                        'Apakah masih tersedia?',
                        'Kondisinya bagaimana?',
                        'Bisa nego harga?',
                        'Lokasi dimana?',
                        'Terima kasih infonya'
                    ])
                    offer_price = None
                elif message_type == 'offer':
                    offer_price = random.randint(int(product.estimated_value * 0.7), int(product.estimated_value * 1.2))
                    message_content = f'Saya tawarkan harga Rp {offer_price:,.0f} untuk {product.title}'
                else:  # deal
                    offer_price = random.randint(int(product.estimated_value * 0.8), int(product.estimated_value * 1.1))
                    message_content = f'Deal untuk harga Rp {offer_price:,.0f}!'
                
                chat_message = ChatMessage(
                    sender_id=sender_id,
                    receiver_id=receiver_id,
                    product_id=product.id,
                    conversation_id=conversation_id,
                    message=message_content,
                    message_type=message_type,
                    offer_price=offer_price,
                    is_read=random.choice([True, False]),
                    created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
                )
                db.session.add(chat_message)
            
            conversations_created += 1

        db.session.commit()
        
        print(f"Created {created_products_count} products with multiple images")
        print(f"Created {cart_entries} cart entries")
        print(f"Created {proposals_created} barter proposals")
        print(f"Created {conversations_created} chat conversations")
        
        print("\n=== LOGIN CREDENTIALS ===")
        print("ADMIN/OWNER:")
        print("Username: admin | Password: admin123")
        print("Developer: Fajar Julyana (fajarmandiri.store)")
        print("\nSELLERS (15 Complete Stores):")
        for i, seller in enumerate(dummy_sellers):
            print(f"{i+1}. {seller['username']} | password123 | {seller['first_name']} {seller['last_name']}")
        print("\nBUYERS (20):")
        for i, buyer in enumerate(dummy_buyers):
            print(f"{i+1}. {buyer['username']} | password123 | {buyer['first_name']} {buyer['last_name']}")
        
        print("\n=== BARTER SYSTEM FEATURES ===")
        print("✓ Multi-image products (up to 5 images per product)")
        print("✓ Complete cart system with add/remove functionality")
        print("✓ Barter proposals with negotiation system")
        print("✓ Chat system with offer/deal features")
        print("✓ Order confirmation system for sellers")
        print("✓ Shipping cost calculation and tracking")
        print("✓ Transaction receipts and shipping details")
        print("✓ Real-time messaging and notifications")

if __name__ == '__main__':
    create_dummy_data()
