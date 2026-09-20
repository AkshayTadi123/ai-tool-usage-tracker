"""Populate usage_records with synthetic data. Safe to re-run: it clears the table first."""

import os
import random
from datetime import date, timedelta
from decimal import Decimal

import pymysql
from dotenv import load_dotenv
from faker import Faker

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

TEAMS = ["Platform", "Analytics", "Infrastructure", "Product", "Research"]

# Price per token, so cost stays proportional to tokens.
TOOLS = {
    "Claude Code": Decimal("0.000009"),
    "GitHub Copilot": Decimal("0.000004"),
    "Cursor": Decimal("0.000006"),
    "ChatGPT": Decimal("0.000005"),
}

USERS = 25
DAYS = 60

fake = Faker()
Faker.seed(42)
random.seed(42)


def build_users():
    """Each user gets a weight from a Pareto distribution: most near 1, a few much larger."""
    return [
        {
            "name": fake.name(),
            "team": random.choice(TEAMS),
            "weight": random.paretovariate(1.5),
        }
        for _ in range(USERS)
    ]


def build_rows(users):
    today = date.today()
    rows = []
    for user in users:
        active_odds = min(0.9, 0.15 * user["weight"])
        for offset in range(DAYS):
            if random.random() >= active_odds:
                continue
            for _ in range(random.randint(1, 3)):
                tool = random.choice(list(TOOLS))
                tokens = int(random.lognormvariate(8.5, 0.8) * user["weight"])
                rows.append(
                    (
                        user["name"],
                        user["team"],
                        tool,
                        tokens,
                        (TOOLS[tool] * tokens).quantize(Decimal("0.01")),
                        today - timedelta(days=offset),
                    )
                )
    return rows


def main():
    rows = build_rows(build_users())
    conn = pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE usage_records")
            cur.executemany(
                "INSERT INTO usage_records "
                "(user_name, team, tool, tokens, cost, used_on) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                rows,
            )
        conn.commit()
    print(f"Inserted {len(rows)} rows.")


if __name__ == "__main__":
    main()
