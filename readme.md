# Social Media API 🚀

A professional Twitter/Instagram-like social media backend API built with FastAPI, SQLAlchemy, and JWT authentication.

## Features ✨

- 🔐 **JWT Authentication** - Secure token-based authentication with access and refresh tokens
- 👤 **User Management** - Complete user profile management (CRUD operations)
- 🎭 **Role-Based Access Control** - Admin, Moderator, and User roles with customizable permissions
- 🔍 **User Search** - Search users by username or full name
- 📊 **User Statistics** - Followers, following, and posts count
- 🔒 **Security** - Password hashing with bcrypt, token validation, permission checks
- 📝 **API Documentation** - Auto-generated Swagger/OpenAPI documentation
- 🗄️ **Database** - SQLAlchemy ORM with SQLite (easily switchable to PostgreSQL)

## Tech Stack 💻

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **JWT** - JSON Web Tokens for authentication
- **Bcrypt** - Password hashing
- **Uvicorn** - Lightning-fast ASGI server

## Project Structure 📁
```
auth-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py          # Authentication endpoints
│   │           ├── users.py         # User management endpoints
│   │           └── roles.py         # Role management endpoints
│   ├── core/
│   │   ├── config.py                # App configuration
│   │   ├── hashing.py               # Password hashing utilities
│   │   ├── jwt.py                   # JWT token handlers
│   │   └── security.py              # Security dependencies
│   ├── db/
│   │   ├── base.py                  # Base model class
│   │   ├── session.py               # Database session
│   │   └── models/
│   │       ├── user.py              # User model
│   │       └── role.py              # Role model
│   ├── schemas/
│   │   ├── auth.py                  # Auth schemas (Pydantic)
│   │   ├── user.py                  # User schemas
│   │   └── role.py                  # Role schemas
│   ├── services/
│   │   ├── auth_service.py          # Authentication business logic
│   │   └── user_service.py          # User business logic
│   └── main.py                      # FastAPI application
├── .env                              # Environment variables
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Installation 🛠️

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd auth-service
```

### 2. Create virtual environment (optional but recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Create a `.env` file in the root directory:
```env
# Database
DATABASE_URL=sqlite:///./social_media.db

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
PROJECT_NAME=Social Media API
VERSION=1.0.0
DESCRIPTION=Twitter/Instagram like social media backend API
```

### 5. Run the application
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation 📖

Once the application is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints 🛣️

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | ❌ |
| POST | `/api/v1/auth/login` | Login user | ❌ |
| POST | `/api/v1/auth/refresh` | Refresh access token | ❌ |
| POST | `/api/v1/auth/logout` | Logout user | ❌ |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/users/me` | Get current user profile | ✅ |
| PUT | `/api/v1/users/me` | Update current user profile | ✅ |
| PUT | `/api/v1/users/me/password` | Change password | ✅ |
| DELETE | `/api/v1/users/me` | Deactivate account | ✅ |
| GET | `/api/v1/users/me/stats` | Get current user stats | ✅ |
| GET | `/api/v1/users/search` | Search users | ❌ |
| GET | `/api/v1/users/{username}` | Get user profile by username | ❌ |

### Roles (Admin Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/roles` | Create new role | ✅ Admin |
| GET | `/api/v1/roles` | List all roles | ❌ |
| GET | `/api/v1/roles/{id}` | Get role details | ❌ |
| PUT | `/api/v1/roles/{id}` | Update role | ✅ Admin |
| DELETE | `/api/v1/roles/{id}` | Delete role | ✅ Admin |

## Usage Examples 💡

### Register a new user
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Get current user profile (with token)
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Search users
```bash
curl -X GET "http://localhost:8000/api/v1/users/search?q=john&limit=10"
```

## Authentication Flow 🔐

1. **Register/Login** → Receive `access_token` (30 min) and `refresh_token` (7 days)
2. **API Requests** → Include `Authorization: Bearer <access_token>` in headers
3. **Token Expires** → Use `refresh_token` to get new `access_token`
4. **Logout** → Delete tokens from client-side storage

## Development 🔧

### Run with auto-reload
```bash
uvicorn app.main:app --reload
```

### Run on different port
```bash
uvicorn app.main:app --reload --port 5000
```

### Run with multiple workers (production)
```bash
uvicorn app.main:app --workers 4
```

## Database Migration 📊

Currently using SQLite for development. To switch to PostgreSQL:

1. Install PostgreSQL
2. Update `.env`:
```env
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```
3. Install psycopg2:
```bash
   pip install psycopg2-binary
```

## Security Considerations 🔒

- ✅ Passwords are hashed with bcrypt
- ✅ JWT tokens with expiration
- ✅ CORS protection
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Input validation with Pydantic
- ⚠️ Change `SECRET_KEY` in production!
- ⚠️ Use HTTPS in production
- ⚠️ Use PostgreSQL in production (not SQLite)

## Future Features 🚀

- [ ] Posts and comments system
- [ ] Follow/unfollow functionality
- [ ] Like system
- [ ] Timeline/feed algorithm
- [ ] Notifications
- [ ] Media upload (images/videos)
- [ ] Real-time messaging (WebSockets)
- [ ] Email verification
- [ ] Password reset
- [ ] OAuth (Google, GitHub)

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.


---

# Sosyal Medya API 🚀

FastAPI, SQLAlchemy ve JWT kimlik doğrulaması ile oluşturulmuş profesyonel Twitter/Instagram benzeri sosyal medya backend API'si.

## Özellikler ✨

- 🔐 **JWT Kimlik Doğrulama** - Access ve refresh token'ları ile güvenli token tabanlı kimlik doğrulama
- 👤 **Kullanıcı Yönetimi** - Tam kullanıcı profil yönetimi (CRUD işlemleri)
- 🎭 **Rol Tabanlı Erişim Kontrolü** - Özelleştirilebilir izinlerle Admin, Moderatör ve Kullanıcı rolleri
- 🔍 **Kullanıcı Arama** - Kullanıcı adı veya tam isimle kullanıcı arama
- 📊 **Kullanıcı İstatistikleri** - Takipçi, takip edilen ve gönderi sayıları
- 🔒 **Güvenlik** - Bcrypt ile şifre hashleme, token doğrulama, izin kontrolleri
- 📝 **API Dokümantasyonu** - Otomatik oluşturulan Swagger/OpenAPI dokümantasyonu
- 🗄️ **Veritabanı** - SQLite ile SQLAlchemy ORM (kolayca PostgreSQL'e geçilebilir)

## Teknoloji Yığını 💻

- **FastAPI** - API oluşturmak için modern, hızlı web framework'ü
- **SQLAlchemy** - SQL toolkit ve ORM
- **Pydantic** - Python tip belirteçleri kullanarak veri doğrulama
- **JWT** - Kimlik doğrulama için JSON Web Token'ları
- **Bcrypt** - Şifre hashleme
- **Uvicorn** - Çok hızlı ASGI sunucusu

## Proje Yapısı 📁
```
auth-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py          # Kimlik doğrulama endpoint'leri
│   │           ├── users.py         # Kullanıcı yönetim endpoint'leri
│   │           └── roles.py         # Rol yönetim endpoint'leri
│   ├── core/
│   │   ├── config.py                # Uygulama yapılandırması
│   │   ├── hashing.py               # Şifre hashleme araçları
│   │   ├── jwt.py                   # JWT token işleyicileri
│   │   └── security.py              # Güvenlik bağımlılıkları
│   ├── db/
│   │   ├── base.py                  # Temel model sınıfı
│   │   ├── session.py               # Veritabanı oturumu
│   │   └── models/
│   │       ├── user.py              # Kullanıcı modeli
│   │       └── role.py              # Rol modeli
│   ├── schemas/
│   │   ├── auth.py                  # Auth şemaları (Pydantic)
│   │   ├── user.py                  # Kullanıcı şemaları
│   │   └── role.py                  # Rol şemaları
│   ├── services/
│   │   ├── auth_service.py          # Kimlik doğrulama iş mantığı
│   │   └── user_service.py          # Kullanıcı iş mantığı
│   └── main.py                      # FastAPI uygulaması
├── .env                              # Ortam değişkenleri
├── requirements.txt                  # Python bağımlılıkları
└── README.md                         # Bu dosya
```

## Kurulum 🛠️

### 1. Repository'yi klonlayın
```bash
git clone <your-repo-url>
cd auth-service
```

### 2. Sanal ortam oluşturun (opsiyonel ama önerilir)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 4. `.env` dosyası oluşturun

Kök dizinde bir `.env` dosyası oluşturun:
```env
# Veritabanı
DATABASE_URL=sqlite:///./social_media.db

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Uygulama
PROJECT_NAME=Social Media API
VERSION=1.0.0
DESCRIPTION=Twitter/Instagram benzeri sosyal medya backend API
```

### 5. Uygulamayı çalıştırın
```bash
uvicorn app.main:app --reload
```

API şu adreste çalışacak: `http://localhost:8000`

## API Dokümantasyonu 📖

Uygulama çalıştıktan sonra şu adresleri ziyaret edin:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoint'leri 🛣️

### Kimlik Doğrulama

| Method | Endpoint | Açıklama | Auth Gerekli |
|--------|----------|----------|--------------|
| POST | `/api/v1/auth/register` | Yeni kullanıcı kaydı | ❌ |
| POST | `/api/v1/auth/login` | Kullanıcı girişi | ❌ |
| POST | `/api/v1/auth/refresh` | Access token yenileme | ❌ |
| POST | `/api/v1/auth/logout` | Kullanıcı çıkışı | ❌ |

### Kullanıcılar

| Method | Endpoint | Açıklama | Auth Gerekli |
|--------|----------|----------|--------------|
| GET | `/api/v1/users/me` | Mevcut kullanıcı profilini getir | ✅ |
| PUT | `/api/v1/users/me` | Mevcut kullanıcı profilini güncelle | ✅ |
| PUT | `/api/v1/users/me/password` | Şifre değiştir | ✅ |
| DELETE | `/api/v1/users/me` | Hesabı devre dışı bırak | ✅ |
| GET | `/api/v1/users/me/stats` | Mevcut kullanıcı istatistikleri | ✅ |
| GET | `/api/v1/users/search` | Kullanıcı ara | ❌ |
| GET | `/api/v1/users/{username}` | Kullanıcı adıyla profil getir | ❌ |

### Roller (Sadece Admin)

| Method | Endpoint | Açıklama | Auth Gerekli |
|--------|----------|----------|--------------|
| POST | `/api/v1/roles` | Yeni rol oluştur | ✅ Admin |
| GET | `/api/v1/roles` | Tüm rolleri listele | ❌ |
| GET | `/api/v1/roles/{id}` | Rol detaylarını getir | ❌ |
| PUT | `/api/v1/roles/{id}` | Rol güncelle | ✅ Admin |
| DELETE | `/api/v1/roles/{id}` | Rol sil | ✅ Admin |

## Kullanım Örnekleri 💡

### Yeni kullanıcı kaydı
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe"
  }'
```

### Giriş yapma
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Mevcut kullanıcı profilini getir (token ile)
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer SIZIN_ACCESS_TOKEN"
```

### Kullanıcı ara
```bash
curl -X GET "http://localhost:8000/api/v1/users/search?q=john&limit=10"
```

## Kimlik Doğrulama Akışı 🔐

1. **Kayıt/Giriş** → `access_token` (30 dk) ve `refresh_token` (7 gün) alın
2. **API İstekleri** → Header'larda `Authorization: Bearer <access_token>` ekleyin
3. **Token Süresi Doldu** → Yeni `access_token` almak için `refresh_token` kullanın
4. **Çıkış** → Token'ları istemci tarafında silin

## Geliştirme 🔧

### Otomatik yenileme ile çalıştır
```bash
uvicorn app.main:app --reload
```

### Farklı port'ta çalıştır
```bash
uvicorn app.main:app --reload --port 5000
```

### Çoklu worker ile çalıştır (production)
```bash
uvicorn app.main:app --workers 4
```

## Veritabanı Geçişi 📊

Şu anda geliştirme için SQLite kullanılıyor. PostgreSQL'e geçmek için:

1. PostgreSQL'i yükleyin
2. `.env` dosyasını güncelleyin:
```env
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```
3. psycopg2'yi yükleyin:
```bash
   pip install psycopg2-binary
```

## Güvenlik Hususları 🔒

- ✅ Şifreler bcrypt ile hashleniyor
- ✅ Süresi dolan JWT token'ları
- ✅ CORS koruması
- ✅ SQL injection koruması (SQLAlchemy ORM)
- ✅ Pydantic ile input doğrulama
- ⚠️ Production'da `SECRET_KEY`'i değiştirin!
- ⚠️ Production'da HTTPS kullanın
- ⚠️ Production'da PostgreSQL kullanın (SQLite değil)

## Gelecek Özellikler 🚀

- [ ] Gönderiler ve yorumlar sistemi
- [ ] Takip et/takipten çık fonksiyonalitesi
- [ ] Beğeni sistemi
- [ ] Timeline/feed algoritması
- [ ] Bildirimler
- [ ] Medya yükleme (resim/video)
- [ ] Gerçek zamanlı mesajlaşma (WebSockets)
- [ ] Email doğrulama
- [ ] Şifre sıfırlama
- [ ] OAuth (Google, GitHub)

## Katkıda Bulunma 🤝

Katkılar memnuniyetle karşılanır! Lütfen Pull Request göndermekten çekinmeyin.

