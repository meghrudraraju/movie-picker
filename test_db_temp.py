from sqlalchemy import create_engine,text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres.dvzoswqduhpeynfqwjzl:SWmegh%40132993@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
try:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.execute(text("SELECT 1"))
    print("✅ Connection successful")
except Exception as e:
    print("❌ Connection failed:")
    print(e)


