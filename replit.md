# Overview

BarterHub is a modern web-based marketplace application built with Flask that enables users to trade goods without monetary exchange. The platform allows users to list items, browse available products, communicate through messages, and propose barter exchanges. It features user authentication, product management with image uploads, categorization, and a complete barter proposal system with administrative oversight.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework Architecture
- **Flask-based MVC pattern**: Uses Flask as the core web framework with SQLAlchemy ORM for database operations
- **Template-driven UI**: Server-side rendering using Jinja2 templates with Bootstrap 5 for responsive design
- **Session-based authentication**: Implements Flask-Login for user session management and authentication
- **File upload handling**: Supports image uploads with file validation and secure filename handling

## Database Design
- **SQLAlchemy ORM**: Uses Flask-SQLAlchemy with declarative base for database modeling
- **Relational data structure**: Implements User, Product, Category, Message, and BarterProposal models with proper foreign key relationships
- **User management**: Includes password hashing with Werkzeug, user roles (admin/regular), and account status tracking
- **Product catalog**: Features categorized products with condition tracking, availability status, and image storage

## Authentication & Authorization
- **Flask-Login integration**: Handles user sessions, login/logout functionality, and protected routes
- **Role-based access**: Distinguishes between regular users and administrators with different permission levels
- **Password security**: Uses Werkzeug for secure password hashing and verification
- **Session management**: Configurable session secrets and proxy-aware middleware for deployment

## File Management
- **Static file serving**: Organized structure for CSS, JavaScript, and uploaded images
- **Upload validation**: Restricts file types to common image formats with size limitations
- **Secure filename handling**: Uses Werkzeug's secure_filename for safe file storage

## Frontend Architecture
- **Bootstrap 5 framework**: Responsive design with modern UI components and utilities
- **Font Awesome icons**: Consistent iconography throughout the application
- **Progressive enhancement**: JavaScript for image previews, form validation, and interactive elements
- **Mobile-responsive design**: Adaptive layout for various screen sizes

## Admin Panel
- **Comprehensive dashboard**: Overview statistics and management interfaces
- **User management**: Admin capabilities for managing user accounts and status
- **Transaction oversight**: Monitoring and management of barter proposals and exchanges

# External Dependencies

## Core Web Framework
- **Flask**: Main web application framework
- **Flask-SQLAlchemy**: Database ORM and management
- **Flask-Login**: User authentication and session management

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6**: Icon library for consistent visual elements

## Security & Utilities
- **Werkzeug**: Password hashing, secure filename handling, and proxy middleware
- **SQLAlchemy**: Database abstraction layer with connection pooling

## Database
- **PostgreSQL**: Primary database system (configured via DATABASE_URL environment variable)
- **Connection pooling**: Configured with pool_recycle and pool_pre_ping for reliability

## File Storage
- **Local filesystem**: Image uploads stored in static/uploads directory
- **File validation**: Built-in support for common image formats (PNG, JPG, JPEG, GIF)

## Environment Configuration
- **Environment variables**: SESSION_SECRET for session management and DATABASE_URL for database connection
- **Development server**: Built-in Flask development server with debug mode support