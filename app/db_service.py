from database import connection, cursor


async def start_db():
    cursor.execute("""CREATE TABLE IF NOT EXISTS poll (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    title TEXT NOT NULL,
    accepted BOOLEAN DEFAULT 0,
    canceled BOOLEAN DEFAULT 0
    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS poll_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id INTEGER NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES poll (id) ON DELETE CASCADE
    );""")
    
    connection.commit()


async def insert_poll(username: str, user_id: int, title: str, answers: list[str], accepted: int, canceled: int) -> int:

    cursor.execute('''
        INSERT INTO poll (username, user_id, title, accepted, canceled)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, user_id, title, accepted, canceled))
    
    new_poll_id: int = cursor.lastrowid
    

    cursor.executemany('''
        INSERT INTO poll_answers (poll_id, answer)
        VALUES (?, ?)
    ''', [(new_poll_id, answer) for answer in answers])
    
    connection.commit()
    return new_poll_id


async def find_poll(poll_id: int) -> dict[str, str | list[str]]:

    cursor.execute('''
        SELECT * FROM poll WHERE id = ?
    ''', (poll_id,))
    
    poll = cursor.fetchone()
    
    if poll is None:
        return None


    cursor.execute('''
        SELECT answer FROM poll_answers WHERE poll_id = ?
    ''', (poll_id,))
    
    answers = cursor.fetchall()


    poll_data: dict[str, str | list[str]] = {
        "id": poll[0],
        "user_id": poll[1],
        "username": poll[2],
        "title": poll[3],
        "answers": [answer[0] for answer in answers], 
        "accepted": poll[4],
        "canceled": poll[5]
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