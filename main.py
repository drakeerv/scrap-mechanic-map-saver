import sqlite3

db = sqlite3.connect("map.db")
cursor = db.cursor()
cursor.execute("SELECT * FROM RigidBodyBounds")

# bounds = cursor.fetchall()
# print(bounds)

positions = {}

for row in cursor:
    # append the last 4 elements of the row to the positions dictionary and assign the list to the first element
    if row[1:] in positions:
        positions[row[1:]].append(row[0])
    else:
        positions[row[1:]] = [row[0]]

# find entries with more than one value
to_remove = []
for key, value in positions.items():
    if len(value) > 1:
        print(key, len(value))
        print(value)
        print("Glitched part found. Do you want to remove this entry? (y/n)", end=" ")
        if input().lower() == "y":
            to_remove.append(key)

for to_remove_key in to_remove:
    for body_id in positions[to_remove_key]:
        cursor.execute("DELETE FROM RigidBodyBounds_rowid WHERE rowid = ?", (body_id,))
        cursor.execute("DELETE FROM RigidBodyBounds WHERE id = ?", (body_id,))
        cursor.execute("DELETE FROM RigidBody WHERE id = ?", (body_id,))
        cursor.execute("DELETE FROM ChildShape WHERE bodyId = ?", (body_id,))
        cursor.execute("DELETE FROM Controller WHERE id = ?", ("3" + str(body_id),))
        
db.commit()