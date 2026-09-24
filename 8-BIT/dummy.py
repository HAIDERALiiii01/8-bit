"""
dummy.py — One-time script to populate the 8-bit Studios database with
realistic dummy data (users, coin transactions, game sessions, orders)
so the admin panel has something to show.

Run once from the project root (same folder as main.py):
    python dummy.py

Then delete this file, as planned.

Deliberately does NOT invent games or products: importing `app` from
main.py already runs seed_games() and seed_products() at module level,
so this script only ever reads the real Snake / Turtle Race games (both
coin_reward=50) and the real 8 vending-machine products (Chai, Coffee,
Pakola, Coke, Lays, Snickers, Extra Bit, Egg Sandwich) and builds
sessions/transactions/orders around them.
"""

import random
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash

from main import app
from extensions import db
from models import User, Game, GameSessions, CoinTransactions, Orders, OrderItems, Products

random.seed(42)  # reproducible dummy data — remove this line for fresh randomness each run

NUM_USERS = 50
DAYS_BACK = 90  # spread activity over the past ~3 months
NOW = datetime.now(timezone.utc)

FIRST_NAMES = [
    "Ahmed", "Ali", "Hassan", "Hussain", "Bilal", "Usman", "Fahad", "Zain",
    "Saad", "Omar", "Danish", "Kamran", "Arslan", "Hamza", "Faizan",
    "Hamid", "Junaid", "Salman", "Waqas", "Tayyab", "Shahzaib", "Rayyan",
    "Talha", "Haris", "Moiz", "Sheraz", "Asad", "Zohaib", "Noman", "Adeel",
    "Ayesha", "Sara", "Fatima", "Zainab", "Mahnoor", "Amna", "Hira",
    "Areeba", "Laiba", "Iqra", "Noor", "Maryam", "Sana", "Rabia", "Komal",
    "Sadia", "Anum", "Kinza", "Mehak", "Wajiha", "Nimra", "Aiman", "Asma",
]
LAST_NAMES = [
    "Khan", "Malik", "Siddiqui", "Sheikh", "Ansari", "Qureshi", "Baig",
    "Raza", "Hashmi", "Farooq", "Iqbal", "Rehman", "Abbasi", "Chaudhry",
    "Javed", "Akhtar", "Shah", "Butt", "Mirza", "Rizvi",
    "Awan", "Bhatti", "Gill", "Warraich", "Cheema", "Dar", "Soomro",
    "Bhutto", "Memon", "Baloch", "Niazi", "Durrani", "Yousafzai", "Satti",
]

# Matches register()'s password policy (>=8 chars, letters + digits + a special char),
# in case you ever want to log in as one of these accounts to poke around.
DUMMY_PASSWORD = "Password123!"


def game_profile_key(game_name: str) -> str:
    """Rough classifier so we can generate plausible scores/coin logic per game."""
    return "snake" if "snake" in game_name.lower() else "race"


def random_datetime_within(days_back: int) -> datetime:
    delta_seconds = random.randint(0, days_back * 24 * 3600)
    return NOW - timedelta(seconds=delta_seconds)


def make_users(n: int) -> list:
    used_names = set()
    users = []
    admin_indices = set(random.sample(range(n), k=2))  # 2 random admins

    while len(users) < n:
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        key = (first, last)
        if key in used_names:
            continue
        used_names.add(key)

        idx = len(users)
        suffix = random.randint(1, 999)
        username = f"{first.lower()}{last.lower()}{suffix}"[:20]  # register() caps at 20 chars
        email = f"{username}@gmail.com"  # register() only accepts @gmail.com addresses

        users.append(
            User(
                username=username,
                email=email,
                password=generate_password_hash(DUMMY_PASSWORD),
                age=random.randint(13, 30),
                gender=random.choice(["male", "female"]),
                is_admin=idx in admin_indices,
            )
        )

    return users


def make_sessions_and_earn_transactions(users, games):
    """Create GameSessions plus a matching 'earn' CoinTransactions row for each.
    Returns {user: running_coin_balance} so make_orders() can spend sensibly.
    """
    balances = {}

    for user in users:
        balances[user] = 0
        num_sessions = random.randint(5, 40)

        for _ in range(num_sessions):
            game = random.choice(games)
            profile = game_profile_key(game.game_name)
            played_at = random_datetime_within(DAYS_BACK)

            if profile == "snake":
                score = random.randint(0, 2500)
                units = score // 500  # every 500 points earns one unit of coin_reward
                coins_earned = units * game.coin_reward
            else:
                won = random.random() < 0.55  # race: coins only on a win
                score = 1 if won else 0
                coins_earned = game.coin_reward if won else 0

            db.session.add(
                GameSessions(
                    user=user,
                    game=game,
                    score=score,
                    coins_earned=coins_earned,
                    played_at=played_at,
                )
            )

            if coins_earned > 0:
                db.session.add(
                    CoinTransactions(
                        user=user,
                        amount=coins_earned,
                        transaction_type="earn",
                        created_at=played_at,
                    )
                )
                balances[user] += coins_earned

    return balances


def make_orders(users, products, balances):
    buyers = random.sample(users, k=int(len(users) * 0.6))  # ~60% of users buy something

    for user in buyers:
        for _ in range(random.randint(1, 3)):
            if balances[user] < 30:  # cheapest real product (Chai) is 30 coins
                break

            order_items_data = []
            for _ in range(random.randint(1, 3)):
                product = random.choice(products)
                quantity = random.randint(1, 2)
                unit_price = product.price
                order_items_data.append((product, quantity, unit_price, unit_price * quantity))

            total_amount = sum(item[3] for item in order_items_data)
            if total_amount > balances[user]:
                order_items_data = order_items_data[:1]
                total_amount = order_items_data[0][3]
                if total_amount > balances[user]:
                    continue

            purchased_at = random_datetime_within(DAYS_BACK)
            payment_status = random.choices(
                ["completed", "pending", "failed"], weights=[80, 12, 8]
            )[0]

            order = Orders(
                user=user,
                total_amount=total_amount,
                payment_status=payment_status,
                purchased_at=purchased_at,
            )
            db.session.add(order)

            for product, quantity, unit_price, subtotal in order_items_data:
                db.session.add(
                    OrderItems(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal,
                    )
                )

            if payment_status == "completed":
                balances[user] -= total_amount
                db.session.add(
                    CoinTransactions(
                        user=user,
                        amount=-total_amount,
                        transaction_type="spend",
                        created_at=purchased_at,
                    )
                )


def main():
    with app.app_context():
        games = Game.query.all()
        products = Products.query.all()

        if not games or not products:
            raise RuntimeError(
                "Expected seed_games()/seed_products() to have already run via the "
                "`from main import app` import above, but games or products are "
                "missing from the database. Check your DB connection / .env."
            )
        print(f"Using {len(games)} existing game(s): {[g.game_name for g in games]}")
        print(f"Using {len(products)} existing product(s): {[p.product_name for p in products]}")

        users = make_users(NUM_USERS)
        db.session.add_all(users)
        db.session.flush()  # assign IDs so relationships resolve cleanly below

        balances = make_sessions_and_earn_transactions(users, games)
        db.session.flush()

        make_orders(users, products, balances)

        db.session.commit()
        print(
            f"Inserted {len(users)} users, plus game sessions, coin transactions, "
            f"and orders spanning the past {DAYS_BACK} days."
        )


if __name__ == "__main__":
    main()