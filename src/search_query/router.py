from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated


from src.auth.models import User
from src.auth.router import get_current_user
from src.search_query.unit_of_work import SqlAlchemyUnitOfWork as SqlSearchQueryUow
from src.search_query.schemas import SearchQueryRead
from src.search_query.service import get, delete


router = APIRouter()


@router.get('', response_model=List[SearchQueryRead])
def get_user_search_queries(current_user: Annotated[User, Depends(get_current_user)]):
    search_queries = get(SqlSearchQueryUow(), current_user.id)
    if not search_queries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg': "User doesn't have any search history"}
        )
    result = []
    for search_query in search_queries:
        result.append(SearchQueryRead.from_orm(search_query))
    return result


@router.delete('/{search_query_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user_search_query(current_user: Annotated[User, Depends(get_current_user)], search_query_id: str):
    try:
        delete(SqlSearchQueryUow(), search_query_id, current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'msg': str(e)
            }
        )
