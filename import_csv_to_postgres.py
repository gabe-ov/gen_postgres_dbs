import os
import pandas as pd
import psycopg2

# Configurações dos bancos (pode ajustar host/port se quiser conectar local)
DATABASES = {
    "titanic_db": {
        "host": "localhost",
        "port": 5433,
        "user": "user",
        "password": "password",
        "database": "titanic_db",
        "csv_folder": "./databases/titanic_db",
    },
    "resolve_db": {
        "host": "localhost",
        "port": 5434,
        "user": "user",
        "password": "password",
        "database": "resolve_db",
        "csv_folder": "./databases/resolve_db",
    },
    "spaceship_titanic_db": {
        "host": "localhost",
        "port": 5435,
        "user": "user",
        "password": "password",
        "database": "spaceship_titanic_db",
        "csv_folder": "./databases/spaceship_titanic_db",
    }
}

def connect_db(cfg):
    return psycopg2.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"]
    )

def clean_table_name(name):
    return "".join(c for c in name if c.isalnum() or c == "_")

def import_csv_to_table(conn, csv_path):
    df = pd.read_csv(csv_path)

    table_name = clean_table_name(os.path.splitext(os.path.basename(csv_path))[0])

    with conn.cursor() as cur:
        cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        conn.commit()

        columns = df.columns
        create_cols = ", ".join([f"{clean_table_name(col)} TEXT" for col in columns])
        create_sql = f"CREATE TABLE {table_name} ({create_cols});"
        cur.execute(create_sql)
        conn.commit()

        for i, row in df.iterrows():
            values = tuple(str(x) if pd.notnull(x) else None for x in row)
            placeholders = ", ".join(["%s"] * len(values))
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cur.execute(insert_sql, values)
        conn.commit()

    print(f"Imported '{csv_path}' into table '{table_name}'.")

def main():
    for db_name, cfg in DATABASES.items():
        print(f"\nProcessing database: {db_name}")
        conn = connect_db(cfg)

        csv_folder = cfg["csv_folder"]
        for filename in os.listdir(csv_folder):
            if filename.endswith(".csv"):
                csv_path = os.path.join(csv_folder, filename)
                import_csv_to_table(conn, csv_path)

        conn.close()

if __name__ == "__main__":
    main()
