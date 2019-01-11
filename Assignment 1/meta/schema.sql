
CREATE TABLE Paper (
    PaperId INTEGER,
    Title VARCHAR,
    year INTEGER,
    VenueId INTEGER
);

CREATE TABLE Author (
    AuthorId INTEGER,
    name VARCHAR
);

CREATE TABLE PaperByAuthors (
    AuthorId INTEGER,
    PaperId INTEGER
);

CREATE TABLE Citation (
    Paper1Id INTEGER,
    Paper2Id INTEGER
);

CREATE TABLE Venue (
    VenueId INTEGER,
    name VARCHAR,
    type VARCHAR
);
