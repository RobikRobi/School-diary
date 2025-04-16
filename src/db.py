from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from src.config import config



engine = create_async_engine(url = config.env_data.DB_URl_ASYNC, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with  async_session() as session:
        yield session
        await session.commit()

class Base(AsyncAttrs, DeclarativeBase):
    pass








# 

#

# model VerficationCode {
#     id Int @id @default(autoincrement())

#     user User @relation(fields: [userId], references: [id])
#     userId Int @unique

#     code String
#     createdAt DateTime @default(now())

#     @@unique([userId, code])

# }

