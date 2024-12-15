CREATE TABLE organisation (
    organisation_id INT GENERATED ALWAYS AS IDENTITY,
    organisation_name TEXT UNIQUE NOT NULL,
    PRIMARY KEY (organisation_id)
);

CREATE TABLE tag (
    tag_id INT GENERATED ALWAYS AS IDENTITY,
    tag_text TEXT UNIQUE NOT NULL,
    PRIMARY KEY (tag_id)
);

CREATE TABLE category (
    category_id INT GENERATED ALWAYS AS IDENTITY,
    category_name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (category_id)
);

CREATE TABLE article (
    article_id INT GENERATED ALWAYS AS IDENTITY,
    article_title TEXT NOT NULL,
    article_url TEXT NOT NULL,
    published TIMESTAMP NOT NULL,
    article_text TEXT,
    organisation_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (article_id),
    FOREIGN KEY (organisation_id) REFERENCES organisation(organisation_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE article_tag_connection (
    article_tag_connection_id INT GENERATED ALWAYS AS IDENTITY,
    article_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (article_tag_connection_id),
    FOREIGN KEY (article_id) REFERENCES article(article_id),
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id)
);

INSERT INTO organisation
    (organisation_name)
VALUES
    ('The Onion')
;

INSERT INTO category
    (category_name)
VALUES
    ('News')
;