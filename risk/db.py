import pandas as pd
from sqlalchemy import create_engine, text
from risk.logger import logger
DB_URI = "postgresql+psycopg2://postgres:Kiru2004@192.168.29.221:5432/beneficiary5"

def get_engine():
    return create_engine(DB_URI)

def load_data_from_db(table_name: str) -> pd.DataFrame:
    logger.info(f"Loading data from {table_name}")
    engine = get_engine()
    return pd.read_sql_table(table_name, con=engine)

def update_predictions_in_db(df: pd.DataFrame, table_name: str):
    engine = get_engine()
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(
                text(f"""
                    UPDATE {table_name}
                    SET RISK_30D = :r30,
                        RISK_60D = :r60,
                        RISK_90D = :r90,
                        RISK_LABEL = :rlabel,
                        TOP_3_FEATURES = :features
                    WHERE DESYNPUF_ID = :pid
                """),
                {
                    "r30": int(row["RISK_30D"]),
                    "r60": int(row["RISK_60D"]),
                    "r90": int(row["RISK_90D"]),
                    "rlabel": row["RISK_LABEL"],
                    "features": row["TOP_3_FEATURES"],
                    "pid": row["DESYNPUF_ID"]
                }
            )
    logger.success("Predictions updated successfully in DB")
