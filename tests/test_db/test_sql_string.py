def test_sql_string():
    from src.news_crawler.connect_db.connect_db import create_insert_sql

    sql = create_insert_sql(
        "company", ["name", "english_name", "short_name", "market", "code"]
    )
    assert (
        sql
        == "INSERT INTO company (name, english_name, short_name, market, code) VALUES (%s, %s, %s, %s, %s);"
    )
