# 🕹️ 8-BIT Vending Machine

\<p align="center">
&#x20; \<img src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bHphdzg3YmY5cmczY3VpcnliNHlnYmVnZnhqbWY4enJyeG43MHpnMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/uchGqpI5drRdK/giphy.gif" alt="8-BIT Vending Machine" width="800"/>
\</p>

> **🕹️ Buy snacks. Play games. Earn coins. Get your reward.**

---

## 🎯 What it does

**8-BIT Vending Machine** is a retro-inspired vending machine web application built as a **Database Management System project**.

Instead of simply inserting money and selecting a product, users earn virtual coins by playing mini-games and use those coins to purchase items from the vending machine.

The system includes:

- 🔐 User **Sign Up / Login**
- 🕹️ Mini-games for earning coins
- 🐍 **Snake Game**
- 🐢 **Turtle Race**
- 🪙 Coin-based purchasing system
- 🥤 Vending machine product selection
- 🧾 Purchase bills
- 📧 Email notifications/bills
- 🗄️ Database storage for users, games, coins, and purchases
- 👑 Admin dashboard for managing the vending machine
- 📊 Persistent records of system activity

The project is currently **under development**, so additional features and improvements may be added as development continues.

---

## 🕹️ How it works

The main idea is simple:

**Sign Up / Login → Play Games → Earn Coins → Choose Products → Purchase → Receive Bill**

### 1. 🔐 Create an account

Users can create an account through the **Sign Up** page and then log in to access the vending machine.

User information is stored in the PostgreSQL database.

### 2. 🕹️ Play games

Before purchasing products, users can earn coins by playing two mini-games:

- 🐍 **Snake**
- 🐢 **Turtle Race**

Each user gets **3 game chances per day**.

The better the user performs, the more coins they can earn.

### 3. 🪙 Earn coins

Game scores are converted into coins that can be used inside the vending machine.

For example:

```text
Better Score → More Coins → More Purchasing Power
```

Coins are stored and managed through the database so that the user's balance can be tracked.

### 4. 🥤 Purchase products

Once the user has enough coins, they can browse the available vending machine items and purchase products using their earned coins.

The system checks the user's available balance before completing the purchase.

### 5. 🧾 Generate a bill

After a successful purchase, the system generates a bill containing information such as:

- Customer
- Purchased products
- Quantity
- Price
- Total amount
- Purchase timestamp

The bill is also sent to the user's registered email address.

### 6. 🗄️ Store everything in the database

The project is designed around the database, so important operations are recorded rather than existing only temporarily.

Records include things such as:

- User accounts
- Game activity
- Scores
- Coins
- Products
- Purchases
- Purchase timestamps
- Bills / transaction information

This allows the system to maintain a history of activity and purchases.

---

## 👑 Admin Dashboard

The application includes a separate **Admin Dashboard** for managing the vending machine.

The dashboard is restricted to the designated administrator rather than being available to normal users.

The admin can manage vending machine contents and monitor database-related information.

Planned/admin functionality includes:

- 📦 Add or update products
- 💰 Update product prices
- 📊 View stored records
- 🧾 View purchase information
- 👥 Manage system data
- 🛠️ Maintain vending machine contents

The admin dashboard is separate from the normal user experience.

---

## 🗄️ Database

The project uses **PostgreSQL** as its database.

The database stores the persistent information required by the vending machine system.

The application uses **SQLAlchemy** to communicate with PostgreSQL from the Flask backend.

A simplified flow looks like this:

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                       Login / Signup
                             │
                             ▼
                    ┌─────────────────┐
                    │    Game System  │
                    └────────┬────────┘
                             │
                       Score → Coins
                             │
                             ▼
                    ┌─────────────────┐
                    │ Vending Machine│
                    └────────┬────────┘
                             │
                         Purchase
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
          PostgreSQL Database       Email Bill
```

Every important transaction is intended to be recorded in the database.

---

## 📁 Project Structure

```text
8-bit/
│
├── 8-BIT
│
├── 
│
├── 
│
├── uv.lock
│
├── .python-version
├── pyproject.toml
├── .gitignore
└── README.md
```

> The project structure may change as new features are implemented.

---

## ⚙️ Tech Stack

### Backend

- **Python**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLAlchemy**
- **PostgreSQL**

### Frontend

- **HTML**
- **CSS**
- **JavaScript**

### Other

- **Jinja2** — Dynamic HTML templates
- **Werkzeug** — Password hashing and security utilities
- **python-dotenv** — Environment variable management
- **Email services** — Sending purchase bills and notifications

---

## 🔑 Authentication

The application provides separate user authentication functionality.

### User

Users can:

- Sign up
- Log in
- Play games
- Earn coins
- Purchase products
- Receive purchase bills

### Admin

The administrator has access to the protected admin area and can manage the vending machine.

The admin dashboard is not intended to be accessible to ordinary users.

---

## 🐍 Snake Game

The Snake Game is one of the two mini-games used to earn coins.

The player controls the snake and attempts to achieve the highest possible score.

```text
Play Snake
     ↓
  Get Score
     ↓
Convert Score → Coins
     ↓
Use Coins → Purchase
```

Each user has a limited number of game attempts per day.

---

## 🐢 Turtle Race

The Turtle Race is the second mini-game.

Players participate in a race and receive a score/reward based on their performance.

The game provides another way for users to earn coins before purchasing products.

---

## 🪙 Coin System

Coins act as the virtual currency of the vending machine.

Users earn coins through gameplay and spend them on products.

The basic concept is:

```text
                    GAME
                      │
                      ▼
                    SCORE
                      │
                      ▼
                    COINS
                      │
                      ▼
                 BUY PRODUCT
                      │
                      ▼
              UPDATE DATABASE
```

The system keeps track of the user's coin balance so purchases can be validated.

---

## 🧾 Purchase System

When a user purchases an item:

1. The system checks the user's available coins.
2. The selected product and quantity are determined.
3. The total purchase cost is calculated.
4. The user's coin balance is updated.
5. The purchase is recorded in PostgreSQL.
6. A bill is generated.
7. The bill is sent to the user's registered email.

This makes the purchase a complete database transaction rather than simply displaying a successful message.

---

## 📧 Email Notifications

The application can use the user's registered email address to send purchase-related information.

The main purpose is to deliver the purchase bill after a successful transaction.

Additional notification features may be added as the project develops.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 5/8-bit"
```

### 2. Install dependencies

```bash
uv sync
```

This creates the project's virtual environment and installs the dependencies defined in `pyproject.toml`.

### 3. Configure PostgreSQL

Make sure **PostgreSQL** is installed and running on your system.

Create a PostgreSQL database for the project:

```text
Database: vending_machine
```

Then configure the database connection in the `.env` file so Flask-SQLAlchemy can connect to PostgreSQL.

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
SECRET_KEY=

DATABASE_URL=
```

> Do not commit `.env` or any credentials to GitHub.

### 5. Run the application

```bash
uv run python app.py
```

The Flask development server will then start locally.

## 📝 Development Status

🚧 **This project is currently under development.**

The core concept and database architecture are being developed incrementally.

### Current / Planned Features

- [x] Flask application
- [x] PostgreSQL database
- [x] SQLAlchemy integration
- [x] User authentication structure
- [ ] Complete Sign Up / Login UI
- [ ] User dashboard
- [ ] Snake Game
- [ ] Turtle Race
- [ ] Daily 3-game limit
- [ ] Coin reward system
- [ ] Vending machine interface
- [ ] Product purchasing
- [ ] Purchase history
- [ ] Bill generation
- [ ] Email bill delivery
- [ ] Protected admin dashboard
- [ ] Admin product management
- [ ] Expanded database records
- [ ] UI/UX improvements

The checklist will be updated as development progresses.

---

## 🔒 Security & Data

The project uses environment variables for sensitive configuration such as:

- Database credentials
- Flask secret key
- Email credentials

Sensitive files and local database-related files are excluded from version control.

Passwords are handled using secure password hashing rather than storing plain-text passwords.

---

## 💡 Future Improvements

Possible future additions include:

- 🏆 Leaderboards for game scores
- 🎮 More mini-games
- 🎁 Daily rewards
- 🪙 Different coin/reward systems
- 📦 Product inventory tracking
- 📈 Admin statistics and analytics
- 🧾 Improved invoice generation
- 📧 More email notifications
- 👤 User purchase history
- 🔐 Improved admin authentication
- 🎨 More detailed 8-bit animations and effects
- 📱 Better responsive design

---

## 🎯 Project Goal

The goal of **8-BIT Vending Machine** is to combine a fun retro gaming experience with a practical database-driven application.

Rather than creating a simple vending machine interface, the project demonstrates how multiple components can work together:

```text
Frontend
   ↓
Flask Backend
   ↓
Business Logic
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
Persistent Records
```

The gaming system, virtual currency, vending machine, authentication, admin management, and purchase system all operate as parts of one database-backed application.

---

> **🕹️ Play hard. Score high. Earn coins. Get your snacks.**

> *"In this vending machine, you don't just buy your snacks — you earn them."* 🚀
