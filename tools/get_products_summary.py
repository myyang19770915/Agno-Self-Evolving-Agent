"""get_products_summary skill

This module provides get_products_summary(limit=None, round_digits=2, return_df=False, rows=None)
It uses db_helper.query / db_helper.query_df for database access when rows is not provided.
Returns list[dict] with keys: category, product_count, average_price (rounded) or a pandas.DataFrame if return_df=True.
"""
from typing import List, Dict, Optional, Any


def get_products_summary(limit: Optional[int] = None,
                         round_digits: int = 2,
                         return_df: bool = False,
                         rows: Optional[List[Dict[str, Any]]] = None):
    """Return per-category product counts and average prices.

    Parameters:
    - limit: if provided, limit the number of rows fetched from the DB
    - round_digits: number of decimals to round average_price
    - return_df: if True return a pandas.DataFrame, else return list[dict]
    - rows: optional pre-fetched rows (list[dict]) to use instead of querying the DB
    """
    import pandas as pd

    # If rows not provided, query the DB using db_helper
    if rows is None:
        # Use db_helper as requested
        from db_helper import query, query_df

        if return_df:
            sql = "SELECT category, unit_price FROM products"
            if limit is not None:
                sql = f"{sql} LIMIT {int(limit)}"
            df = query_df(sql)
        else:
            sql = "SELECT category, unit_price FROM products"
            if limit is not None:
                sql = f"{sql} LIMIT {int(limit)}"
            rows = query(sql)
            df = pd.DataFrame(rows)
    else:
        df = pd.DataFrame(rows)

    # If no data, return empty structure
    if df.empty:
        return pd.DataFrame(columns=['category', 'product_count', 'average_price']) if return_df else []

    # Ensure the expected columns exist
    if 'unit_price' not in df.columns:
        # try common alternative column names
        for alt in ['price', 'unitPrice']:
            if alt in df.columns:
                df = df.rename(columns={alt: 'unit_price'})
                break

    # Keep only relevant columns
    if 'category' not in df.columns:
        raise ValueError('Input data must contain a "category" column')

    df = df[['category', 'unit_price']].copy()

    # Convert unit_price to numeric, coerce errors to NaN
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

    # Group by category
    grouped = df.groupby('category', dropna=False)['unit_price'].agg(['count', 'mean']).reset_index()
    grouped = grouped.rename(columns={'count': 'product_count', 'mean': 'average_price'})

    # Round average_price
    grouped['average_price'] = grouped['average_price'].round(round_digits)

    # Ensure product_count is int
    grouped['product_count'] = grouped['product_count'].astype(int)

    result_df = grouped[['category', 'product_count', 'average_price']]

    if return_df:
        return result_df
    else:
        return result_df.to_dict(orient='records')