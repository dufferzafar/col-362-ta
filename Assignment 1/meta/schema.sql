
CREATE TABLE Paper (
    PaperId INTEGER,
    Title VARCHAR,
    Year INTEGER,
    VenueId INTEGER
);

CREATE TABLE Author (
    AuthorId INTEGER,
    AuthorName VARCHAR
);

CREATE TABLE PaperByAuthors (
    AuthorId INTEGER,
    PaperId INTEGER
);

CREATE TABLE Citation (
    Paper1Id INTEGER,
    Paper2id INTEGER
);

CREATE TABLE Venue (
    VenueId INTEGER,
    VenueName VARCHAR,
    VenueType VARCHAR
);
