CREATE TABLE customer (
        id INTEGER NOT NULL,
        code TEXT UNIQUE,
        name TEXT,
        address TEXT,
        part_iva TEXT,
        cap TEXT,
        city TEXT,
        prov TEXT,
	tel TEXT,
	ins_date TEXT,
	mod_date TEXT,
        user_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE discount_product (
        id INTEGER NOT NULL,
        customer_id INTEGER,
        product_id INTEGER,
        discount_value FLOAT,
        discount_type VARCHAR(1) NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(customer_id) REFERENCES customer (id),
        FOREIGN KEY(product_id) REFERENCES product (id)
);
CREATE TABLE favorite (
        id INTEGER NOT NULL,
        customer_id INTEGER,
        product_id INTEGER,
        hits INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(customer_id) REFERENCES customer (id),
        FOREIGN KEY(product_id) REFERENCES product (id)
);
CREATE TABLE icewer_purchase (
        id INTEGER NOT NULL,
        user_id INTEGER,
        customer_id INTEGER,
        creation_date DATETIME,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user (id),
        FOREIGN KEY(customer_id) REFERENCES customer (id)
);
CREATE TABLE icewer_purchase_item (
        id INTEGER NOT NULL,
        purchase_id INTEGER,
        product_code TEXT,
        qty INTEGER,
        notes TEXT,
        discount TEXT,
        PRIMARY KEY (id),
        FOREIGN KEY(purchase_id) REFERENCES icewer_purchase (id)
);
CREATE TABLE product (
        id INTEGER NOT NULL,
        code VARCHAR(10) UNIQUE,
        name VARCHAR(80),
        price FLOAT,
        PRIMARY KEY (id)
);
CREATE TABLE purchase (
        id INTEGER NOT NULL,
        user_id INTEGER,
        customer_id INTEGER,
        creation_date DATETIME,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user (id),
        FOREIGN KEY(customer_id) REFERENCES customer (id)
);
CREATE TABLE purchase_item (
        id INTEGER NOT NULL,
        product_id INTEGER,
        purchase_id INTEGER,
        qty INTEGER,
        notes TEXT,
        discount TEXT,
        PRIMARY KEY (id),
        FOREIGN KEY(product_id) REFERENCES product (id),
        FOREIGN KEY(purchase_id) REFERENCES purchase (id)
);
CREATE TABLE user (
        id INTEGER NOT NULL,
        username VARCHAR(80),
        password VARCHAR(32),
        code VARCHAR(36),
        is_admin BOOLEAN,
        PRIMARY KEY (id),
        UNIQUE (username),
        CHECK (is_admin IN (0, 1))
);

