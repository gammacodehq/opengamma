import sqlite3

conn = sqlite3.connect("sqlite.db")
cursor = conn.cursor()

query = """
WITH convs AS (SELECT id FROM conversations ORDER BY id),
first_msgs AS (
    SELECT conversation_id, role, content,
           ROW_NUMBER() OVER (PARTITION BY conversation_id, role ORDER BY created_at) as rn
    FROM messages
    WHERE conversation_id IN (SELECT id FROM convs) AND role IN ('user', 'assistant')
)
SELECT MAX(CASE WHEN role='user' THEN content END) as user_content,
       MAX(CASE WHEN role='assistant' THEN content END) as assistant_content
FROM first_msgs
WHERE rn = 1
GROUP BY conversation_id
ORDER BY conversation_id
"""

cursor.execute(query)
results = cursor.fetchall()

count = 0
for row in results:
    user_content, assistant_content = row
    if 'резентаци' in user_content or 'резентаци' in assistant_content:
        count+=1
        with open('test/task'+str(count).rjust(4, '0')+'.txt', 'w') as f:
                f.write(assistant_content)
print(f"Found {count}")
conn.close()
