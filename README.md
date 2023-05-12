# Pi - Take Home Test


## Requirements

Tested with:
- Python 3.9
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
JWT_SECRET_KEY=<jwt_secret_key>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=<jwt_expire_minutes>
TEST_APP_USER_USERNAME=<test_jwt_auth_username>
TEST_APP_USER_PASSWORD=<test_jwt_auth_password>
```
5. Start development server:
```
uvicorn app.main:main_app --reload
```
6. See documentations at http://localhost:8000/docs#/

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
- Trade-offs: Weak data typing. Lower performance.

Framework choice: FastAPI, SQLAlchemy
- Good choices for API development with good performance and minimal overhead.
- Has async support.
- Has good documentations.
- Compare to Django/Django REST Framework, its async support still in development.

Database choice: PostgreSQL
- Free and open source.
- High performance and scalability with a lot of advanced features for modern applications.

Possible improvements:
- IMPORTANT: Remove the test app user creation (`create_test_app_user()`, `settings.TEST_APP_USER_USERNAME`, `settings.TEST_APP_USER_PASSWORD`) and replace with proper app user management.
- IMPORTANT: Turn off echo feature in database engine (echo=Off) in `app/db/base.py`.
- Use Docker
- Add authorization and authentication.
- Add database migrations.
- Add data cleanup after integration test execution.
- Add caching layer. Maybe using Redis.
- Add logging.
- Add more tests, eg. duplicate email address.
