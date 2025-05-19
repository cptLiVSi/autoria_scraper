CREATE TABLE IF NOT EXISTS autoria_cars (
    url TEXT PRIMARY KEY,
    title TEXT,
    price_usd INTEGER,
    odometer INTEGER,
    username TEXT,
    phone_number TEXT,
    image_url TEXT,
    images_count INTEGER,
    car_number TEXT,
    car_vin TEXT,
    datetime_found TIMESTAMPTZ
);