CREATE TABLE company_info(
    ID  SERIAL PRIMARY KEY,
    company_name TEXT,
    registered_address TEXT,
    company_address TEXT,
    owner_name TEXT,
    occupation TEXT,
    tax_number TEXT UNIQUE,
    city TEXT,
    district TEXT,
    ward TEXT,
    full_name TEXT,
    surname TEXT, 
    middlename TEXT,
    lastname TEXT,
    url TEXT
)