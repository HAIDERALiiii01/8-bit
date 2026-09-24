# 🕹️ 8-BIT Studios

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bHphdzg3YmY5cmczY3VpcnliNHlnYmVnZnhqbWY4enJyeG43MHpnMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/uchGqpI5drRdK/giphy.gif" alt="8-BIT Vending Machine" width="800"/>
</p>

<p align="center">
  <strong>🕹️ Play games. Earn coins. Buy snacks. Get rewarded.</strong>
</p>

---

## 🎯 About the Project

**8-BIT Studios** is a retro-inspired, database-driven vending machine web application developed as a **Database Management System (DBMS) project**.

Instead of simply inserting money into a vending machine, users earn virtual coins by playing mini-games. Those coins can then be used to purchase products from the vending machine.

The application combines:

- 🔐 User registration and authentication
- 🕹️ Mini-games
- 🪙 Virtual coin economy
- 🥤 Vending machine
- 🧾 Purchase and billing system
- 📧 Email bill delivery
- 🗄️ PostgreSQL database
- 👑 Admin management system
- 📊 Activity statistics and analytics

The entire system is connected through a Flask backend and uses PostgreSQL for persistent data storage.

---

## 🎮 How It Works

The core flow of the application is:

```text
Register
   ↓
Login
   ↓
Play Games
   ↓
Earn Coins
   ↓
Open Vending Machine
   ↓
Select Products
   ↓
Purchase with Coins
   ↓
Generate Bill
   ↓
Send Bill to Registered Gmail
```

### 1. 🔐 Register & Login

A new user creates an account by providing their required information.

After registration, the user can log in and access the main 8-BIT application.

User information and account data are stored in PostgreSQL.

---

### 2. 🕹️ Play Games

Users can earn coins by playing two mini-games:

- 🐍 **Snake**
- 🐢 **Turtle Race**

Each game contributes to the user's gaming activity and reward system.

The application also keeps records of game sessions, scores, coins earned, and play timestamps.

---

### 3. 🪙 Earn Coins

Players receive coins as rewards from gameplay.

The coins act as the virtual currency of the 8-BIT Studios.

```text
Game
  ↓
Score / Result
  ↓
Reward
  ↓
Coins
```

The user's coin balance is stored in the database and can be used for purchases.

---

### 4. 🥤 Use the Vending Machine

After earning enough coins, users can enter the vending machine and browse the available products.

Products include items such as:

- ☕ Chai
- ☕ Coffee
- 🥤 Coke
- 🥤 Pakola
- 🍟 Lays
- 🍫 Snickers
- 🥪 Egg Sandwich
- 🕹️ Extra Bit

Users can select products and quantities before completing their purchase.

---

### 5. 🧾 Purchase & Billing

When a user makes a purchase, the system:

1. Checks the user's available coins.
2. Determines the selected products and quantities.
3. Calculates the total cost.
4. Deducts the required coins.
5. Records the purchase in PostgreSQL.
6. Generates a purchase bill.
7. Sends the bill to the user's registered email address.

The purchase therefore becomes a persistent database transaction rather than simply displaying a success message.

---

### 6. 📧 Email Bill

After a successful purchase, the generated bill is sent to the user's registered **Gmail/email address**.

The bill contains information such as:

- Customer information
- Purchased products
- Quantity
- Product prices
- Total amount
- Purchase information
- Transaction timestamp

---

# 👑 Admin Panel

The application includes a protected admin area for managing and monitoring the 8-BIT system.

Unlike the normal user interface, the admin panel provides access to system-wide statistics, game controls, vending machine management, and user information.

## 📊 Admin Statistics

The admin can monitor important activity across the application, including:

### Users

- 👥 **Total registered players**
- 🎮 **Users who played games today**
- 🎯 **Total games played by users**

### Coins

- 🪙 **Total coins earned**
- 💰 **Total coins spent**
- 📈 **Coins earned today**
- 📉 **Coins spent today**

These statistics provide an overview of how the virtual economy is being used.

---

## 📈 Activity Analytics

The admin panel also provides recent activity information.

The dashboard displays:

- 🪙 Coin activity over the **past 5 days**
- 🎮 Game activity over the **past 5 days**

This makes it possible to observe recent changes in gameplay and the virtual coin economy.

---

## 🎮 Game Management

The admin can control the availability and reward behavior of games.

### Game Controls

Administrators can:

- Enable games
- Disable games
- Control game availability
- Configure game reward settings

This allows the administrator to control which games are currently available to users without changing the application's source code.

---

## 🥤 Vending Machine Management

The admin panel also provides management functionality for the vending machine.

Administrators can manage the available vending machine products and their related information.

This includes controlling the products presented to users and maintaining the vending machine's contents.

---

## 👥 Users

The admin can access an **All Users** section containing information about registered users.

This provides the administrator with an overview of the application's player accounts and their stored information.

---

# 🕹️ Games

## 🐍 Snake

The Snake game is one of the two ways users can earn coins.

The player controls a snake, collects food, and attempts to achieve a higher score.

```text
Play Snake
    ↓
Collect Food
    ↓
Increase Score
    ↓
Earn Coins
    ↓
Spend Coins
```

Game activity and rewards are recorded in the database.

---

## 🐢 Turtle Race

Turtle Race is the second game available in 8-BIT.

Players participate in a turtle race and receive rewards based on the game's result.

```text
Start Race
    ↓
Turtles Compete
    ↓
Race Result
    ↓
Reward Coins
```

The game provides an alternative way for users to earn virtual currency.

---

# 🪙 Coin System

Coins are the virtual currency used throughout the application.

Users earn coins through games and spend them on vending machine products.

```text
        🕹️ GAME
           │
           ▼
       GAME RESULT
           │
           ▼
       🪙 COINS EARNED
           │
           ▼
    🥤 VENDING MACHINE
           │
           ▼
      🧾 PURCHASE
           │
           ▼
    🪙 COINS SPENT
           │
           ▼
     🗄️ DATABASE
```

The database keeps track of coin activity so that the system can calculate balances, earnings, spending, and statistics.

---

# 🗄️ Database

**PostgreSQL** is used as the primary database for the application.

**Flask-SQLAlchemy / SQLAlchemy** provides the connection between the Flask application and PostgreSQL.

The database stores information related to:

- Users
- Games
- Game sessions
- Scores
- Coin rewards
- Products
- Orders
- Order items
- Purchases
- Inventory activity
- Timestamps
- Administrative information

This allows the application to maintain persistent records of user activity and transactions.

---

# 🏗️ Application Architecture

The project follows a database-backed Flask architecture:

```text
┌──────────────────────────┐
│        Frontend          │
│     HTML / CSS / JS      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       Flask Backend      │
│   Routes & Application   │
│         Logic            │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      SQLAlchemy ORM      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       PostgreSQL         │
│      Database            │
└──────────────────────────┘

             │
             ▼
      📧 Email Service
```

---

# 🛠️ Tech Stack

## Backend

- **Python**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLAlchemy**
- **PostgreSQL**

## Frontend

- **HTML**
- **CSS**
- **JavaScript**
- **Jinja2**

## Games

- **Python**
- **JavaScript**
- **HTML5/CSS**
- Game-specific assets and audio

## Utilities

- **python-dotenv** — environment variable management
- **Werkzeug** — password hashing and security utilities
- **Email/SMTP** — purchase bill delivery
- **uv** — Python project and dependency management

---

# 📁 Project Structure

```text
8-bit/
│
├── .venv/
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
│
├── 8-BIT/
│   │
│   ├── main.py
│   ├── auth.py
│   ├── dummy.py
│   ├── extensions.py
│   ├── models.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   └── register.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
│
├── favicon.png
│
└── bit/
    │
    ├── bit.py
    ├── __init__.py
    ├── dashboard.py
    ├── mail.py
    ├── vending_machine.py
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── images/
    │       ├── admin/
    │       ├── classic/
    │       ├── race/
    │       ├── snake/
    │       └── vend/
    │           ├── chai/
    │           ├── coffee/
    │           ├── coke/
    │           ├── egg-sandwich/
    │           ├── extra-bit/
    │           ├── Lays/
    │           ├── Pakola/
    │           └── Snickers/
    │
    ├── templates/
    │   ├── bit_base.html
    │   ├── bit.html
    │   ├── dashboard.html
    │   ├── dashboard_user.html
    │   ├── games.html
    │   └── vending_machine.html
    │
    └── games/
        │
        ├── game.py
        │
        ├── race/
        │   ├── race.py
        │   ├── static/
        │   │   └── bgm.mp3
        │   └── templates/
        │       └── race.html
        │
        └── snake/
            ├── snake.py
            ├── static/
            │   ├── bgm.mp3
            │   └── game_over.mp3
            └── templates/
                └── snake.html
```

---

# ⚙️ Getting Started

## Prerequisites

Before running the project, make sure you have:

- **Python 3.12+**
- **uv**
- **PostgreSQL**
- A Gmail/email account configured for sending purchase bills

---

## 1. Clone the Repository

```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss.git
```

Then navigate to the 8-BIT project directory.

```bash
cd "ProjecTss/Gear 5/8-bit"
```

---

## 2. Install Dependencies with uv

This project uses **uv** for Python dependency and virtual-environment management.

Run:

```bash
uv sync
```

`uv` will create the project's virtual environment and install the dependencies defined by `pyproject.toml`.

The committed `uv.lock` file ensures that the project's dependency versions can be reproduced consistently.

---

## 3. Configure PostgreSQL

Make sure PostgreSQL is installed and running.

Create a PostgreSQL database for the project.

For example:

```text
Database name:
vending_machine
```

The Flask application uses SQLAlchemy to communicate with PostgreSQL.

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```dotenv
SECRET_KEY=your_secret_key

DATABASE_URL=your_postgresql_connection_string

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_app_password
```

Use the actual environment variable names expected by your application configuration.

> **Important:** Never commit `.env`, database credentials, email credentials, API keys, or other secrets to GitHub.

---

## 5. Run the Application

Start the Flask application using `uv`:

```bash
uv run python main.py
```

The application will start using Flask's development server.

Open the local address shown in the terminal to access the application.

---

# 🔐 Authentication & Security

The application provides authentication for both normal users and administrators.

### Users can:

- Register
- Log in
- Access the 8-BIT application
- Play games
- Earn coins
- Purchase products
- Receive purchase bills

### Administrators can:

- Access the protected admin panel
- Monitor application statistics
- Manage vending machine products
- Enable/disable games
- Configure game rewards
- View user information
- Monitor recent game and coin activity

Passwords are handled using password hashing rather than being stored as plain text.

Sensitive configuration is kept in environment variables.

---

# 🧾 Purchase Flow

A complete purchase follows this process:

```text
User
 │
 ├── Select Product
 │
 ├── Select Quantity
 │
 ▼
Check Coin Balance
 │
 ▼
Calculate Total
 │
 ▼
Deduct Coins
 │
 ▼
Create Order
 │
 ▼
Create Order Items
 │
 ▼
Record Transaction
 │
 ▼
Generate Bill
 │
 ▼
Send Bill by Email
```

This ensures that the purchase is represented as an actual database transaction.

---

# 📊 Admin Activity Overview

The admin panel provides a high-level view of how the application is being used.

```text
              ADMIN PANEL
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
    USERS        COINS       GAMES
       │           │           │
       ▼           ▼           ▼
  Registered    Earned       Played
   Players       Spent       Today
       │           │           │
       └───────────┼───────────┘
                   ▼
            Recent Activity
               Past 5 Days
```

This turns the admin panel into more than a simple CRUD interface: it provides an overview of the application's users, virtual economy, games, and vending machine activity.

---

# 🎯 Project Goal

The goal of **8-BIT Studios** is to combine a retro gaming experience with a practical database management system.

Instead of building a simple vending machine, the project connects several systems together:

```text
Authentication
      ↓
Game System
      ↓
Coin Economy
      ↓
Vending Machine
      ↓
Purchase System
      ↓
Email Billing
      ↓
PostgreSQL
      ↓
Admin Analytics
```

The result is a complete database-backed application where gameplay, rewards, purchases, users, and administrative activity are connected through a single system.

---

# 🕹️ Final Flow

```text
        👤 REGISTER
             │
             ▼
         🔐 LOGIN
             │
             ▼
       🎮 PLAY GAMES
        ╱           ╲
       ▼             ▼
   🐍 SNAKE     🐢 TURTLE RACE
       ╲             ╱
        ▼           ▼
          🪙 EARN COINS
               │
               ▼
        🥤 VENDING MACHINE
               │
               ▼
         🛒 BUY PRODUCTS
               │
               ▼
         🧾 GENERATE BILL
               │
               ▼
          📧 EMAIL BILL
```

---

<p align="center">
  <strong>🕹️ Play hard. Score high. Earn coins. Get your snacks.</strong>
</p>

<p align="center">
  <i>In 8-BIT, you don't just buy your snacks — you earn them.</i> 🚀
</p>