# ============================================================
#   Smart Student Management System
#   Group Assignment 1 — OOP in Python
#   Features: step-by-step form, back navigation, preview,
#             edit after save, full input validation
# ============================================================

# ─────────────────────────────────────────────────────────────
#  UTILITIES — colors and display
# ─────────────────────────────────────────────────────────────

class C:
    """ANSI color shortcuts."""
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    DIM    = "\033[2m"

def clr(text, color): return f"{color}{text}{C.RESET}"
def ok(text):         return clr(f"  ✔  {text}", C.GREEN)
def warn(text):       print(clr(f"  ⚠  {text}", C.YELLOW))
def err(text):        print(clr(f"  ✘  {text}", C.RED))
def title(text):      print(f"\n{C.BOLD}{C.CYAN}{'═'*60}\n  {text}\n{'═'*60}{C.RESET}")
def section(text):    print(f"\n{C.BOLD}{C.BLUE}  ── {text} {'─'*(52-len(text))}{C.RESET}")
def hint(text):       print(clr(f"  ↩  (Press Enter with nothing to {text})", C.DIM))


# ─────────────────────────────────────────────────────────────
#  PART 1 — FOUNDATIONS: input helpers with validation
# ─────────────────────────────────────────────────────────────

def get_string(prompt, current=None, allow_back=False):
    """
    Read a non-empty string.
    If current is set, pressing Enter keeps the current value.
    If allow_back, typing '0' goes back (returns None).
    """
    if current is not None:
        hint(f"keep \"{current}\"")
    if allow_back:
        hint("go back: type 0")
    while True:
        value = input(f"{C.BOLD}  {prompt}{C.RESET}").strip()
        if allow_back and value == "0":
            return None             # back signal
        if value == "" and current is not None:
            return current          # keep existing value
        if value:
            return value
        err("This field is required.")


def get_integer(prompt, lo, hi, current=None, allow_back=False):
    """Read and validate an integer within [lo, hi]."""
    if current is not None:
        hint(f"keep {current}")
    if allow_back:
        hint("go back: type 0")
    while True:
        try:
            raw = input(f"{C.BOLD}  {prompt}{C.RESET}").strip()
            if allow_back and raw == "0":
                return None
            if raw == "" and current is not None:
                return current
            value = int(raw)
            if lo <= value <= hi:
                return value
            err(f"Please enter a number between {lo} and {hi}.")
        except ValueError:
            err("Please enter a whole number.")


def get_float_val(prompt, lo, hi, current=None, default=None, allow_back=False):
    """Read and validate a float within [lo, hi]. Supports default and back."""
    if current is not None:
        hint(f"keep {current:,.0f}")
    elif default is not None:
        hint(f"default: {default:,.0f}")
    if allow_back:
        hint("go back: type 0")
    while True:
        try:
            raw = input(f"{C.BOLD}  {prompt}{C.RESET}").strip()
            if allow_back and raw == "0":
                return None
            if raw == "" and current is not None:
                return current
            if raw == "" and default is not None:
                return float(default)
            value = float(raw)
            if lo <= value <= hi:
                return value
            err(f"Please enter a value between {lo} and {hi}.")
        except ValueError:
            err("Please enter a valid number.")


def get_choice(prompt, options, allow_back=False):
    """Numbered menu. options = list of (label, value)."""
    for i, (label, _) in enumerate(options, 1):
        print(f"  {C.CYAN}{i}{C.RESET}. {label}")
    if allow_back:
        print(f"  {C.DIM}0. ← Go back{C.RESET}")
    while True:
        raw = input(f"{C.BOLD}  {prompt}{C.RESET}").strip()
        if allow_back and raw == "0":
            return None
        try:
            idx = int(raw)
            if 1 <= idx <= len(options):
                return options[idx - 1][1]
            err(f"Please choose between 1 and {len(options)}.")
        except ValueError:
            err("Please enter a number.")


def get_yes_no(prompt):
    """Read a yes/no answer."""
    while True:
        raw = input(f"{C.BOLD}  {prompt} (y/n): {C.RESET}").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        err("Please answer y or n.")


# ─────────────────────────────────────────────────────────────
#  PART 2 — FOUNDATIONS + INHERITANCE: classes
# ─────────────────────────────────────────────────────────────

class Person:
    """
    Parent class: holds basic personal information.
    Data types used: str (name, person_id, membership_type), int (age)
    """

    total_persons: int = 0   # class variable shared by all instances

    def __init__(self, name: str, person_id: str, age: int, membership_type: str):
        self.name            = name             # str
        self.person_id       = person_id        # str
        self.age             = age              # int
        self.membership_type = membership_type  # str
        Person.total_persons += 1

    # ── PART 3: Magic methods ────────────────────────────────

    def __str__(self) -> str:
        """Human-readable string — used by print()."""
        mt     = str(self.membership_type or "").strip()
        member = mt.title() if mt and mt.lower() != "none" else "None"
        return (f"{self.name}  (ID: {self.person_id} | "
                f"Age: {self.age} | Membership: {member})")

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Person(id={self.person_id!r}, name={self.name!r})"

    def __eq__(self, other) -> bool:
        """Two persons are equal if they share the same ID."""
        if not isinstance(other, Person):
            return NotImplemented
        return self.person_id == other.person_id

    # ── PART 4: Decorators ───────────────────────────────────

    @staticmethod
    def validate_age(age: int) -> bool:
        """Static utility — check if age is realistic (15–80)."""
        return isinstance(age, int) and 15 <= age <= 80

    @classmethod
    def get_total_persons(cls) -> int:
        """Class method — return the total number of Person instances."""
        return cls.total_persons

    def __del__(self):
        Person.total_persons -= 1


# ─────────────────────────────────────────────────────────────

class Student(Person):
    """
    Child class of Person.
    Adds academic attributes: specialty, annual_fees, grades (dict), gpa (float), admitted (bool).
    """

    ADMISSION_THRESHOLD  = 10.0   # minimum average to be admitted
    SCHOLARSHIP_THRESHOLD = 14.0  # minimum average for a scholarship

    def __init__(self, student_id: str, name: str, age: int,
                 membership_type: str, specialty: str, annual_fees: float):
        # Call parent constructor with super()
        super().__init__(name, student_id, age, membership_type)
        self.specialty   = specialty     # str
        self.annual_fees = annual_fees   # float
        self.grades      = {}            # dict {subject: grade}

    # ── PART 3: Magic methods ────────────────────────────────

    def __str__(self) -> str:
        avg = self.calculate_average()
        return (f"{super().__str__()} | Program: {self.specialty}"
                f" | Avg: {avg:.2f}/20")

    def __len__(self) -> int:
        """len(student) → number of subjects recorded."""
        return len(self.grades)

    def __repr__(self) -> str:
        return f"Student(id={self.person_id!r}, avg={self.calculate_average():.2f})"

    def __lt__(self, other) -> bool:
        """Allows sorting students by average grade."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.calculate_average() < other.calculate_average()

    def __add__(self, other):
        """Returns the student with the higher average."""
        if not isinstance(other, Student):
            return NotImplemented
        return self if self.calculate_average() >= other.calculate_average() else other

    # ── Academic methods ─────────────────────────────────────

    def add_grade(self, subject: str, grade: float) -> bool:
        """Add or update a grade for a subject."""
        if not (0 <= grade <= 20):
            return False
        self.grades[subject] = grade
        return True

    def calculate_average(self) -> float:
        """Arithmetic expression #1 — compute grade average."""
        if not self.grades:
            return 0.0
        return round(sum(self.grades.values()) / len(self.grades), 2)

    def is_admitted(self) -> bool:
        return self.calculate_average() >= self.ADMISSION_THRESHOLD

    def has_scholarship(self) -> bool:
        return self.calculate_average() >= self.SCHOLARSHIP_THRESHOLD

    # ── PART 4: @property decorator ──────────────────────────

    @property
    def discount_amount(self) -> float:
        """Arithmetic expression #2 — compute tuition discount."""
        rate  = 0.50 if self.has_scholarship() else (0.20 if self.is_admitted() else 0.0)
        mt    = str(self.membership_type or "").strip().lower()
        extra = 0.10 if mt and mt != "none" else 0.0
        return self.annual_fees * min(rate + extra, 0.9)

    @property
    def net_fees(self) -> float:
        """Arithmetic expression #3 — net fees after discount."""
        return self.annual_fees - self.discount_amount

    # ── PART 4: @staticmethod ────────────────────────────────

    @staticmethod
    def grade_to_letter(grade: float) -> str:
        """Convert a numeric grade to a letter grade."""
        if grade >= 18: return "A+"
        if grade >= 16: return "A"
        if grade >= 14: return "B"
        if grade >= 12: return "C"
        if grade >= 10: return "D"
        return "F"

    @classmethod
    def get_thresholds(cls):
        """Class method — return admission and scholarship thresholds."""
        return cls.ADMISSION_THRESHOLD, cls.SCHOLARSHIP_THRESHOLD


# ─────────────────────────────────────────────────────────────

class ScholarshipStudent(Student):
    """
    Child class of Student.
    Represents a student who holds an external scholarship.
    Extra attributes: scholarship_name, amount, sponsor, renewed (bool).
    """

    def __init__(self, student_id: str, name: str, age: int,
                 membership_type: str, specialty: str, annual_fees: float,
                 scholarship_name: str, amount: float, sponsor: str):
        super().__init__(student_id, name, age, membership_type,
                         specialty, annual_fees)
        self.scholarship_name = scholarship_name  # str
        self.amount           = amount            # float
        self.sponsor          = sponsor           # str
        self.renewed          = False             # bool

    def check_renewal(self) -> str:
        """Renew the scholarship if average >= 12."""
        if self.calculate_average() >= 12.0:
            self.renewed = True
            return ok(f"Scholarship \"{self.scholarship_name}\" renewed!")
        self.renewed = False
        return clr(f"  ✘  Scholarship \"{self.scholarship_name}\" NOT renewed (avg < 12).", C.RED)

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Scholarship: {self.scholarship_name} ({self.sponsor})"


# ─────────────────────────────────────────────────────────────
#  DISPLAY — student cards and lists
# ─────────────────────────────────────────────────────────────

def preview_student(student: Student, final: bool = False):
    """Display the complete student card."""
    label = "STUDENT RECORD" if final else "PREVIEW — PLEASE REVIEW BEFORE SAVING"
    title(label)

    section("Personal Information")
    rows = [
        ("Name",       student.name),
        ("ID",         student.person_id),
        ("Age",        student.age),
        ("Program",    student.specialty),
        ("Membership", (student.membership_type or "none").title()),
    ]
    if isinstance(student, ScholarshipStudent):
        rows += [
            ("Scholarship", student.scholarship_name),
            ("Amount",      f"{student.amount:,.0f} FCFA/year"),
            ("Sponsor",     student.sponsor),
        ]
    for k, v in rows:
        print(f"  {C.DIM}{k:<14}{C.RESET}  {C.WHITE}{v}{C.RESET}")

    section("Grades")
    if student.grades:
        print(f"  {C.DIM}{'Subject':<30} {'Grade':>6}  Letter{C.RESET}")
        print(f"  {'─'*44}")
        for subj, gr in student.grades.items():
            letter = Student.grade_to_letter(gr)
            color  = C.GREEN if gr >= 14 else (C.YELLOW if gr >= 10 else C.RED)
            print(f"  {subj:<30} {clr(f'{gr:>5.2f}/20', color)}  [{letter}]")
        print(f"  {'─'*44}")
        avg    = student.calculate_average()
        acolor = C.GREEN if avg >= 14 else (C.YELLOW if avg >= 10 else C.RED)
        print(f"  {'AVERAGE':<30} {clr(f'{avg:>5.2f}/20', acolor)}")
    else:
        warn("No grades recorded yet.")

    section("Academic Status")
    adm = clr("YES ✔", C.GREEN) if student.is_admitted()    else clr("NO ✘", C.RED)
    brs = clr("YES ✔", C.GREEN) if student.has_scholarship() else clr("NO ✘", C.RED)
    print(f"  Admitted              : {adm}")
    print(f"  Scholarship eligible  : {brs}")
    if isinstance(student, ScholarshipStudent):
        print("  " + student.check_renewal())

    section("Financial Summary")
    mt         = str(student.membership_type or "").strip().lower()
    member_pct = 10 if mt and mt != "none" else 0
    print(f"  Base fees             : {C.WHITE}{student.annual_fees:>12,.0f} FCFA{C.RESET}")
    print(f"  Membership discount   :      {member_pct}%   "
          f"({student.annual_fees * member_pct / 100:>10,.0f} FCFA)")
    print(f"  Total discount        : {C.GREEN}{student.discount_amount:>12,.0f} FCFA{C.RESET}")
    print(f"  {C.BOLD}Net fees              : {C.CYAN}{student.net_fees:>12,.0f} FCFA{C.RESET}")
    print(f"\n{'═'*60}\n")


def list_students(students: list):
    """Print a ranked list of all students."""
    if not students:
        warn("No students registered yet.")
        return
    title("ALL STUDENTS")
    for i, s in enumerate(sorted(students, reverse=True), 1):
        avg    = s.calculate_average()
        badge  = Student.grade_to_letter(avg)
        acolor = C.GREEN if avg >= 14 else (C.YELLOW if avg >= 10 else C.RED)
        tag    = clr(" [SCHOLARSHIP]", C.CYAN) if isinstance(s, ScholarshipStudent) else ""
        print(f"  {C.DIM}{i:>2}.{C.RESET} {C.WHITE}{s.name:<24}{C.RESET}"
              f"  {clr(f'{avg:.2f}/20', acolor)}  [{badge}]"
              f"  {s.specialty}{tag}")
    print()


# ─────────────────────────────────────────────────────────────
#  REGISTRATION FORM (step-by-step with back navigation)
# ─────────────────────────────────────────────────────────────

def register_student() -> "Student | None":
    """
    Step-by-step registration form.
    Type 0 at any step to go back to the previous one.
    Shows a preview before saving, with option to edit.
    """
    title("REGISTER A NEW STUDENT")

    MEMBERSHIP_OPTIONS = [
        ("None",             "none"),
        ("Student Club",     "club"),
        ("Library",          "library"),
        ("Other",            "other"),
    ]
    STUDENT_TYPE = [
        ("Regular Student",      "regular"),
        ("Scholarship Student",  "scholarship"),
    ]

    # Collected data — all None until entered by the user
    data = {
        "student_id":  None,
        "name":        None,
        "age":         None,
        "membership":  None,
        "specialty":   None,
        "annual_fees": None,
        "stype":       None,
        # scholarship fields
        "s_name":   None,
        "s_amount": None,
        "s_sponsor": None,
        # grades
        "grades":   None,
    }

    steps = [
        "student_id", "name", "age", "membership",
        "specialty", "annual_fees", "stype",
    ]
    i = 0  # current step index

    while i < len(steps):
        step = steps[i]
        print()

        # ── Step: student_id ─────────────────────────────────
        if step == "student_id":
            print(f"  {C.DIM}Step 1/7{C.RESET}  — Student ID")
            val = get_string("Student ID      : ", current=data["student_id"],
                             allow_back=(i > 0))
            if val is None: i -= 1; continue
            data["student_id"] = val

        # ── Step: name ───────────────────────────────────────
        elif step == "name":
            print(f"  {C.DIM}Step 2/7{C.RESET}  — Full Name")
            val = get_string("Full name       : ", current=data["name"], allow_back=True)
            if val is None: i -= 1; continue
            data["name"] = val

        # ── Step: age ────────────────────────────────────────
        elif step == "age":
            print(f"  {C.DIM}Step 3/7{C.RESET}  — Age")
            val = get_integer("Age (15–80)     : ", 15, 80,
                              current=data["age"], allow_back=True)
            if val is None: i -= 1; continue
            if not Person.validate_age(val):
                warn("Unusual age, but continuing.")
            data["age"] = val

        # ── Step: membership ─────────────────────────────────
        elif step == "membership":
            print(f"  {C.DIM}Step 4/7{C.RESET}  — Membership Type")
            val = get_choice("Your choice     : ", MEMBERSHIP_OPTIONS, allow_back=True)
            if val is None: i -= 1; continue
            if val == "other":
                val = get_string("Specify type    : ")
            data["membership"] = val

        # ── Step: specialty ──────────────────────────────────
        elif step == "specialty":
            print(f"  {C.DIM}Step 5/7{C.RESET}  — Program / Specialty")
            val = get_string("Program         : ", current=data["specialty"], allow_back=True)
            if val is None: i -= 1; continue
            data["specialty"] = val

        # ── Step: annual_fees ────────────────────────────────
        elif step == "annual_fees":
            print(f"  {C.DIM}Step 6/7{C.RESET}  — Annual Fees")
            val = get_float_val("Fees (FCFA)     : ", 0, 5_000_000,
                                current=data["annual_fees"],
                                default=500_000, allow_back=True)
            if val is None: i -= 1; continue
            data["annual_fees"] = val

        # ── Step: student type ───────────────────────────────
        elif step == "stype":
            print(f"  {C.DIM}Step 7/7{C.RESET}  — Student Type")
            val = get_choice("Your choice     : ", STUDENT_TYPE, allow_back=True)
            if val is None: i -= 1; continue
            data["stype"] = val
            # Add scholarship steps if needed
            if val == "scholarship" and "s_name" not in steps:
                steps += ["s_name", "s_amount", "s_sponsor"]

        # ── Scholarship step: name ───────────────────────────
        elif step == "s_name":
            print(f"  {C.DIM}Scholarship 1/3{C.RESET}  — Scholarship Name")
            val = get_string("Scholarship name: ", current=data["s_name"], allow_back=True)
            if val is None: i -= 1; continue
            data["s_name"] = val

        # ── Scholarship step: amount ─────────────────────────
        elif step == "s_amount":
            print(f"  {C.DIM}Scholarship 2/3{C.RESET}  — Annual Amount")
            val = get_float_val("Amount (FCFA)   : ", 0, 10_000_000,
                                current=data["s_amount"],
                                default=300_000, allow_back=True)
            if val is None: i -= 1; continue
            data["s_amount"] = val

        # ── Scholarship step: sponsor ────────────────────────
        elif step == "s_sponsor":
            print(f"  {C.DIM}Scholarship 3/3{C.RESET}  — Sponsor")
            val = get_string("Sponsor         : ", current=data["s_sponsor"], allow_back=True)
            if val is None: i -= 1; continue
            data["s_sponsor"] = val

        i += 1

    # ── Grade entry ──────────────────────────────────────────
    grades   = data["grades"] or {}
    section("GRADE ENTRY")
    n        = get_integer("How many subjects? (1–10): ", 1, 10)
    j        = 0
    subjects = list(grades.keys())

    while j < n:
        print(f"\n  {C.DIM}Subject {j+1}/{n}{C.RESET}")
        if j > 0:
            hint("go back to previous subject: type 0")

        default_subj = subjects[j] if j < len(subjects) else None
        subj = get_string(f"Subject {j+1} name : ",
                          current=default_subj, allow_back=(j > 0))
        if subj is None:
            if subjects:
                del grades[subjects[j-1]]
                subjects.pop()
            j -= 1
            continue

        current_grade = grades.get(subj, None)
        grade = get_float_val(f"Grade {j+1} (0–20): ", 0, 20,
                              current=current_grade, allow_back=(j > 0))
        if grade is None:
            if subjects:
                del grades[subjects[j-1]]
                subjects.pop()
            j -= 1
            continue

        grades[subj] = grade
        if j < len(subjects):
            subjects[j] = subj
        else:
            subjects.append(subj)
        j += 1

    data["grades"] = grades

    # ── Build the student object ─────────────────────────────
    if data["stype"] == "scholarship":
        student = ScholarshipStudent(
            data["student_id"], data["name"], data["age"],
            data["membership"], data["specialty"], data["annual_fees"],
            data["s_name"], data["s_amount"], data["s_sponsor"],
        )
    else:
        student = Student(
            data["student_id"], data["name"], data["age"],
            data["membership"], data["specialty"], data["annual_fees"],
        )

    for subj, grade in data["grades"].items():
        student.add_grade(subj, grade)

    # ── Preview before confirming ────────────────────────────
    while True:
        preview_student(student)
        print(f"  {C.CYAN}1{C.RESET}. ✅  Save")
        print(f"  {C.CYAN}2{C.RESET}. ✏️   Edit a field")
        print(f"  {C.CYAN}3{C.RESET}. ❌  Cancel (do not save)")
        choice = input(f"{C.BOLD}  Your choice: {C.RESET}").strip()

        if choice == "1":
            print(ok(f"{student.name} saved successfully!"))
            return student
        elif choice == "2":
            student = edit_student(student)
        elif choice == "3":
            warn("Registration cancelled.")
            return None
        else:
            err("Please enter 1, 2 or 3.")


# ─────────────────────────────────────────────────────────────
#  EDIT AN EXISTING STUDENT
# ─────────────────────────────────────────────────────────────

def edit_student(student: Student) -> Student:
    """Edit menu — every field can be changed."""
    FIELDS = [
        ("Name",            "name"),
        ("Age",             "age"),
        ("Membership",      "membership"),
        ("Program",         "specialty"),
        ("Annual Fees",     "annual_fees"),
        ("Grades",          "grades"),
    ]
    if isinstance(student, ScholarshipStudent):
        FIELDS += [
            ("Scholarship Name",   "s_name"),
            ("Scholarship Amount", "s_amount"),
            ("Sponsor",            "s_sponsor"),
        ]

    while True:
        section("EDIT STUDENT")
        options = list(FIELDS) + [("← Back", "__back__")]

        for i, (label, _) in enumerate(options, 1):
            print(f"  {C.CYAN}{i}{C.RESET}. {label}")

        raw = input(f"{C.BOLD}  Field to edit: {C.RESET}").strip()
        try:
            idx = int(raw) - 1
            if not (0 <= idx < len(options)):
                raise ValueError
        except ValueError:
            err("Invalid choice."); continue

        _, key = options[idx]
        if key == "__back__":
            break

        if key == "name":
            student.name = get_string("New name        : ", current=student.name)

        elif key == "age":
            student.age = get_integer("New age         : ", 15, 80, current=student.age)

        elif key == "membership":
            OPTS = [("None","none"), ("Student Club","club"),
                    ("Library","library"), ("Other","other")]
            v = get_choice("New type        : ", OPTS)
            if v == "other":
                v = get_string("Specify         : ")
            student.membership_type = v

        elif key == "specialty":
            student.specialty = get_string("New program     : ", current=student.specialty)

        elif key == "annual_fees":
            student.annual_fees = get_float_val("New fees (FCFA) : ", 0, 5_000_000,
                                                current=student.annual_fees)

        elif key == "grades":
            edit_grades(student)

        elif key == "s_name" and isinstance(student, ScholarshipStudent):
            student.scholarship_name = get_string("Scholarship name: ",
                                                   current=student.scholarship_name)

        elif key == "s_amount" and isinstance(student, ScholarshipStudent):
            student.amount = get_float_val("Scholarship amt : ", 0, 10_000_000,
                                           current=student.amount)

        elif key == "s_sponsor" and isinstance(student, ScholarshipStudent):
            student.sponsor = get_string("Sponsor         : ", current=student.sponsor)

        print(ok("Change saved."))

    return student


def edit_grades(student: Student):
    """Add, edit or remove grades interactively."""
    while True:
        section("EDIT GRADES")
        subjects = list(student.grades.keys())
        if subjects:
            for i, (subj, gr) in enumerate(student.grades.items(), 1):
                letter = Student.grade_to_letter(gr)
                print(f"  {C.CYAN}{i}{C.RESET}. {subj:<28} {gr:.2f}/20  [{letter}]")
        else:
            print("  No grades recorded.")

        print(f"\n  {C.CYAN}a{C.RESET}. Add a subject")
        print(f"  {C.CYAN}d{C.RESET}. Delete a subject")
        print(f"  {C.CYAN}0{C.RESET}. ← Back")

        raw = input(f"{C.BOLD}  Choice: {C.RESET}").strip().lower()

        if raw == "0":
            break
        elif raw == "a":
            subj  = get_string("Subject name    : ")
            grade = get_float_val("Grade (0–20)    : ", 0, 20)
            student.add_grade(subj, grade)
            print(ok(f"\"{subj}\" added."))
        elif raw == "d":
            if not subjects:
                warn("No grades to delete.")
                continue
            idx = get_integer("Number to delete: ", 1, len(subjects))
            removed = subjects[idx - 1]
            del student.grades[removed]
            print(ok(f"\"{removed}\" deleted."))
        else:
            try:
                idx = int(raw)
                if 1 <= idx <= len(subjects):
                    subj  = subjects[idx - 1]
                    grade = get_float_val(
                        f"New grade for \"{subj}\": ",
                        0, 20, current=student.grades[subj])
                    student.grades[subj] = grade
                    print(ok("Grade updated."))
                else:
                    err("Invalid number.")
            except ValueError:
                err("Invalid choice.")


# ─────────────────────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────────────────────

def main():
    students: list = []

    print(f"\n{C.BOLD}{C.CYAN}")
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║     SMART STUDENT MANAGEMENT SYSTEM             ║")
    print("  ║     PRG1406 — Group Assignment 1                ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print(C.RESET)

    MENU = [
        ("Register a new student",     "1"),
        ("View all students",           "2"),
        ("View a student's record",     "3"),
        ("Edit an existing student",    "4"),
        ("Compare two students",        "5"),
        ("Global statistics",           "6"),
        ("Exit",                        "7"),
    ]

    while True:
        print(f"\n{C.BOLD}  ── MAIN MENU {'─'*44}{C.RESET}")
        for label, val in MENU:
            print(f"  {C.CYAN}{val}{C.RESET}  →  {label}")
        print()

        choice = input(f"{C.BOLD}  Your choice (1–7): {C.RESET}").strip()

        # ── 1. Register ──────────────────────────────────────
        if choice == "1":
            s = register_student()
            if s:
                students.append(s)

        # ── 2. List all ──────────────────────────────────────
        elif choice == "2":
            list_students(students)

        # ── 3. View record ───────────────────────────────────
        elif choice == "3":
            if not students:
                warn("No students registered yet.")
            else:
                list_students(students)
                idx = get_integer("Student number: ", 1, len(students))
                preview_student(sorted(students, reverse=True)[idx-1], final=True)

        # ── 4. Edit ──────────────────────────────────────────
        elif choice == "4":
            if not students:
                warn("No students registered yet.")
            else:
                list_students(students)
                idx    = get_integer("Student number: ", 1, len(students))
                target = sorted(students, reverse=True)[idx-1]
                target = edit_student(target)
                real_idx = students.index(target)
                students[real_idx] = target
                print(ok("Changes saved."))
                preview_student(target)

        # ── 5. Compare ───────────────────────────────────────
        elif choice == "5":
            if len(students) < 2:
                warn("You need at least 2 students to compare.")
            else:
                list_students(students)
                a = get_integer("First student  : ", 1, len(students))
                b = get_integer("Second student : ", 1, len(students))
                if a == b:
                    warn("Please choose two different students.")
                else:
                    s_list = sorted(students, reverse=True)
                    best   = s_list[a-1] + s_list[b-1]   # uses __add__
                    print(f"\n  🏆  {C.GREEN}{C.BOLD}Best performer: {best.name}"
                          f" (avg {best.calculate_average():.2f}/20){C.RESET}\n")

        # ── 6. Statistics ────────────────────────────────────
        elif choice == "6":
            title("GLOBAL STATISTICS")
            total    = len(students)
            admitted = sum(1 for s in students if s.is_admitted())
            scholars = sum(1 for s in students if s.has_scholarship())
            bursary  = sum(1 for s in students if isinstance(s, ScholarshipStudent))
            avgs     = [s.calculate_average() for s in students if s.grades]
            best_avg = max(avgs) if avgs else 0.0
            print(f"  Students registered   : {total}")
            print(f"  Students admitted     : {admitted}")
            print(f"  Scholarship eligible  : {scholars}")
            print(f"  External scholarship  : {bursary}")
            print(f"  Best average          : {best_avg:.2f}/20")
            print(f"  Admission threshold   : {Student.ADMISSION_THRESHOLD}/20")
            print(f"  Scholarship threshold : {Student.SCHOLARSHIP_THRESHOLD}/20")
            print(f"  Total Person counter  : {Person.get_total_persons()}")
            print()

        # ── 7. Exit ──────────────────────────────────────────
        elif choice == "7":
            print(f"\n  {C.CYAN}Thank you for using the Smart Student System.{C.RESET}")
            print(f"  {C.DIM}Goodbye!{C.RESET}\n")
            break

        else:
            err("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
