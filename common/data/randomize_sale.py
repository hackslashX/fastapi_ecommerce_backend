import sys, os

sys.path.append(os.getcwd())

import crud
from db.dependency import get_db

import random
import asyncio
from datetime import datetime, timedelta

TOTAL_SALES_TO_MODIFY = 2000


async def randomize_sale():
    _db = get_db()
    db = await anext(_db)
    for i in range(0, TOTAL_SALES_TO_MODIFY):
        # Pick a random date between jan 2022 and sep 2023
        date = datetime(2022, 1, 1) + timedelta(days=random.randrange(0, 999))
        # Get a sale
        sale = await crud.sale.get(db, id=i)
        if not sale:
            continue
        await crud.sale.update(db, db_obj=sale, obj_in={"created_at": date})


if __name__ == "__main__":
    asyncio.run(randomize_sale())
