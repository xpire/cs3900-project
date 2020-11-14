"""
Check __init__.py files under each directory to see the description of each directory

Brief overview of the top-level directories (logically organised):
- [core]: fundamental modules that rest of the application may depend on
- [schemas]: defines various JSON-parsable types for both the endpoints and internal usage

- [db]: manages database setup, start up, and connection
- [models]: defines SQLAlchemy ORMs that map to database tables
- [crud]: implements CRUD operations on the database and the database [models]

- [domain_models]: object-oriented encapsulation of core business logic, split into 5 parts: 
                    order, trade, user, statistics, and trading hours management
- [api]: implements the API endpoints provided

- [game]: implements the "game-like" features
- [notification]: implements the user notification system that occurs through websockets

- [test]: aggregation of all tests
"""
