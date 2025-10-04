
import sqlite3
import os
from typing import List, Dict, Any
from datetime import datetime
import uuid


DB_PATH = "learning_tracker.db"

def init_database():
    """
    Inisialisasi database dengan tabel-tabel untuk melacak pembelajaran.
    Fungsi ini akan membuat dan mengisi data sampel jika database belum ada.
    """
  
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        start_time TEXT NOT NULL,
        main_topic TEXT
    )
    """)
    
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        timestamp TEXT NOT NULL,
        user_query TEXT NOT NULL,
        search_results TEXT,
        llm_response TEXT NOT NULL,
        user_feedback INTEGER,  -- 1 for positive, -1 for negative, 0 for neutral
        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
    )
    """)
    
   
    if cursor.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] == 0:
       
        sample_session_id = str(uuid.uuid4())
        
       
        cursor.execute(
            "INSERT INTO sessions (session_id, start_time, main_topic) VALUES (?, ?, ?)",
            (sample_session_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Musim di Indonesia")
        )
        
      
        cursor.executemany(
            "INSERT INTO interactions (session_id, timestamp, user_query, search_results, llm_response, user_feedback) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (
                    sample_session_id, 
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    "musim apa sekarang di indonesia?", 
                    "{'source': 'BMKG', 'summary': 'Masa transisi dari kemarau ke hujan.'}",
                    "Saat ini Indonesia sedang dalam masa transisi dari musim kemarau ke musim hujan.",
                    1
                ),
                (
                    sample_session_id, 
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    "kapan puncak musim hujan?",
                    "{'source': 'BMKG', 'summary': 'Puncak musim hujan diprediksi Januari-Februari.'}",
                    "Puncak musim hujan di sebagian besar wilayah Indonesia diperkirakan akan terjadi pada bulan Januari dan Februari.",
                    0
                ),
                (
                    sample_session_id, 
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    "apa itu angin muson?",
                    "{'source': 'Wikipedia', 'summary': 'Angin periodik yang berubah arah setiap setengah tahun.'}",
                    "Angin muson adalah angin yang bertiup secara periodik, biasanya berubah arah setiap enam bulan sekali, yang menyebabkan perbedaan musim di Indonesia.",
                    1
                )
            ]
        )
    
    conn.commit()
    conn.close()
    
    return "Database Learning Tracker berhasil diinisialisasi dengan data sampel."

def execute_sql_query(query: str) -> List[Dict[str, Any]]:
    """
    Mengeksekusi query SQL dan mengembalikan hasilnya sebagai list of dictionaries.
    Fungsi ini generik dan bisa digunakan untuk SELECT, INSERT, UPDATE, DELETE.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
           
            result = [{k: row[k] for k in row.keys()} for row in rows]
        else:
            
            conn.commit()
            result = [{"affected_rows": cursor.rowcount}]
            
        conn.close()
        return result
    
    except sqlite3.Error as e:
        return [{"error": str(e)}]

def get_table_schema() -> Dict[str, List[Dict[str, str]]]:
    """
    Mengambil skema dari semua tabel di dalam database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        schema = {}
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            schema[table_name] = [
                {
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "pk": bool(col[5])
                }
                for col in columns
            ]
        
        conn.close()
        return schema
    
    except sqlite3.Error as e:
        return {"error": str(e)}


def query_learning_database(sql_query: str) -> Dict[str, Any]:
    """
    Mengeksekusi query SQL terhadap database learning_tracker.
    
    Args:
        sql_query: Query SQL yang akan dieksekusi.
        
    Returns:
        Dictionary berisi query SQL dan hasilnya.
    """
    
    if not os.path.exists(DB_PATH):
        init_database()
    
    try:
        results = execute_sql_query(sql_query)
        return {
            "query": sql_query,
            "results": results
        }
    except Exception as e:
        return {
            "query": sql_query,
            "results": [{"error": str(e)}]
        }

def get_database_info() -> Dict[str, Any]:
    """
    Mengambil informasi tentang skema database untuk membantu AI dalam membuat query.
    
    Returns:
        Dictionary berisi skema database dan beberapa data sampel.
    """
  
    if not os.path.exists(DB_PATH):
        init_database()
    
    schema = get_table_schema()
    
   
    sample_data = {}
    for table_name in schema.keys():
        if isinstance(table_name, str):
            try:
                sample_data[table_name] = execute_sql_query(f"SELECT * FROM {table_name} LIMIT 3")
            except Exception:
                pass
    
    return {
        "schema": schema,
        "sample_data": sample_data
    }


if __name__ == "__main__":
    print(init_database())
    print("\nSkema Database:")
    import json
    print(json.dumps(get_table_schema(), indent=2))
    print("\nContoh Query 'Topik yang paling sering ditanyakan':")
    print(query_learning_database("SELECT user_query, COUNT(*) as total FROM interactions GROUP BY user_query ORDER BY total DESC LIMIT 3"))