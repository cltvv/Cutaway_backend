from uuid import uuid4
from typing import List
from datetime import datetime

from src.auth.unit_of_work import AbstractUnitOfWork as UserUow
from src.search_query.unit_of_work import AbstractUnitOfWork as SearchQueryUow

from src.auth.models import User
from src.search_query.models import SearchQuery


def create(user_uow: UserUow,
           search_query_uow: SearchQueryUow,
           user_id: str,
           text_query: str) -> None:
    
    with user_uow:
        user = user_uow.users.getByID(user_id)
        user_uow.commit()
    
    with search_query_uow:
        search_query_uow.search_queries.add(SearchQuery(uuid4(), user, text_query, created_at=datetime.utcnow()))
        search_query_uow.commit()


def get(search_query_uow: SearchQueryUow, user_id: str) -> List[SearchQuery]:
    with search_query_uow:
        search_queries = search_query_uow.search_queries.getByUserID(user_id)
        search_queries = sorted(search_queries, key=lambda x: x.created_at, reverse=True)
        search_query_uow.commit()
    return search_queries


def delete(search_query_uow: SearchQueryUow, sq_id: str, user_id) -> None:
    with search_query_uow:
        search_queries = search_query_uow.search_queries.getByUserID(user_id)
        found_query = False
        for search_query in search_queries:
            if search_query.id == sq_id:
                found_query = True
                break

        if not found_query:
            raise ValueError("User doesn't have a search query with this id")

        search_query_uow.search_queries.deleteByID(sq_id)
        search_query_uow.commit()
