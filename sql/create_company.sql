CREATE TABLE company (
    id SERIAL PRIMARY KEY,  -- 添加一个自动递增的主键
    name VARCHAR(255) NOT NULL,
    english_name VARCHAR(255) NOT NULL,
    short_name VARCHAR(100) NOT NULL,
    market VARCHAR(10) NOT NULL CHECK (market IN ('公開發行', '上市', '上櫃')),
    code VARCHAR(20) NOT NULL
);

CREATE TABLE test_company (
    id SERIAL PRIMARY KEY,  -- 添加一个自动递增的主键
    name VARCHAR(255) NOT NULL,
    english_name VARCHAR(255) NOT NULL,
    short_name VARCHAR(100) NOT NULL,
    market VARCHAR(10) NOT NULL CHECK (market IN ('公開發行', '上市', '上櫃')),
    code VARCHAR(20) NOT NULL
);