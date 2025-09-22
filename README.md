# CodeVerseHub - Discord Community Programming Platform

A comprehensive competitive programming platform built with Django for Discord communities. CodeVerseHub provides coding contests, problem repositories, user progress tracking, and community features.

## 🚀 Features

### Core Features
- **User Authentication**: Custom user model with role-based permissions (Admin, Moderator, User)
- **Contest System**: Create, manage, and participate in coding contests
- **Problem Repository**: Extensive library of algorithmic problems with difficulty levels
- **Submission System**: Submit solutions in multiple programming languages
- **User Dashboard**: Personalized dashboard with statistics and progress tracking
- **Admin Panel**: Comprehensive administrative interface for platform management

### User Features
- User registration and profile management
- Contest participation and registration
- Problem solving with real-time submission feedback
- Personal statistics and achievement tracking
- Leaderboards and rankings
- Community interaction features

### Administrative Features
- Contest creation and management
- Problem creation with test cases
- User management and role assignment
- Platform analytics and statistics
- Content moderation tools

## 🛠 Technology Stack

- **Backend**: Django 5.0.7 (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Django's built-in authentication with custom User model
- **Forms**: Django Crispy Forms with Bootstrap4 theme
- **Static Files**: Bootstrap CDN, Font Awesome, Chart.js

## 📁 Project Structure

```
cvh/
├── codeversehub/           # Main Django project
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── main/                   # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── forms.py            # Django forms
│   ├── admin.py            # Admin configuration
│   ├── urls.py             # App URL patterns
│   └── migrations/         # Database migrations
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   └── main/               # App-specific templates
├── static/                 # Static files
│   ├── css/                # Custom CSS
│   ├── js/                 # Custom JavaScript
│   └── images/             # Images
├── media/                  # User uploads
├── requirements.txt        # Python dependencies
└── manage.py               # Django management script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cvh
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📊 Database Models

### User Model
- Custom user model extending AbstractUser
- Role-based permissions (Admin, Moderator, User)
- Profile information and statistics tracking
- Discord integration fields

### Contest Model
- Contest management with status tracking
- Support for individual and team contests
- Flexible scheduling and participant limits

### Problem Model
- Algorithmic problems with difficulty levels
- Tag system for categorization
- Test case management

### Submission Model
- Solution submissions with verdict tracking
- Multiple programming language support
- Execution time and memory usage tracking

## 🎯 User Roles and Permissions

### User (Default)
- Participate in contests
- Solve problems
- View personal statistics
- Access community features

### Moderator
- All User permissions
- Create and manage contests
- Create and manage problems
- Basic content moderation

### Administrator
- All Moderator permissions
- User management and role assignment
- Platform configuration
- Full admin panel access

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional) for environment-specific settings:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
```

### Settings Configuration
Key settings in `settings.py`:
- Database configuration
- Static files handling
- Media files configuration
- Authentication settings
- Crispy forms integration

## 📱 Pages and Features

### Public Pages
- **Home**: Platform overview and statistics
- **About**: Information about the platform
- **Rules**: Community guidelines and contest rules
- **FAQ**: Frequently asked questions
- **Resources**: Learning materials and references
- **Timeline**: Platform development roadmap

### Authenticated Pages
- **Dashboard**: Personalized user overview
- **Contests**: Contest listing and management
- **Problems**: Problem repository and submissions
- **Profile**: User profile and statistics

### Administrative Pages
- **Django Admin**: Full platform administration
- **Contest Creation**: Create and manage contests
- **Problem Creation**: Create and manage problems

## 🛡 Security Features

- CSRF protection on all forms
- User authentication and session management
- Role-based access control
- Input validation and sanitization
- Secure file uploads

## 📈 Future Enhancements

- Real-time code execution and evaluation
- Advanced analytics and reporting
- Mobile application
- API development
- Integration with external platforms
- Enhanced community features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is built for educational purposes and community use.

## 🆘 Support

For support and questions:
- Check the FAQ page
- Contact community moderators
- Open an issue in the repository

## 📝 Changelog

### Version 1.0.0 (September 2025)
- Initial release
- Complete user authentication system
- Contest and problem management
- User dashboard and statistics
- Administrative features
- Responsive design

---

**CodeVerseHub** - Built with ❤️ for the programming community