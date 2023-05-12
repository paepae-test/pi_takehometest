# Pi - Take Home Test


## Requirements

Tested with:
- Python 3.9.1
- PostgreSQL 12.5


## Running development server

Run development server:
1. Install Python packages:
```
pip install -r requirements.txt
```
2. Run PostgreSQL server.
3. Create new database in PostgreSQL.
4. Create `.env` file with following content. Replace all values with your configuration:
```
POSTGRES_HOST=<host>
POSTGRES_PORT=<port>
POSTGRES_USERNAME=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database_name>
```
5. Start development server:
```
uvicorn app.main:app --reload
```

Run integration test:
1. Run the server at least once to initialize DB data.
2. Execute pytest command:
```
pytest
```


## Development Note

Language choice: Python
- Good for fast development. Has features fit to the requirements.
- Compare to C#, it would take more time to develop.

Framework choice: FastAPI, SQLAlchemy
- Good choices for API development with good performance and minimal overhead.
- Has async support.
- Has good documentations.
- Compare to Django/Django Rest Framework, its async support still in development.

Database choice: PostgreSQL
- Free and open source.
- High performance and scalability with a lot of advanced features for modern applications.

Possible improvements:
- Use Docker
- Add authorization and authentication.
- Add database migrations.
- Add data cleanup after integration test execution.
- Add caching layer. Maybe using Redis.
- Turn off echo feature in database engine (echo=Off) in `app/db/base.py`.
