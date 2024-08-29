CREATE TABLE company (
    id SERIAL PRIMARY KEY,  -- 添加一個自動遞增的主鍵
    name VARCHAR(255) NOT NULL,
    english_name VARCHAR(255) NOT NULL,
    short_name VARCHAR(100) NOT NULL,
    market VARCHAR(10) NOT NULL CHECK (market IN ('公開發行', '上市', '上櫃')),
    code VARCHAR(20) NOT NULL
);

CREATE TABLE test_company (
    id SERIAL PRIMARY KEY,  -- 添加一個自動遞增的主鍵
    name VARCHAR(255) NOT NULL,
    english_name VARCHAR(255) NOT NULL,
    short_name VARCHAR(100) NOT NULL,
    market VARCHAR(10) NOT NULL CHECK (market IN ('公開發行', '上市', '上櫃')),
    code VARCHAR(20) NOT NULL
);

CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    news_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL
);