# IMPORTS
from tkinter import*  #import tkinter module
from tkinter import ttk # import themed tkinter widgets

# FILE PATH
DATA_FILE = "Assessment 1 - Skills Portfolio/A1 - Resources/Random jokes/students mark/studentMarks.txt"

# SAFE INTEGER PARSER
def parse_int_safe(s, default=0):#safely convert string to integer, return default if fails
    try: return int(str(s).strip())
    except: return default

# LOAD STUDENTS
def load_students():# load student records from file into list of dictionaries
    students = []
    try:
        with open(DATA_FILE, "r") as f:
            lines = f.readlines() # read all lines
        for line in lines[1:]:# skip first line (student count)
            p = [x.strip() for x in line.split(",")]#split by comma
            if len(p) != 6: continue# skip malformed lines
            code = parse_int_safe(p[0])#student code
            name = p[1]#student name
            c1, c2, c3 = map(parse_int_safe, p[2:5])# coursework marks
            exam = parse_int_safe(p[5])# exam mark
            if not (1000 <= code <= 9999): continue# validate code
            if not name: continue # skip if name empty

            # append validated student record

            students.append({
                "code": code,
                "name": name,
                "c1": min(max(c1,0),20),
                "c2": min(max(c2,0),20),
                "c3": min(max(c3,0),20),
                "exam": min(max(exam,0),100)
            })
    except:
        pass
    return students

# SAVE STUDENTS
def save_students(students):# save student records back to file
    try:
        with open(DATA_FILE, "w") as f:# open file for writing
            f.write(str(len(students)) + "\n")# write count

            for s in students: # write each student
                f.write(f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")
        return True
    except:
        return False

# MARK CALCULATIONS
def coursework_total(s): return s["c1"] + s["c2"] + s["c3"]# return total coursework marks
def overall_percentage(s): return (coursework_total(s) + s["exam"]) / 160 * 100# return overall percentage out of 160
def grade_from_percentage(p):# return grade letter based on percentage
    return "A" if p>=70 else "B" if p>=60 else "C" if p>=50 else "D" if p>=40 else "F"

# FORMAT SUMMARY
def format_summary(s):# format student record into readable string
    pct = overall_percentage(s)
    return (
        f"Name: {s['name']}\n"
        f"Code: {s['code']}\n"
        f"Coursework: {coursework_total(s)} / 60\n"
        f"Exam: {s['exam']} / 100\n"
        f"Overall: {pct:.2f}%\n"
        f"Grade: {grade_from_percentage(pct)}\n"
        "-------------------------\n"
    )

# APP CLASS
class StudentApp:# main tkinter app class
    def __init__(self, root):
        self.root = root # root window
        self.root.title("Student Manager")#window title
        self.root.geometry("850x550")#window size
        self.root.configure(bg="#FFB6C1")#window background
        self.students = load_students()

        # LEFT MENU
        self.left = Frame(root, bg="#FFB6C1", width=250) # left panel
        self.left.pack(side=LEFT, fill=Y)
        Label(self.left, text="Menu", font=("Poppins",16,"bold"),
              bg="#FFB6C1", fg="#333").pack(pady=10)#menu header

       #MENU BUTTONS
        self.make_btn("View All", self.view_all)
        self.make_btn("View Individual", self.view_individual)
        self.make_btn("Highest Mark", self.highest)
        self.make_btn("Lowest Mark", self.lowest)
        self.make_btn("Sort Records", self.sort_records)
        self.make_btn("Add Record", self.add_record)
        self.make_btn("Delete Record", self.delete_record)
        self.make_btn("Update Record", self.update_record)

        # RIGHT PANEL
        self.right = Frame(root, bg="white")# right panel
        self.right.pack(side=RIGHT, fill=BOTH, expand=True)
        self.header = Label(self.right, text="Welcome",
                            font=("Poppins",18,"bold"),
                            bg="white", fg="#333")#header
        self.header.pack(pady=10)
        self.output = Text(self.right, font=("Poppins",11), bg="#FFF0F5")
        self.output.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # BUTTON BUILDER
    def make_btn(self, text, cmd):
        Button(self.left, text=text, bg="#FFF0F5", fg="#333",
               font=("Poppins",11), relief="ridge",
               command=cmd).pack(fill=X, padx=10, pady=5)

    # CLEAR OUTPUT
    def clr(self, title):# clear output area and set header
        self.header.config(text=title)
        self.output.delete("1.0", END)

    # VIEW ALL
    def view_all(self):#Display all student record
        self.clr("All Records")
        if not self.students: return self.output.insert(END,"No data\n")
        for s in self.students:
            self.output.insert(END, format_summary(s))

    # VIEW INDIVIDUAL
    def view_individual(self): # search for student by code or name
        self.clr("Search Student")
        win = Toplevel(self.root)#pop up window
        win.title("Search")
        win.geometry("300x200")

        Label(win, text="Enter Code or Name").pack(pady=10)#entry field
        entry = Entry(win); entry.pack()

        def search():
            q = entry.get().strip().lower() # loop through all student record
            for s in self.students:# check if query matches student code or name
                if q == str(s["code"]) or q == s["name"].lower(): # if found, insert formatted summary into output area
                    self.output.insert(END, format_summary(s))
                    win.destroy()# close the popup window
                    return
            self.output.insert(END, "Not found\n")#if not found, display message
            win.destroy()
        Button(win, text="Search", command=search).pack(pady=10)#search button

    # HIGHEST
    def highest(self): # clear output and set header
        self.clr("Highest Mark")
        if not self.students: return#if no students, return
        s = max(self.students, key=overall_percentage)#student with maximum overal percentage
        self.output.insert(END, format_summary(s))# display summary

    # LOWEST
    def lowest(self):# clear output and set header
        self.clr("Lowest Mark")
        if not self.students: return#if no students, return
        s = min(self.students, key=overall_percentage)#student with minimum overal percentage
        self.output.insert(END, format_summary(s))#display summary

    # SORT
    def sort_records(self):#clear output and set header
        self.clr("Sorted Records")# sort students by percentage descending
        self.students.sort(key=overall_percentage, reverse=True)#display all sorted records
        for s in self.students:
            self.output.insert(END, format_summary(s))# save sorted list back to file
        save_students(self.students)

    # ADD
    def add_record(self):# clear output and set header

        self.clr("Add New Record")
# create popup window for adding record
        win = Toplevel(self.root)
        win.title("Add Record")
        win.geometry("300x400")
        fields = ["Code","Name","C1","C2","C3","Exam"]#fields and dictionary
        entries = {}

        for f in fields:
            Label(win, text=f).pack()
            e = Entry(win); e.pack()
            entries[f] = e

        def add():
            code = parse_int_safe(entries["Code"].get())#values from entry fields
            name = entries["Name"].get().strip()
            c1 = parse_int_safe(entries["C1"].get())
            c2 = parse_int_safe(entries["C2"].get())
            c3 = parse_int_safe(entries["C3"].get())
            exam = parse_int_safe(entries["Exam"].get())

            if not (1000 <= code <= 9999) or not name:# validate code and name
             return self.output.insert(END,"Invalid input\n")

            for s in self.students:# check for duplicate code
                if s["code"] == code:
                    return self.output.insert(END,"Code exists\n")

            new_s = {# create new student dictionary
                "code": code,"name": name,
                "c1": min(max(c1,0),20),
                "c2": min(max(c2,0),20),
                "c3": min(max(c3,0),20),
                "exam": min(max(exam,0),100)
            }
            self.students.append(new_s)#append to list
            save_students(self.students)
            self.output.insert(END,"Added:\n"+format_summary(new_s))
            win.destroy()

        Button(win,text="Add",command=add).pack(pady=10)#add button in popup

    # DELETE
    def delete_record(self):
        self.clr("Delete Record")# clear output and set header
        win = Toplevel(self.root)#pop up winodw
        win.geometry("300x150")
        Label(win, text="Code or Name").pack()
        entry = Entry(win); entry.pack()

        def delete():#query
            q = entry.get().strip().lower()#loop through students
            for i,s in enumerate(self.students):
                if q == str(s["code"]) or q == s["name"].lower():#if found,delete record
                    self.output.insert(END,f"Deleted {s['name']}\n")
                    self.students.pop(i)
                    save_students(self.students)
                    win.destroy()
                    return
            self.output.insert(END,"Not found\n")#ifn ot found
            win.destroy()
        Button(win,text="Delete",command=delete).pack(pady=10)#delete button

    # UPDATE
    def update_record(self): # clear output and set header
        self.clr("Update Record")
        win = Toplevel(self.root)#pop up winodw
        win.geometry("300x350")

        Label(win, text="Search Code/Name").pack()
        search = Entry(win); search.pack() # search field
#new value field
        Label(win,text="New Name").pack(); n_name = Entry(win); n_name.pack()
        Label(win,text="New C1").pack(); n_c1 = Entry(win); n_c1.pack()
        Label(win,text="New C2").pack(); n_c2 = Entry(win); n_c2.pack()
        Label(win,text="New C3").pack(); n_c3 = Entry(win); n_c3.pack()
        Label(win,text="New Exam").pack(); n_exam = Entry(win); n_exam.pack()
        def update():#query
            q = search.get().strip().lower()# loop through students
            for s in self.students:
                if q == str(s["code"]) or q == s["name"].lower():
                    # update fields 
                    if n_name.get().strip(): s["name"] = n_name.get().strip()
                    if n_c1.get(): s["c1"] = min(max(parse_int_safe(n_c1.get()),0),20)
                    if n_c2.get(): s["c2"] = min(max(parse_int_safe(n_c2.get()),0),20)
                    if n_c3.get(): s["c3"] = min(max(parse_int_safe(n_c3.get()),0),20)
                    if n_exam.get(): s["exam"] = min(max(parse_int_safe(n_exam.get()),0),100)
                    save_students(self.students)
                    # display confirmation
                    self.output.insert(END, "Updated:\n" + format_summary(s))
                    win.destroy()
                    return
            self.output.insert(END,"Not found\n")
            win.destroy()
        Button(win,text="Update",command=update).pack(pady=10)#update button
# MAIN
if __name__ == "__main__":
    root = Tk() # create root window
    app = StudentApp(root)
    root.mainloop()#run mainloop
