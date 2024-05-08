db = db.getSiblingDB("test_db");
db.test_db.drop();

db.test_db.insertMany([
    {
        "id": 1,
        "username": "John_Smith",
        "password": "Password1",
        "email": "js@example.com"
    },
    {
        "id": 2,
        "username": "Anrew_Do",
        "password": "Password2",
        "email": "ad@example.com"
    },
    {
        "id": 3,
        "username": "Anna Woo",
        "password": "Password3",
        "email": "aw@example.com"
    },
]);