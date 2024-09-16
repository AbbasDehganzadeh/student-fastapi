import tkinter as tk
from tkinter import messagebox
from request_api import createStudent, deleteStudent, listStudents, updateStudent

wind1 = tk.Tk()
wind1.title("Student management programme")
wind1.geometry("640x480")


def initStudents():
    global students
    students = listStudents()
    studentsData = [
        f"{student['name']} _ {student['lastname']}" for student in students
    ]
    return studentsData


def send_request():
    name_ = name.get()
    lname_ = lname.get()
    score_ = score.get()
    grade_ = grade.get()
    phone_ = phone.get()
    try:
        score_ = score_ if score != 0 else None
        grade_ = grade_ if grade != 0 else None
        if ID:
            updateStudent(ID, name_, lname_, phone_, score_, grade_)
    except NameError as e:
        print("Error({})".format(e))
        createStudent(name_, lname_, phone_, score_, grade_)
    finally:
        print(name_, lname_, score_, grade_, phone_)

        studentsObj.set(initStudents())  # update the list
        newStudent()  # refresh the input


def selectStudent(*args):
    global ID
    idx = lists.curselection()
    lists.see(int(idx[0]))
    stu = students[int(idx[0])]
    ID = stu.get("_id")
    # print("ID:\t", ID)
    name.set(stu.get("name"))
    lname.set(stu.get("lastname"))
    score.set(stu.get("score", 0))
    grade.set(stu.get("grade", 0))
    phone.set(stu.get("phonenumber", ""))


def newStudent():
    global ID
    name.set("")
    lname.set("")
    score.set(0)
    grade.set(0)
    phone.set("")
    try:
        del ID
    except NameError as e:
        print("Error({})".format(e))


def delStudent():
    try:
        print("del: ID = ", ID)
        if ID:
            result = messagebox.askretrycancel("DELETE", "آیا مظینید.")
            if result:
                ok = deleteStudent(ID)
    except NameError as e:
        print("Error({})".format(e))
    finally:
        studentsObj.set(initStudents())  # update the list
        newStudent()  # refresh the input


name = tk.StringVar()
inp_name = tk.Entry(wind1, textvariable=name)
lbl_name = tk.Label(wind1, text="نام", padx=5)
lname = tk.StringVar()
inp_lname = tk.Entry(wind1, textvariable=lname)
lbl_lname = tk.Label(wind1, text="نام خانوادگی", padx=5)
score = tk.DoubleVar()
inp_score = tk.Entry(wind1, textvariable=score, fg="aqua")
lbl_score = tk.Label(wind1, text="نمره", padx=5)
grade = tk.IntVar()
inp_grade = tk.Entry(wind1, textvariable=grade, fg="magenta")
lbl_grade = tk.Label(wind1, text="کلاس", padx=5)
phone = tk.StringVar()
inp_phone = tk.Entry(wind1, textvariable=phone)
lbl_phone = tk.Label(wind1, text="تلفن", padx=5)

## place input widget ##
lbl_name.grid(row=1, column=0)
inp_name.grid(row=1, column=1)
lbl_lname.grid(row=2, column=0)
inp_lname.grid(row=2, column=1)
lbl_score.grid(row=3, column=0)
inp_score.grid(row=3, column=1)
lbl_grade.grid(row=4, column=0)
inp_grade.grid(row=4, column=1)
lbl_phone.grid(row=5, column=0)
inp_phone.grid(row=5, column=1)
btn_signup = tk.Button(wind1, command=send_request, text="ثبت مشخصات", bg="cyan")
btn_signup.grid(row=7, column=0, rowspan=2, columnspan=2)
btn_refresh = tk.Button(
    wind1, command=newStudent, text="دانش آموز جدید", bg="maroon", fg="white smoke"
)
btn_refresh.grid(row=7, column=1, rowspan=2, columnspan=2)
btn_refresh = tk.Button(
    wind1, command=delStudent, text="حذف دانش آموز", bg="firebrick", fg="yellow2"
)
btn_refresh.grid(row=7, column=2)

## list of users ##
csrl = tk.Frame(wind1, bg="grey")
csrl.grid(row=10, column=0, rowspan=2, columnspan=2)
studentsObj = tk.StringVar(value=initStudents())
lists = tk.Listbox(csrl, listvariable=studentsObj)
lists.bind("<<ListboxSelect>>", selectStudent)
lists.pack()

wind1.mainloop()
