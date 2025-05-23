from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.UserModel import User
from src.auth.auth_shema import RegisterUser, UserShema, LoginUser, UpdateUser
from src.db import get_session
from src.auth.auth_utilits import create_access_token, dencode_password, check_password
from src.get_current_user import get_current_user

app = APIRouter(prefix="/users", tags=["Users"])

# получение авторизованного пользователя
@app.get("/me", response_model=UserShema)
async def me(me = Depends(get_current_user)):
     return me

# получение всех пользователей
@app.get("/all_users/", response_model=list[UserShema])
async def get_all_users(session:AsyncSession = Depends(get_session)):
    users = await session.scalars(select((User)).options(selectinload(User.groups)))
    return users.all()

# авторизация
@app.post("/login")
async def login_user(data:LoginUser, session:AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.email == data.email))

    if user:
        if await check_password(password=data.password, old_password=user.password):
            user_token = await create_access_token(user_id=user.id)
            return {"token":user_token}

    raise HTTPException(status_code=401, detail={
                "details":"user is not exists",
                "status":401
        })


# регистрация
@app.post("/register")
async def register_user(data:RegisterUser ,session:AsyncSession = Depends(get_session)):
    
    isUserEx = await session.scalar(select(User).where(User.email == data.email))
    
    if isUserEx:
        raise HTTPException(status_code=411, detail={
        "status":411,
        "data":"user is exists"
        })
        
    data_dict = data.model_dump()
        
    data_dict["password"] = await dencode_password(password=data.password)
    
    user = User(**data_dict)
    session.add(user) 
    await session.flush()

    user_id = user.id
        
    await session.commit()
        
    user_token = await create_access_token(user_id=user_id)
    data_dict["token"] = user_token  
        
    return data_dict

# изменений данных пользователя
@app.put("/update", response_model=UserShema)
async def update_user(data:UpdateUser, me:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    
    await session.refresh(me)
    if data.surname:
        me.surname = data.surname
    if data.name:
        me.name = data.name
    if data.patronymic:
        me.patronymic = data.patronymic
    if data.email:
        me.email = data.email
    if data.snils:
        me.snilas = data.snils

    await session.commit()
    await session.refresh(me)

    return me

# удаление пользователя
@app.delete("/delete/{user_id}")
async def delete_user(user_id: int = Path(..., gt=0), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # Проверка, что текущий пользователь — админ
    if current_user.role.value != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не имеете прав на удаление пользователя."
        )
    user = await session.scalar(select(User).where(User.id == user_id))
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

    return {"message": f"User with ID {user_id} has been deleted"}

