from datetime import date

from sqlalchemy.orm import Query


def filter_by_date_range(query: Query, column, date_from: date | None, date_to: date | None) -> Query:
    if date_from is not None:
        query = query.filter(column >= date_from)
    if date_to is not None:
        query = query.filter(column <= date_to)
    return query