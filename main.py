from tkinter import *
from record_db import connect
import bcrypt
from tkinter import messagebox as msg

def validate_numeric_input(char):
    return char.isdigit() or char == ""

def sign_up():
    # from main import main_screen
    global register_screen
    global surname
    global other_names
    global password
    global gender
    global email
    global phone_number
  

    global surname_entry
    global other_names_entry
    global password_entry
    global gender_entry
    global email_entry
    global phone_number_entry
   

    register_screen = Toplevel(main_screen)
    register_screen.geometry("700x600")
    register_screen.title("Register your details")
    register_screen.configure(bg="lightyellow")

    surname = StringVar()
    other_names = StringVar()
    password = StringVar()
    gender = StringVar()
    email = StringVar()
    phone_number = StringVar()

    validate_cmd = register_screen.register(validate_numeric_input)

    Label(register_screen, text="", bg="lightyellow").pack()
    Label(register_screen, text="Enter your following details", bg="dark gray", font=("calibri", 13)).pack()
    
    surname_label = Label(register_screen, text="Surname * ", bg="lightyellow")
    surname_label.pack()
    surname_entry = Entry(register_screen, textvariable=surname)
    surname_entry.pack()

    other_names_label = Label(register_screen, text="Other_Names * ", bg="lightyellow")
    other_names_label.pack()
    other_names_entry = Entry(register_screen, textvariable=other_names)
    other_names_entry.pack()

    password_label = Label(register_screen, text="Password * ", bg="lightyellow")
    password_label.pack()
    password_entry = Entry(register_screen, textvariable=password, show="*")
    password_entry.pack()

    
    gender_label = Label(register_screen, text="Gender * ", bg="lightyellow")
    gender_label.pack()
    gender_entry = Entry(register_screen, textvariable=gender)
    gender_entry.pack()

    email_label = Label(register_screen, text="Email * ", bg="lightyellow")
    email_label.pack()
    email_entry = Entry(register_screen,textvariable=email)
    email_entry.pack()

    phone_number_label = Label(register_screen, text="Phone_Number * ", bg="lightyellow")
    phone_number_label.pack()
    phone_number_entry = Entry(register_screen, textvariable=phone_number)
    phone_number_entry.pack()

    
    Label(register_screen, text="", bg="lightyellow").pack()
    Button(register_screen, text="Submit", bg="dark gray", font=("calibri", 13), width=13, height=1, command=register_user).pack()

def register_user():
    surname_info = surname.get()
    other_names_info =other_names.get()
    password_info = password.get()
    gender_info = gender.get()
    email_info = email.get()
    phone_number_info = phone_number.get()  
    hashed_password = bcrypt.hashpw(password_info.encode('utf-8'), bcrypt.gensalt())
    

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO student(surname, other_names, password, gender, email, phone_number)
        VALUES(%s, %s, %s, %s, %s, %s)
        """, (surname_info, other_names_info,  hashed_password.decode("utf-8"), gender_info, email_info, phone_number_info)
    )
    conn.commit()
    conn.close()
    cur.close()

    surname_entry.delete(0, END)
    other_names_entry.delete(0, END)
    password_entry.delete(0, END)
    gender_entry.delete(0, END)
    email_entry.delete(0, END)
    phone_number_entry.delete(0, END)
    Label(register_screen, text=(f"Registration Successully."), fg="dark gray", font=("Calibri, 13")).pack()

# REGISTER END

# LOGIN BEGIn

def login():
    global login_screen
    global email_entry
    global password_entry
    login_screen = Toplevel(main_screen)
    login_screen.title("login")
    login_screen.geometry("600x700")
    login_screen.configure(bg="lightyellow")
                           
    email = StringVar()
    password = StringVar()

    Label(login_screen, text="Enter your details correctly", bg="dark gray", font=("calibri", 13)).pack()

    email_label = Label(login_screen, text="Email * ", bg="lightyellow")
    email_label.pack()
    email_entry = Entry(login_screen, textvariable=email)
    email_entry.pack()

    password_label = Label(login_screen, text="Password * ", bg="lightyellow")
    password_label.pack()
    password_entry = Entry(login_screen, textvariable=password, show="*")
    password_entry.pack()

    Label(login_screen, text="", bg="lightyellow").pack()
    Button(login_screen, text="Login", bg="dark gray", command=login_verify).pack()

def login_verify():
    email_info = email_entry.get()
    password_info = password_entry.get()

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT password FROM student WHERE email = %s
        """,(email_info,)
    )
    result = cur.fetchone()
    conn.close()

    if result:
        stored_hashed_password = result[0].encode('utf-8')
        if bcrypt.checkpw(password_info.encode("utf-8"), stored_hashed_password):
            login_successful()
        else: 
            password_invalid()    
    else:
        student_not_found()   

def login_successful():
    global login_successful_screen
    login_successful_screen = Toplevel(login_screen)
    login_successful_screen.title("Login successful")   
    login_successful_screen.geometry("150x100")
    login_successful_screen.configure(bg="lightyellow")

    Label(login_successful_screen, text="Login Successfully", bg="dark gray", font=("calibri", 13)).pack()
    Button(login_successful_screen, text="Login", bg="darkgray",  width="30", height="2", font=("Arial Bold", 10), command=menu).pack()

def student_not_found():
    global student_not_found_screen
    student_not_found_screen = Toplevel(login_screen)
    student_not_found_screen.title("Failed")
    student_not_found_screen.geometry("150x100")
    student_not_found_screen.configure(bg="lightyellow")

    Label(student_not_found_screen, text="Student not found", bg="dark gray", font=("calibri", 13)).pack()
    Button(student_not_found_screen, text="OK", bg="dark gray",  width= "30", height="2", font=("Arial Bold", 10), command=delete_student_not_found).pack()

def delete_student_not_found():
    student_not_found_screen.destroy()

def password_invalid():
    global password_invalid_screen
    password_invalid_screen = Toplevel(login_screen)
    password_invalid_screen.title("Password")
    password_invalid_screen.geometry("150x100")
    password_invalid_screen.configure(bg="lightyellow")

    Label(password_invalid_screen, text="Invalid Password", bg="dark gray", font=("calibri", 13)).pack()
    Button(password_invalid_screen, text="OK", bg="dark gray",  width="30", height="2", font=("Arial Bold", 10), command=delete_password_invalid).pack()

def delete_password_invalid():
    password_invalid_screen.destroy()
#    LOGIN_END

def student_detalis():
    global student_details_screen
    global name 
    global gender
    global matrix_number
    global math_score
    global phy_score
    global chm_score
    global name_entry
    global gender_entry
    global matrix_number_entry
    global math_score_entry
    global phy_score_entry
    global chm_score_entry

    student_details_screen = Toplevel(main_screen)
    student_details_screen.title("Student_Scores")
    student_details_screen.geometry("600x700")
    student_details_screen.configure(bg="lightyellow")
                           


    name = StringVar()
    gender = StringVar()
    matrix_number = StringVar()
    math_score= StringVar()
    phy_score= StringVar()
    chm_score = StringVar()

    validate_cmd = student_details_screen.register(validate_numeric_input)

    name_label = Label(student_details_screen, text="name * ", bg="lightyellow")
    name_label.pack()
    name_entry = Entry(student_details_screen, textvariable=name)
    name_entry.pack()
    
    gender_label = Label(student_details_screen, text="Gender * ", bg="lightyellow")
    gender_label.pack()
    gender_entry = Entry(student_details_screen, textvariable=gender)
    gender_entry.pack()
    
    matrix_number_label = Label(student_details_screen, text="Matrix_number * ", bg="lightyellow")
    matrix_number_label.pack()
    matrix_number_entry = Entry(student_details_screen, textvariable=matrix_number)
    matrix_number_entry.pack()
    
    math_score_label = Label(student_details_screen, text="Mathematics * ", bg="lightyellow")
    math_score_label.pack()
    math_score_entry = Entry(student_details_screen, textvariable=math_score, validatecommand=(validate_cmd, "%S"))
    math_score_entry.pack()

    phy_score_label = Label(student_details_screen, text="Physics * ", bg="lightyellow")
    phy_score_label.pack()
    phy_score_entry = Entry(student_details_screen, textvariable=phy_score, validatecommand=(validate_cmd, "%S"))
    phy_score_entry.pack()

    chm_score_label = Label(student_details_screen, text="Chemistry * ", bg="lightyellow")
    chm_score_label.pack()
    chm_score_entry = Entry(student_details_screen, textvariable=chm_score, validatecommand=(validate_cmd, "%S"))
    chm_score_entry.pack()

    Label(text="", bg="lightyellow").pack()
    Label(student_details_screen, text="", bg="lightyellow").pack()
    Button(student_details_screen, text="Submit", bg="dark gray", font=("calibri", 13), width=13, height=1, command=student_detalis_verify).pack()

def student_detalis_verify():
    conn = connect()
    cur = conn.cursor()

    name_info = name.get()
    gender_info = gender.get()
    matrix_number_info = matrix_number.get()
    math_score_info = math_score.get()
    phy_score_info = phy_score.get()
    chm_score_info = chm_score.get()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*) FROM exam_records WHERE matrix_number = %s
        """, (matrix_number_info,)
    )
    count = cur.fetchone()[0]

    if count > 0:
        cur.close()
        conn.close()
        return msg.showerror("Error", "Matric number already exists.")
    else:
        cur.execute(
            """
            INSERT INTO exam_records (name, gender, matrix_number, math_score, phy_score, chm_score)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (
            name_info,
            gender_info,
            matrix_number_info,
            math_score_info,
            phy_score_info,
            chm_score_info
        )  
    )
    conn.commit()
    cur.close()
    conn.close()
    Label(student_details_screen, text=(f"Data Saved Successully."), bg="dark gray", font=("Calibri, 13")).pack()
    Label(text="", bg="lightyellow").pack()
    Button(student_details_screen, text="ok", bg="dark gray", font=("calibri", 13), width=13, height=1, command=display).pack()


def display():
    global display_screen
    global matrix_number_entry
    display_screen = Toplevel(login_screen)
    display_screen.title("Check Detalis")   
    display_screen.geometry("600x700")
    display_screen.configure(bg="lightyellow")

    Label(display_screen, text="Enter a Matrix Number", bg="dark gray", font=("calibri", 13)).pack()

    matrix_number = StringVar()
    Label(display_screen, text="", bg="lightyellow").pack()
    matrix_number_entry = Entry(display_screen, textvariable=matrix_number)
    matrix_number_entry.pack()

    Label(display_screen, text="", bg="lightyellow").pack()
    Button(display_screen, text="OK", bg="dark gray",  width="30", height="2", font=("Arial Bold", 10), command=display_verify).pack()

def display_verify():
    matrix_number_info = matrix_number_entry.get()
    if matrix_number_info == "":
        Label(display_screen, text="Plase enter a valid Matrix Number", bg="dark gray", font=("calibri", 13)).pack()
        return

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """ SELECT name, gender, math_score, phy_score, chm_score FROM exam_records WHERE matrix_number = %s
        """,(matrix_number_info,)
    )
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        name_info, gender_info, math_score, phy_score, chm_score = result
        display_student_result(name_info, gender_info, math_score, phy_score, chm_score, matrix_number_info)
    else:
        Label(display_screen, text="Matrix Number not found", bg="dark gray", font=("calibri", 13)).pack()

def display_student_result(name, gender, math_score, phy_score, chm_score, matrix_number_info):
    for widget in display_screen.winfo_children():
        widget.destroy()

    Label(display_screen, text="Student Details", bg="dark gray", font=("calibri", 14), width=300, height=1).pack()

    Label(display_screen, text=f"Name: {name}", bg="lightyellow", font=("calibri", 13)).pack()             
    Label(display_screen, text=f"Gender: {gender}", bg="lightyellow", font=("calibri", 13)).pack()
    Label(display_screen, text=f"Maths score: {math_score}", bg="lightyellow", font=("calibri", 13)).pack()                          
    Label(display_screen, text=f"Physics score: {phy_score}", bg="lightyellow", font=("calibri", 13)).pack()             
    Label(display_screen, text=f"Chemistry score: {chm_score}", bg="lightyellow", font=("calibri", 13)).pack()             

    Label(display_screen, text="",bg="lightyellow").pack() 
    Button(display_screen, text="Update", bg="lightyellow", font=("calibri", 13), width=13, height=1, command=lambda: Update_details (matrix_number_info)).pack()
    Button(display_screen, text="Delete", bg="lightyellow", font=("calibri", 13), width=13, height=1, command=lambda: Delete_details (matrix_number_info)).pack()
    Button(display_screen, text="OK", bg="lightyellow", font=("calibri", 13), width=13, height=1, command=display_screen.destroy).pack()

def Update_details(matrix_number_info):
    global Update_screen
    global math_score_entry, phy_score_entry, chm_score_entry

    Update_screen = Toplevel(display_screen)
    Update_screen.geometry("600x700")
    Update_screen.title("Update Student Result")

    math_score = StringVar()
    phy_score = StringVar()
    chm_score = StringVar()

    Label(Update_screen, text="update the details", bg="dark gray", font=("calibri", 13), width=300, height=1).pack()

    Label(Update_screen, text="Maths Score *", bg="lightyellow").pack()
    math_score_entry = Entry(Update_screen, textvariable=math_score)
    math_score_entry.pack()

    Label(Update_screen, text="Physics Score *", bg="lightyellow").pack()
    phy_score_entry = Entry(Update_screen, textvariable=phy_score)
    phy_score_entry.pack()

    Label(Update_screen, text="Chemistry Score *", bg="lightyellow").pack()
    chm_score_entry = Entry(Update_screen, textvariable=chm_score)
    chm_score_entry.pack()

    Label(Update_screen, text="", bg="lightyellow").pack()
    Button(Update_screen, text="Update", bg="lightyellow", font=("calibri", 13), width=13, height=1, command=lambda: Update_detailss (matrix_number_info)).pack()

def Update_detailss(matrix_number_info):
    math_score_info = math_score_entry.get()
    phy_score_info = phy_score_entry.get()
    chm_score_info = chm_score_entry.get()

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """ 
        UPDATE exam_records SET math_score = %s, phy_score = %s, chm_score = %s WHERE matrix_number = %s
        """, (math_score_info, phy_score_info, chm_score_info, matrix_number_info)
    )
    conn.commit()
    cur.close()
    conn.close()

    Label(Update_screen, text="Result updated successfully", bg="dark gray", font=("calibri", 13)).pack()

    math_score_entry.delete(0, END)
    phy_score_entry.delete(0, END)
    chm_score_entry.delete(0, END)

def Delete_details(matrix_number_info):
    conform = msg.askyesno("Conform Delete", "Are you sure you want to delete this student record?")

    if conform:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM exam_records WHERE matrix_number = %s
            """, (matrix_number_info,)
        ) 
        conn.commit()
        cur.close()
        conn.close()   

        Label(display_screen, text="Detalis Deleted successfully", bg="dark gray", font=("calibri", 13)).pack()
        display_screen.destroy()
    else:
        Label(display_screen, text="Deletion Cancelled", bg="dark gray", font=("calibri", 13)).pack()    


def menu():
    global menu_screen 
    menu_screen = Toplevel(main_screen)
    menu_screen.title("Student_Record")
    menu_screen.geometry("300x250")
    menu_screen.configure(bg="lightyellow")

    Button(menu_screen, text="Add result", bg="white", width="30", height="2", font=("Arial Bold", 10), command=student_detalis).pack()
    Button(menu_screen, text="Edit/Delete result", bg="yellow", width="30", height="2", font=("Arial Bold", 10), command=display).pack()

def main_action_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("3000x2500")
    main_screen.title("student portal Register/Login")
    main_screen.configure(bg="lightyellow")

    Label(text="Select your choice", bg="lightyellow", width="300", height="2", font=("calibri", 13)).pack()
    Label(main_screen, text="", bg="lightyellow").pack()

    Button(text="Register", bg="white", width="30", height="2", font=("Arial Bold", 10), command=sign_up).pack()
    Button(text="Login", bg="yellow", width="30", height="2", font=("Arial Bold", 10), command=login).pack()
    
    main_screen.mainloop()

main_action_screen()