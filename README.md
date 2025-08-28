
# BarterHub - Platform Perdagangan Barter Modern

![BarterHub Logo](https://via.placeholder.com/800x200/667eea/ffffff?text=BarterHub+-+Platform+Perdagangan+Barter)

## Deskripsi Aplikasi

BarterHub adalah platform perdagangan barter modern yang memungkinkan pengguna untuk menukar barang tanpa menggunakan uang. Platform ini menghubungkan penjual dan pembeli dalam sistem pertukaran yang adil dan transparan dengan sistem poin barter yang canggih.

## Fitur Utama

### 🔐 Sistem Autentikasi & Otorisasi
- Registrasi pengguna dengan pilihan peran (Penjual/Pembeli)
- Login/logout dengan enkripsi password
- Sistem admin untuk pengelolaan platform
- Verifikasi akses berdasarkan peran

### 📦 Manajemen Produk
- Upload produk dengan multiple images
- Sistem kategorisasi produk
- Penilaian kondisi barang (New, Like New, Good, Fair, Poor)
- Sistem poin barter otomatis berdasarkan:
  - Utility Score (Tingkat kebutuhan)
  - Scarcity Score (Tingkat kelangkaan)
  - Durability Score (Daya tahan)
  - Portability Score (Kemudahan dibawa)
  - Seasonal Factor (Faktor musiman)

### 💬 Sistem Chat & Negosiasi
- Chat real-time antara penjual dan pembeli
- Sistem penawaran dan counter-offer
- Negosiasi harga dengan timeline
- Notifikasi pesan tidak terbaca

### 🛒 Sistem Keranjang & Checkout
- Keranjang belanja per penjual
- Checkout dengan sistem topup
- Pilihan pembayaran: Barang topup atau Tunai
- Detail formulir barang topup

### 📋 Sistem Transaksi
- Transaction receipt permanen
- Tracking pengiriman
- Konfirmasi deal dari kedua pihak
- Status tracking lengkap

### 🛡️ Panel Administrasi
- Dashboard overview dengan statistik
- Manajemen user (suspend/unsuspend)
- Monitoring transaksi
- Sistem pesan admin

## Alur Kerja Aplikasi

### 1. Registrasi & Setup
```
Pengguna Baru → Registrasi → Pilih Peran (Penjual/Pembeli) → Dashboard
```

### 2. Untuk Penjual
```
Login → Seller Dashboard → Add Product → Set Barter Points → Product Live
→ Receive Proposals → Negotiate → Accept Deal → Ship Product → Complete Transaction
```

### 3. Untuk Pembeli
```
Login → Buyer Dashboard → Browse Products → Add to Cart → Chat with Seller
→ Make Offer → Finalize Deal → Submit Topup Details → Wait Approval → Send Payment/Items
```

### 4. Sistem Poin Barter
```
Base Points = (Utility + Scarcity + Durability + Portability) × Seasonal Factor
Final Points = Base Points × Condition Modifier
```

### 5. Proses Transaksi
```
Initial Chat → Negotiation → Deal Agreement → Transaction Receipt
→ Topup Submission → Seller Approval → Shipping → Completion
```

## Struktur Database

### User Model
- Personal information (nama, email, phone)
- Role management (seller/buyer/admin)
- Status tracking (active, suspended, online)

### Product Model
- Product details dengan multiple images
- Barter value calculation
- Exchange preferences
- Availability status

### Chat System
- Real-time messaging
- Offer/counter-offer tracking
- Deal finalization
- Conversation grouping

### Transaction System
- Permanent receipt storage
- Shipping details
- Topup item management
- Status progression

## Aturan Hukum & Ketentuan Platform

### 🏛️ Dasar Hukum yang Berlaku

#### 1. Undang-Undang Perlindungan Konsumen
- **UU No. 8 Tahun 1999**: Melindungi hak konsumen dalam transaksi
- Kewajiban penjual memberikan informasi yang jujur dan akurat
- Hak pembeli mendapat barang sesuai deskripsi

#### 2. Undang-Undang Informasi dan Transaksi Elektronik
- **UU No. 11 Tahun 2008 jo. UU No. 19 Tahun 2016**: Mengatur transaksi elektronik
- Keabsahan kontrak elektronik
- Perlindungan data pribadi pengguna

#### 3. Kitab Undang-Undang Hukum Perdata
- **Pasal 1338**: Asas kebebasan berkontrak
- **Pasal 1365**: Tanggung jawab atas perbuatan melawan hukum
- **Pasal 1457**: Ketentuan jual beli (berlaku untuk barter)

### 📋 Ketentuan Platform BarterHub

#### Untuk Penjual:
1. **Kewajiban Penjual**:
   - Memberikan deskripsi produk yang akurat dan jujur
   - Upload foto asli produk (minimal 1, maksimal 5)
   - Menyebutkan kondisi barang dengan benar
   - Merespons chat pembeli dalam 24 jam
   - Mengirim barang sesuai kesepakatan

2. **Larangan Penjual**:
   - Menjual barang ilegal atau berbahaya
   - Memberikan informasi palsu tentang produk
   - Melakukan penipuan atau manipulasi harga
   - Menggunakan foto produk orang lain

3. **Sanksi Pelanggaran**:
   - Peringatan tertulis
   - Suspend akun 7-30 hari
   - Ban permanen untuk pelanggaran berat

#### Untuk Pembeli:
1. **Hak Pembeli**:
   - Mendapat informasi lengkap tentang produk
   - Negosiasi harga yang wajar
   - Membatalkan deal sebelum konfirmasi final
   - Komplain jika barang tidak sesuai

2. **Kewajiban Pembeli**:
   - Memberikan topup sesuai kesepakatan
   - Berkomunikasi dengan sopan
   - Konfirmasi penerimaan barang
   - Membayar ongkos kirim sesuai kesepakatan

3. **Sistem Topup**:
   - Wajib menyediakan barang pengganti jika memilih topup barang
   - Barang topup harus sesuai permintaan penjual
   - Estimasi nilai topup harus wajar dan sesuai market price

### ⚖️ Penyelesaian Sengketa

1. **Mediasi Internal**:
   - Admin platform sebagai mediator
   - Resolusi dalam 7 hari kerja
   - Keputusan berdasarkan bukti dan komunikasi

2. **Arbitrase**:
   - Jika mediasi gagal, dapat menggunakan arbitrase
   - Biaya arbitrase ditanggung pihak yang kalah

3. **Hukum yang Berlaku**:
   - Hukum Republik Indonesia
   - Yurisdiksi Pengadilan Negeri Jakarta Pusat

### 🛡️ Perlindungan Data & Privasi

1. **Data yang Dikumpulkan**:
   - Informasi pribadi (nama, email, nomor telepon)
   - Data transaksi dan komunikasi
   - Foto produk dan dokumen pendukung

2. **Penggunaan Data**:
   - Fasilitasi transaksi barter
   - Verifikasi identitas pengguna
   - Peningkatan layanan platform

3. **Keamanan Data**:
   - Enkripsi password dengan hash
   - Penyimpanan aman di server
   - Tidak dibagikan ke pihak ketiga tanpa izin

## Data Dummy untuk Testing

### Kategori Produk
- **Elektronik**: Smartphone, Laptop, Headphone, Camera
- **Pakaian & Aksesoris**: Baju, Sepatu, Tas, Jam tangan
- **Rumah & Taman**: Furnitur, Alat dapur, Tanaman, Dekorasi
- **Olahraga & Outdoor**: Sepeda, Alat fitness, Sepatu olahraga
- **Buku & Media**: Novel, Komik, DVD, Vinyl record
- **Mainan & Permainan**: Board game, Action figure, Puzzle
- **Otomotif**: Helm, Aksesoris motor, Tools
- **Kesehatan & Kecantikan**: Skincare, Parfum, Supplement
- **Koleksi**: Koin, Stamp, Trading cards
- **Lainnya**: Barang unik dan misc

### Contoh Produk dengan Sistem Poin

#### 1. iPhone 13 Pro (Kondisi: Like New)
- **Utility Score**: 9 (Sangat dibutuhkan)
- **Scarcity Score**: 7 (Cukup langka)
- **Durability Score**: 8 (Tahan lama)
- **Portability Score**: 9 (Mudah dibawa)
- **Seasonal Factor**: 1.0
- **Total Poin**: 33 × 1.1 (kondisi) = **36 poin**
- **Ingin ditukar dengan**: Gaming laptop atau Camera DSLR + cash

#### 2. Sepeda Gunung MTB (Kondisi: Good)
- **Utility Score**: 7 (Dibutuhkan untuk hobi)
- **Scarcity Score**: 5 (Standar)
- **Durability Score**: 9 (Sangat tahan lama)
- **Portability Score**: 3 (Sulit dibawa)
- **Seasonal Factor**: 1.2 (Musim olahraga)
- **Total Poin**: 24 × 1.2 × 1.0 = **29 poin**
- **Ingin ditukar dengan**: Peralatan camping atau motorcycle gear

#### 3. Koleksi Manga One Piece 1-100 (Kondisi: New)
- **Utility Score**: 6 (Untuk penggemar)
- **Scarcity Score**: 8 (Langka lengkap)
- **Durability Score**: 7 (Cukup tahan)
- **Portability Score**: 2 (Berat dan banyak)
- **Seasonal Factor**: 1.0
- **Total Poin**: 23 × 1.2 (kondisi) = **28 poin**
- **Ingin ditukar dengan**: Action figure anime atau gaming console

#### 4. Laptop Gaming ASUS ROG (Kondisi: Fair)
- **Utility Score**: 9 (Sangat dibutuhkan)
- **Scarcity Score**: 6 (Cukup umum)
- **Durability Score**: 6 (Perlu perawatan)
- **Portability Score**: 7 (Portable untuk laptop gaming)
- **Seasonal Factor**: 1.0
- **Total Poin**: 28 × 0.8 (kondisi) = **22 poin**
- **Ingin ditukar dengan**: MacBook atau PC components + monitor

#### 5. Jam Tangan Seiko Automatic (Kondisi: Good)
- **Utility Score**: 5 (Aksesoris)
- **Scarcity Score**: 7 (Vintage, agak langka)
- **Durability Score**: 9 (Sangat awet)
- **Portability Score**: 10 (Sangat mudah dibawa)
- **Seasonal Factor**: 1.0
- **Total Poin**: 31 × 1.0 = **31 poin**
- **Ingin ditukar dengan**: Jam tangan lain atau aksesoris premium

### Users Dummy

#### Penjual Aktif:
1. **Andi Pratama** (andipratama) - Penjual elektronik
2. **Sari Wijaya** (sariwijaya) - Penjual fashion & aksesoris
3. **Budi Santoso** (budisantoso) - Penjual hobi & koleksi
4. **Linda Chen** (lindachen) - Penjual rumah tangga
5. **Rizki Firmansyah** (rizkifirman) - Penjual otomotif

#### Pembeli Aktif:
1. **Maya Putri** (mayaputri) - Pencari gadget
2. **Tommy Setiawan** (tommysetiawan) - Kolektor anime
3. **Dewi Lestari** (dewilestari) - Fashion enthusiast
4. **Arief Rahman** (ariefrahman) - Gaming enthusiast
5. **Nina Suharto** (ninasuharto) - Home decorator

## Teknologi yang Digunakan

### Backend
- **Python Flask**: Web framework
- **SQLAlchemy**: ORM database
- **Flask-Login**: Authentication
- **Werkzeug**: Security & file handling
- **PostgreSQL**: Production database

### Frontend
- **Bootstrap 5**: CSS framework
- **Font Awesome**: Icons
- **JavaScript**: Interactive features
- **Jinja2**: Template engine

### Infrastructure
- **Replit**: Development & deployment platform
- **File uploads**: Local storage dengan validasi
- **Session management**: Flask sessions dengan secret key

## Instalasi & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL (untuk production)

### Installation Steps
```bash
# Clone repository
git clone <repository-url>
cd barterhub

# Install dependencies
pip install -r requirements.txt

# Setup database
python init_database.py

# Create dummy data (optional)
python create_dummy_data.py

# Run application
python main.py
```

### Environment Variables
```
DATABASE_URL=postgresql://username:password@host:port/database
SESSION_SECRET=your-secret-key-here
```

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Login process
- `GET /register` - Registration page
- `POST /register` - Registration process
- `GET /logout` - Logout

### Products
- `GET /browse` - Browse products
- `GET /product/<id>` - Product detail
- `GET /add_product` - Add product form
- `POST /add_product` - Create product

### Chat & Messaging
- `POST /send_chat_message` - Send chat message
- `GET /get_chat_messages/<conversation_id>` - Get conversation
- `POST /respond_to_offer` - Respond to offers
- `POST /finalize_deal` - Finalize deal

### Cart & Checkout
- `POST /add_to_cart/<product_id>` - Add to cart
- `GET /cart` - View cart
- `POST /process_checkout_seller/<seller_id>` - Checkout

### Admin
- `GET /admin` - Admin dashboard
- `GET /admin/users` - User management
- `POST /admin/suspend_user/<user_id>` - Suspend user

## Kontribusi

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

## Kontak

**Tim Pengembangan BarterHub**
- Email: admin@barterhub.com
- Website: https://barterhub.replit.app
- Support: /support (dalam aplikasi)

---

*BarterHub - Menghubungkan kebutuhan, membangun komunitas, tanpa uang tunai.*
