import requests
import ujson
import random
import time

import logging
import os
import sqlite3

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.debug(
    "Opening database @ %s", os.environ.get("DB_PATH", "/var/lib/crawler/crawler.db")
)
conn = sqlite3.connect(os.environ.get("DB_PATH", "/var/lib/crawler/crawler.db"))

logging.debug("Creating table")
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS house (
        id              TEXT,
        street          TEXT,
        district        TEXT,
        postcode        TEXT,
        state           TEXT,
        size            TEXT,
        unit            REAL,
        unit_price      REAL,
        asking_price    REAL,
        raw             TEXT,
        PRIMARY KEY (id)
    )
    """
)

for i in range(200):
    resp = requests.get(
        "https://www.edgeprop.my/jwdsonic/api/v1/property/search",
        params={
            "state": os.environ.get("QUERY_STATE", "Kuala Lumpur"),
            "listing_type": os.environ.get("QUERY_LISTING_TYPE", "rent"),
            "start": i,
            "size": 20,
            "property_type": "rl",
            "featured": 1,
        },
    )

    logging.debug("Writing rows in page %s", i)
    result = resp.json()
    for row in result.get("property", []):
        conn.execute(
            """
            REPLACE INTO house (id, street, district, postcode, state, size, unit, unit_price, asking_price, raw)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                row["id"],
                row.get("field_prop_street_t", None),
                row.get("district_s_lower", None),
                row.get("field_prop_postcode_i", None),
                row.get("state_s_lower", None),
                row.get("field_prop_built_up_d", None),
                row.get("field_prop_built_up_unit_s_lower", None),
                row.get("field_prop_built_up_price_pu_d", None),
                row.get("field_prop_asking_price_d", None),
                ujson.dumps(row),
            ),
        )

    time.sleep(
        random.randint(
            int(os.environ.get("REST_SEC_MIN", 7)),
            int(os.environ.get("REST_SEC_MAX", 9)),
        )
    )

conn.close()
