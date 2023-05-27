from fastapi import FastAPI


from src.auth.router import auth_router, user_router
from src.profile.router import profile_router, user_profile_router
from src.bookmark.router import router as bookmark_router
from src.profile_history.router import router as profile_history_router
from src.search_query.router import router as search_query_router
from src.image.router import router as image_router
from database import start_mappers


app = FastAPI(
    title='Cutaway API'
)


start_mappers()


app.include_router(image_router, prefix='/images', tags=['Images'])
app.include_router(auth_router, tags=['Auth'])
app.include_router(user_router, prefix='/users', tags=['Users'])
app.include_router(bookmark_router, prefix='/me/bookmarks', tags=['Bookmarks'])
app.include_router(user_profile_router, prefix='/me/profiles', tags=['User Profiles'])
app.include_router(profile_router, prefix='/profiles', tags=['Profiles'])
app.include_router(profile_history_router, prefix='/me/profile-history', tags=['Profile History'])
app.include_router(search_query_router, prefix='/me/search-history', tags=['Search Query History'])
