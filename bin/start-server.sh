PGPASSWORD=12345 psql -h db -U sportsbook_user -w -b sportsbook_db < app/db/seed.sql

cd app/
uvicorn main:app --host 0.0.0.0 --reload
