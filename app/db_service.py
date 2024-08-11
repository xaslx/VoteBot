from database import connection, cursor


async def start_db():
    cursor.execute("""CREATE TABLE IF NOT EXISTS poll (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    title TEXT NOT NULL,
    one_answer TEXT NOT NULL,
    two_answer TEXT NOT NULL,
    accepted BOOLEAN DEFAULT 0,
    canceled BOOLEAN DEFAULT 0
);""")
    connection.commit()


async def insert_poll(username: str, user_id: int, title: str, one_answer: str, two_answer: str, accepted: int, canceled: int) -> int:
    cursor.execute('''
        INSERT INTO poll (username, user_id, title, one_answer, two_answer, accepted, canceled)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (username, user_id, title, one_answer, two_answer, accepted, canceled))
    new_id: int = cursor.lastrowid
    connection.commit()
    return new_id 
    

async def find_poll(poll_id: int) -> dict:
    cursor.execute('''
        SELECT * FROM poll WHERE id = ?
    ''', (poll_id,))
    
    poll = cursor.fetchone()
    
    if poll is None:
        return None

    poll_data = {
        "id": poll[0],
        "user_id": poll[1],
        "username": poll[2],
        "title": poll[3],
        "one_answer": poll[4],
        "two_answer": poll[5],
        "accepted": poll[6],
        "canceled": poll[7]
    }
    
    return poll_data

async def accept_poll(poll_id: int) -> None:
    cursor.execute('''
        UPDATE poll
        SET accepted = 1
        WHERE id = ?
    ''', (poll_id,))
    
    connection.commit()

async def cancel_poll(poll_id: int) -> None:
    cursor.execute('''
        UPDATE poll
        SET canceled = 1
        WHERE id = ?
    ''', (poll_id,))
    
    connection.commit()