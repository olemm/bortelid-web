No questions — this is clear. Below is the full consolidated LLM spec with the custom forms section integrated and consistent Markdown formatting using **text**.

LLM SPEC — py4web (Tables, Forms, File Uploads, Custom Forms)

1. Objective
Generate idiomatic py4web code using:
    • pyDAL (DAL, Field)
    • Form from py4web.utils.form
    • Built-in file uploads via Field(..., "upload")
Follow this architecture:
Field → Table → Form → Controller → Template → Rendering

2. Core Principles
Rule 1 — Table-first design
Always define database tables before forms or logic.
db.define_table(...)

Rule 2 — Fields define behavior
All validation, defaults, and behavior MUST be defined in Field(...).
Field("name", requires=IS_NOT_EMPTY(), default="N/A")

Rule 3 — Forms are auto-generated
Use:
Form(db.table)

Rule 4 — Uploads are fields
Use:
Field("file", "upload")

Rule 5 — Keep controllers thin
Controllers should:
    • instantiate form
    • check .accepted
    • redirect or return data

Rule 6 — Templates render only
Templates must:
    • render form
    • loop through rows
    • use URL(...)

3. Data Model (DAL)
3.1 Minimal table
db.define_table(
    "entity",
    Field("name"),
    Field("description", "text"),
    format="%(name)s"
)

3.2 Validation
Field("name", requires=IS_NOT_EMPTY())
Field("type", requires=IS_IN_SET(["A", "B"]))

3.3 Constraints
Field("email", unique=True, notnull=True)
Type
Purpose
requires
form validation
notnull / unique
database enforcement

3.4 References
Field("company_id", "reference company")

4. Forms
4.1 Create
form = Form(db.table)

4.2 Update
form = Form(db.table, record_id)

4.3 Submission
if form.accepted:
    redirect(URL("target"))

4.4 Rules
    • do NOT manually insert if using Form
    • do NOT mix request.forms
    • use form.vars

4.5 Widgets
from py4web.utils.form import FormStyleDefault, RadioWidget
FormStyleDefault.widgets["field"] = RadioWidget()

4.6 Custom Forms (Non-Table Forms)
Used when the form is not tied to a single table.

Basic pattern
fields = [
    Field("name", "string", label="name-id", requires=IS_NOT_EMPTY()),
    Field("child", "string", label="ChildID", requires=IS_NOT_EMPTY()),
    Field("master_type", "string", label="Master Type", requires=IS_IN_SET(["pe", "co", "gr"])),
    Field("child_type", "string", label="Child Type", requires=IS_IN_SET(["pe", "co", "gr"]))
]

form = Form(fields, formstyle=FormStyleDefault, dbio=False)

Rule 1 — Use dbio=False
Form(fields, dbio=False)
Disables automatic DB insert/update.

Rule 2 — Use form.vars
if form.accepted:
    value = form.vars["name"]

Rule 3 — Manual processing required
if form.accepted:
    data = form.vars
    # custom logic here

Rule 4 — When to use
If one table → Form(db.table)
If workflow/custom → Form(fields, dbio=False)

Rule 5 — Validation in Field
Field("type", requires=IS_IN_SET([...]))

Rule 6 — Clear naming
Field("child_uuid", label="Child UUID")

Rule 7 — Supports formstyle/widgets
Form(fields, formstyle=FormStyleDefault)

4.7 Custom Form Example
@action("relate", method=["GET", "POST"])
@action.uses("relate.html", db)
def relate():

    fields = [
        Field("name", requires=IS_NOT_EMPTY()),
        Field("child", requires=IS_NOT_EMPTY()),
        Field("master_type", requires=IS_IN_SET(["pe", "co", "gr"])),
        Field("child_type", requires=IS_IN_SET(["pe", "co", "gr"]))
    ]

    form = Form(fields, formstyle=FormStyleDefault, dbio=False)

    if form.accepted:
        data = form.vars
        # process relation

    return dict(form=form)

5. File Uploads
5.1 Basic
Field(
    "image",
    "upload",
    download_url=lambda name: URL("download", name)
)

5.2 Storage
DB: filename
Filesystem: file

5.3 Custom folder
Field("file", "upload", uploadfolder=settings.UPLOAD_FOLDER)

5.4 Store in DB
Field("file_data", "blob"),
Field("file", "upload", uploadfield="file_data")

5.5 Render
<img src="[[=URL('download', row.image)]]">

5.6 Programmatic
field.store(stream, filename)

6. Controller Pattern
@action("endpoint", method=["GET", "POST"])
@action.uses("template.html", db)
def endpoint():

    form = Form(db.table)

    if form.accepted:
        redirect(URL("endpoint"))

    rows = db(db.table).select()

    return dict(form=form, rows=rows)

7. Template Pattern
[[=form]]

[[for row in rows:]]
    <div>
        [[=row.name]]

        [[if row.file:]]
            <img src="[[=URL('download', row.file)]]">
        [[pass]]

    </div>
[[pass]]

8. End-to-End Example
Model
db.define_table(
    "card",
    Field("description", "text"),
    Field("date", "date"),
    Field("logo", "upload", download_url=lambda name: URL("download", name))
)

Controller
@action("cards", method=["GET", "POST"])
@action.uses("cards.html", db)
def cards():

    form = Form(db.card)

    if form.accepted:
        redirect(URL("cards"))

    rows = db(db.card).select()

    return dict(form=form, rows=rows)

Template
[[=form]]

[[for row in rows:]]
    <div>
        [[=row.description]]

        [[if row.logo:]]
            <img src="[[=URL('download', row.logo)]]">
        [[pass]]

    </div>
[[pass]]

9. Anti-Patterns
Do NOT
db.table.insert(...)
when using Form

Do NOT
request.forms

Do NOT
    • put business logic in controller
    • bypass upload field
    • use widget= in Field

10. Mental Model
Field → Table → Form → Controller → Template
For custom forms:
Fields → Form(dbio=False) → form.vars → manual logic

11. Output Requirements
Always generate:
    • imports
    • db.define_table
    • Form(...)
    • controller
    • template
    • upload handling (if needed)

12. Summary
py4web is:
Database-driven
Table defines structure
Form handles input
Upload is a field
Controller orchestrates
Template renders

