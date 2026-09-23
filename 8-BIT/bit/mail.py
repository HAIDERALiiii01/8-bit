import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

FROM_EMAIL = os.getenv("from_email")
PASSWORD = os.getenv("gmail_password")


def build_receipt(user, order) -> str:
    """Plain-text receipt built from an Orders row and its OrderItems."""
    lines = [
        f"Hey {user.username},",
        "",
        "Thanks for shopping at 8-Bit Studios! Here's your receipt:",
        "",
    ]

    for item in order.items:
        name = item.product.product_name if item.product else "Item"
        lines.append(f"  {name} x{item.quantity} \u2014 {item.subtotal}c ({item.unit_price}c each)")

    lines += [
        "",
        f"Total: {order.total_amount}c",
        f"Order #{order.order_id}",
        "",
        "See you next time!",
    ]
    return "\n".join(lines)


def send_receipt_email(user, order) -> None:
    """
    Emails the user a receipt for the order they just placed.
    Raises on failure -- the caller decides whether that should block
    the purchase response or just get logged.
    """
    if not FROM_EMAIL or not PASSWORD:
        raise RuntimeError("Missing from_email or password env vars.")

    message = build_receipt(user, order)

    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = f"8-Bit Studios \u2014 Receipt for Order #{order.order_id}"
    msg["From"] = FROM_EMAIL
    msg["To"] = user.email

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=FROM_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=FROM_EMAIL, to_addrs=user.email, msg=msg.as_string())