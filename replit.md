# BarterHub - Marketplace Barter dengan Sistem Poin

## Overview

BarterHub adalah platform marketplace barter modern yang memungkinkan pengguna menukar barang tanpa menggunakan uang tunai. Sistem menggunakan algoritma poin otomatis untuk menentukan nilai wajar setiap produk berdasarkan faktor-faktor seperti kegunaan, kelangkaan, daya tahan, dan portabilitas. Platform ini menyediakan sistem chat real-time untuk negosiasi, manajemen transaksi yang komprehensif, dan dashboard admin untuk monitoring seluruh aktivitas.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 dengan Flask untuk server-side rendering
- **CSS Framework**: Bootstrap 5 dengan dark theme support dan Font Awesome icons
- **JavaScript**: Vanilla JavaScript untuk interaktivitas client-side, termasuk chat auto-refresh, form validations, dan image previews
- **Responsive Design**: Mobile-first approach dengan grid system Bootstrap

### Backend Architecture
- **Web Framework**: Flask dengan Blueprint pattern untuk modular route organization
- **Authentication**: Flask-Login untuk session management dengan role-based access control (admin, penjual, pembeli)
- **Forms**: Flask-WTF untuk form handling dan validation dengan CSRF protection
- **File Upload**: Secure file handling dengan PIL for image processing and resizing

### Database Design
- **ORM**: SQLAlchemy dengan declarative base pattern
- **Database**: PostgreSQL with connection pooling and health checks
- **Models**: User, Product, Category, ProductImage, ChatRoom, ChatMessage, Transaction, TransactionOffer
- **Relationships**: Complex many-to-many and one-to-many relationships for comprehensive data modeling

### Core Features
- **Point Calculation System**: Automated product valuation based on utility, scarcity, durability, and portability scores
- **Chat System**: Real-time messaging between buyers and sellers for negotiation
- **Transaction Management**: Complete workflow from offer creation to completion with status tracking
- **File Management**: Secure image upload with automatic resizing and organized storage
- **Admin Dashboard**: Comprehensive platform management with user, product, and transaction oversight

### Security Implementation
- **Password Security**: Werkzeug password hashing with salt
- **Session Management**: Secure session handling with configurable secret keys
- **File Security**: Filename sanitization and file type validation
- **CSRF Protection**: Built-in protection through Flask-WTF
- **Proxy Support**: ProxyFix middleware for proper URL generation behind reverse proxies

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and validation
- **WTForms**: Form field definitions and validators

### Database and Storage
- **PostgreSQL**: Primary database system
- **Pillow (PIL)**: Image processing and resizing
- **Werkzeug**: WSGI utilities and security helpers

### Frontend Assets
- **Bootstrap 5**: CSS framework loaded from CDN
- **Font Awesome 6**: Icon library loaded from CDN
- **Custom CSS**: Application-specific styling in static/css/style.css

### Production Considerations
- **Environment Variables**: DATABASE_URL and SESSION_SECRET for configuration
- **File Upload Limits**: 16MB maximum file size with organized directory structure
- **Logging**: Debug-level logging configuration for development and troubleshooting