# 🌍 Triplicity – Travel & Tour Booking Platform

Triplicity is a full-featured travel and tour booking platform built with **Django** and **PostgreSQL**, designed to provide users with seamless holiday discovery, booking, and payment capabilities. Whether you're booking a honeymoon, a trekking adventure, or a group getaway — Triplicity makes it easy.

---

## 🚀 Features

- **🔐 Modern User Authentication** – Email-based registration, login, profile, and dashboard
- **🏨 Hotel & Package Management** – Admin-manageable hotels and holiday packages
- **🔎 Category Browsing** – Browse by travel categories like honeymoon, trekking, family, etc.
- **📅 Booking System** – End-to-end bookings with dynamic pricing and history tracking
- **💳 Secure Payments** – Integrated with Stripe or Razorpay for live/test payments
- **📬 Email Notifications** – Transactional emails for sign-up and booking confirmations
- **🖥️ Responsive UI** – Clean, Bootstrap-based modern frontend
- **🛠️ Admin Console** – Full CRUD access for packages, users, reviews, and more

---

## 🛠 Tech Stack

- **Backend**: Python 3.12, Django 4.x
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, Bootstrap 5, FontAwesome
- **Payments**: Stripe
- **Email**: Gmail SMTP (or any compatible SMTP server)
- **Cloud Ready**: Deployed on Render.

---

## ⚡ Quickstart – Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/triplicity.git
cd triplicity/
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
# or use uv if preferred:
# uv venv .venv && source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
# or
uv pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the root directory:

```ini
SECRET_KEY=YourSecretKeyHere
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=triplicity_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@triplicity.com

STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
```

### 5. Migrate and Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🏗️ Project Structure

```
Triplicity/
│
├── triplicity/           # Core project settings and URLs
├── accounts/             # User registration, login, dashboard
├── home/                 # Homepage and landing views
├── packages/             # Packages by category
├── bookings/             # Booking & payment logic
├── templates/            # All HTML templates
│   ├── accounts/
│   ├── home/
│   ├── packages/
│   └── bookings/
├── static/               # CSS, JS, images
└── media/                # User-uploaded content
```

---

## 💼 Admin Console

Visit: http://127.0.0.1:8000/admin/  
Login using your superuser credentials.

**Manage:**
- Users
- Hotels & Packages
- Categories
- Bookings
- Reviews

---

## 💳 Payments

Stripe integration ensures secure, real-time transactions.
- Update `.env` with your test/live keys.
- Bookings only confirm after successful payment.

---

## 📧 Email Notifications

- Uses Gmail SMTP or any compatible service.
- Emails sent for registration and booking confirmations.
- Configurable in `.env`.

---

## ☁️ Deployment (Render)

Triplicity is ready for cloud deployment:
- One-click PostgreSQL setup
- Auto CI/CD from GitHub
- HTTPS, custom domains
- Set `DEBUG=False` in production
- Configure `.env` securely

**Production Checklist:**
- `DEBUG=False`
- Add your domain to `ALLOWED_HOSTS`
- Use cloud database & email credentials
- Enable SSL for DB connections
- Don't commit `.env` or secrets

---

## 🔐 Security Best Practices

- Always use a strong, unique `SECRET_KEY`
- Never commit `.env` to version control
- Set up HTTPS and database SSL in production
- Regularly update dependencies

---

## 🙋‍♂️ Support & Contributions

Got suggestions or issues?  
Open a PR or start a discussion!

Feel free to fork and modify as per your needs.

---

## 💡 Credits

Built with ❤️ by Anish Bawdhankar
MIT License – Free to use and modify

---

## ✈️ Happy Journey with Triplicity!
