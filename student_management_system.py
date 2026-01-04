import pymysql
import sys

# Connect to MySQL database
def connect_db():
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            passwd="useratheal",
            database="office"
        )
        return db
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

# Main program
def student_marks_management():
    db = connect_db()
    cursor = db.cursor()

    # Check database is connected
    if db.open:
        print("Database connected\n")

    print("WELCOME TO MY PROJECT STUDENT MARKS MANAGEMENT SYSTEM\n")

    while True:
        # Menu options
        print("1: CREATE TABLE FOR THE FIRST TIME")
        print("2: DISPLAY TABLES OF DATABASE")
        print("3: SHOW FIELDS OF A TABLE")
        print("4: DISPLAY ALL DATA")
        print("5: ADD NEW STUDENT")
        print("6: SEARCH A STUDENT RECORD")
        print("7: UPDATE STUDENT MARKS")
        print("8: DELETE STUDENT RECORD")
        print("9: EXIT\n")
        ch = int(input("ENTER YOUR CHOICE: "))

        # Option 1: Create student table
        if ch == 1:
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS student (
                        ROLL INT(4) PRIMARY KEY,
                        name VARCHAR(15) NOT NULL,
                        class CHAR(3) NOT NULL,
                        sec CHAR(1),
                        mark1 INT(4),
                        mark2 INT(4),
                        mark3 INT(4),
                        mark4 INT(4),
                        mark5 INT(4),
                        total INT(4),
                        per FLOAT
                    );
                """)
                db.commit()
                print("STUDENT table created successfully.")
            except pymysql.MySQLError as e:
                print(f"Error creating table: {e}")

        # Option 2: Display tables of database
        elif ch == 2:
            try:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                for table in tables:
                    print(table[0])
            except pymysql.MySQLError as e:
                print(f"Error displaying tables: {e}")

        # Option 3: Show fields of a table
        elif ch == 3:
            try:
                table = input("Enter table name: ")
                cursor.execute(f"DESCRIBE {table}")
                fields = cursor.fetchall()
                for field in fields:
                    print(field)
            except pymysql.MySQLError as e:
                print(f"Error describing table: {e}")

        # Option 4: Display all student data
        elif ch == 4:
            try:
                cursor.execute("SELECT * FROM student")
                data = cursor.fetchall()
                print("ROLL NO | STUDENT NAME | CLASS | SECTION | SUBJECT1 | SUBJECT2 | SUBJECT3 | SUBJECT4 | SUBJECT5 | TOTALMARKS | PERCENTAGE")
                for row in data:
                    print(" | ".join(map(str, row)))
            except pymysql.MySQLError as e:
                print(f"Error fetching data: {e}")

        # Option 5: Add new student
        elif ch == 5:
            try:
                r = int(input("Enter student roll number: "))
                name = input("Enter student name: ")
                c = input("Enter class of student: ")
                s = input("Enter section of student: ")
                m1 = int(input("Enter marks in subject 1: "))
                m2 = int(input("Enter marks in subject 2: "))
                m3 = int(input("Enter marks in subject 3: "))
                m4 = int(input("Enter marks in subject 4: "))
                m5 = int(input("Enter marks in subject 5: "))
                total = m1 + m2 + m3 + m4 + m5
                per = total / 5

                query = """
                    INSERT INTO student (ROLL, name, class, sec, mark1, mark2, mark3, mark4, mark5, total, per)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (r, name, c, s, m1, m2, m3, m4, m5, total, per))
                db.commit()
                print("STUDENT RECORD SAVED IN TABLE")
            except pymysql.MySQLError as e:
                print(f"Error inserting record: {e}")

        # Option 6: Search student record
        elif ch == 6:
            print("1: Search by roll number")
            print("2: Search by name")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                try:
                    roll = int(input("Enter student roll number: "))
                    query = "SELECT * FROM student WHERE roll = %s"
                    cursor.execute(query, (roll,))
                    data = cursor.fetchall()
                    if not data:
                        print("STUDENT NOT FOUND")
                    else:
                        print("ROLL NO | STUDENT NAME | CLASS | SECTION | SUBJECT1 | SUBJECT2 | SUBJECT3 | SUBJECT4 | SUBJECT5 | TOTALMARKS | PERCENTAGE")
                        for row in data:
                            print(" | ".join(map(str, row)))
                except pymysql.MySQLError as e:
                    print(f"Error searching record: {e}")

            elif choice == 2:
                try:
                    name = input("Enter student name: ")
                    query = "SELECT * FROM student WHERE name = %s"
                    cursor.execute(query, (name,))
                    data = cursor.fetchall()
                    if not data:
                        print("STUDENT NOT FOUND")
                    else:
                        print("ROLL NO | STUDENT NAME | CLASS | SECTION | SUBJECT1 | SUBJECT2 | SUBJECT3 | SUBJECT4 | SUBJECT5 | TOTALMARKS | PERCENTAGE")
                        for row in data:
                            print(" | ".join(map(str, row)))
                except pymysql.MySQLError as e:
                    print(f"Error searching record: {e}")

        # Option 7: Update student marks
        elif ch == 7:
            try:
                roll = int(input("Enter roll number of student to update marks: "))
                cursor.execute("SELECT * FROM student WHERE roll = %s", (roll,))
                data = cursor.fetchall()
                if not data:
                    print("STUDENT NOT FOUND")
                else:
                    m1 = int(input("Enter updated marks in subject 1: "))
                    m2 = int(input("Enter updated marks in subject 2: "))
                    m3 = int(input("Enter updated marks in subject 3: "))
                    m4 = int(input("Enter updated marks in subject 4: "))
                    m5 = int(input("Enter updated marks in subject 5: "))
                    total = m1 + m2 + m3 + m4 + m5
                    per = total / 5

                    query = """
                        UPDATE student
                        SET mark1 = %s, mark2 = %s, mark3 = %s, mark4 = %s, mark5 = %s, total = %s, per = %s
                        WHERE roll = %s
                    """
                    cursor.execute(query, (m1, m2, m3, m4, m5, total, per, roll))
                    db.commit()
                    print("STUDENT RECORD UPDATED")
            except pymysql.MySQLError as e:
                print(f"Error updating record: {e}")

        # Option 8: Delete student record
        elif ch == 8:
            try:
                roll = int(input("Enter student roll number to delete: "))
                cursor.execute("SELECT * FROM student WHERE roll = %s", (roll,))
                data = cursor.fetchall()
                if not data:
                    print("STUDENT NOT FOUND")
                else:
                    cursor.execute("DELETE FROM student WHERE roll = %s", (roll,))
                    db.commit()
                    print("STUDENT RECORD DELETED")
            except pymysql.MySQLError as e:
                print(f"Error deleting record: {e}")

        # Option 9: Exit
        elif ch == 9:
            print("Exiting program.")
            db.close()
            break

        else:
            print("Invalid choice. Try again.")

# Run the program
student_marks_management()
S
 
