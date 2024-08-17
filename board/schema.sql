
CREATE TABLE flashcard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term VARCHAR NOT NULL,
    definition VARCHAR NOT NULL,
    course VARCHAR(20)
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(1000),
    surname VARCHAR(1000),
    school VARCHAR(1000),
    role VARCHAR(20) NOT NULL DEFAULT 'student'
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course = VARCHAR(100) NOT NULL,
    course_number = VARCHAR(100) NOT NULL, 
    subject = VARCHAR(100) NOT NULL,
    teacher = VARCHAR(100) NOT NULL
);