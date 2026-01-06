from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

client = None
db = None

async def connect_to_mongo():
    global client, db
    try:
        print("🔌 Connecting to MongoDB...")
        client = AsyncIOMotorClient(settings.MONGO_URI)
        db = client[settings.DB_NAME]
        await client.admin.command("ping")
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)
        raise e

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("🔒 MongoDB connection closed")

def get_user_collection():
    return db.users
