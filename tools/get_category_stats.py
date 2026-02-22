"""
get_category_stats skill

This module provides a single function `get_category_stats` which queries the products
table and returns a list of dicts with keys: category, product_count, average_price.

The function is self-contained and uses db_helper to access the database.
"""

from typing import List, Dict, Any, Optional


def get_category_stats(limit: Optional[int] = None, round_digits: int = 2, rows: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Return a list of dicts with category, product_count, average_price.

    Parameters:
    - limit: if provided, limit the number of returned rows from the DB query (passed to SQL as LIMIT)
    - round_digits: number of decimal places to round average_price
    - rows: optional pre-fetched rows (list[dict]) to use instead of querying the DB

    Returns:
    - list[dict]: each dict contains 'category', 'product_count' (int), 'average_price' (float or None)
    """
    if rows is None:
        # import locally to keep module import-safe when not executing
        from db_helper import query
        sql = (
            "SELECT category, COUNT(*) AS product_count, AVG(unit_price) AS average_price "
            "FROM products GROUP BY category ORDER BY category"
        )
        if limit is not None:
            sql = sql + f" LIMIT {int(limit)}"
        rows = query(sql)

    # Normalize and round results
    result = []
    for r in rows:
        category = r.get('category') if r.get('category') is not None else r.get('CATEGORY')
        product_count = r.get('product_count') if r.get('product_count') is not None else r.get('PRODUCT_COUNT')
        avg = r.get('average_price') if r.get('average_price') is not None else r.get('AVERAGE_PRICE')

        try:
            product_count = int(product_count) if product_count is not None else 0
        except Exception:
            product_count = 0

        if avg is None:
            average_price = None
        else:
            try:
                average_price = round(float(avg), int(round_digits))
            except Exception:
                # fallback if value not castable
                average_price = None

        result.append({
            'category': category,
            'product_count': product_count,
            'average_price': average_price,
        })

    return result