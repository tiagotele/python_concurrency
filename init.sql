CREATE TABLE prices(
    id serial primary key,
    symbol text,
    price float,
    extracted_time timestamp
)
;