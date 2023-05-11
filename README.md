# Pi - Take Home Test

Install Python packages:
```
pip install -r requirements.txt
```

Start development server:
```
uvicorn app.main:app --reload
```

Run integration test:
1. Run the server at least once to initialize DB data.
2. Execute command:
```
pytest
```
