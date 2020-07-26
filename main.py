from flask import Flask, request, render_template, redirect, Blueprint, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ishaan kamra'
app.config['UPLOAD_FOLDER'] = "C:\\Users\\ISHAAN KAMRA\\PycharmProjects\\scientificatt\\static"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

dashboard = Blueprint('login', __name__, url_prefix='/dashboard')  # admin   branch-head   employee
branch = Blueprint('branch', __name__, url_prefix='/branches')  # admin
department = Blueprint('department', __name__, url_prefix='/departments')  # admin
employee = Blueprint('employee', __name__, url_prefix='/employee')  # admin   branch-head
new_employee = Blueprint('new_employee', __name__, url_prefix='/new')


class Employees(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(80))
    branch = db.Column(db.String(30), nullable=False)
    department = db.Column(db.String(30), nullable=False)
    designation = db.Column(db.String(30), nullable=False)


class Branches(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    head = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(60), nullable=False)


class Departments(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(30), nullable=True)

class Projects(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    employee = db.Column(db.String(65000), nullable=False)
    branch = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    report = db.Column(db.String(65000), nullable=True)


class New(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone_no = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)


@login_manager.user_loader
def load_user(employee_id):
    return Employees.query.get(employee_id)


# DEBUG REMEMBER ME
@app.route('/', methods=['GET', 'POST'])
def login():
    # Take care of security while logging in
    # set session variable for email
    # fetch designation from  employees table to direct to correct dashboard
    # flash error msg for wrong credentials
    # flash error msg if user is registered but not assigned
    if current_user.is_authenticated:
        if current_user.designation == 'Founder':
            return redirect('/dashboard/admin/')
        elif current_user.designation == 'Branch Head':
            return redirect('/dashboard/branch_head/')
        else:
            return redirect('/dashboard/employee/')
    elif request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('pass')
        remember_me = request.form.get('remember_me')
        employee = Employees.query.filter_by(email=username).first()
        if employee:
            if check_password_hash(employee.password, password):
                login_user(employee, remember=remember_me)
                flash('Logged in successfully.')
                if employee.designation == 'Founder':
                    return redirect('/dashboard/admin/')
                elif employee.designation == 'Branch Head':
                    return redirect('/dashboard/branch_head/')
                else:
                    return redirect('/dashboard/employee/')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@dashboard.route('/admin/')
def admin_dashboard():
    # filter by all projects
    # show active projects first and then completed ones as well
    # add project option
    # open project on a new page after clicking on the project card and the page should have the options for assigning people edit and delete
    # edit page should display a table of currently assigned employees with an option to delete them
    # assign page should have a dropdown with a list of all the employees to select from them
    project1 = Projects.query.filter_by(status='ACTIVE').all()
    project2 = Projects.query.filter_by(status='COMPLETED').all()
    department = Departments.query.filter_by().all()
    return render_template('founder_module.html', project1=project1, project2=project2, user=current_user, department=department)


@dashboard.route('/branch_head/')
def branch_head_dashboard():
    # add project option
    # open project on a new page after clicking on the project card and the page should have the options for assigning people edit and delete
    # edit page should display a table of currently assigned employees with an option to delete them
    # assign page should have a dropdown with a list of all the employees to select from them
    # either create session variable of branch and use it to fetch projects of the branch to display to the branchhead
    # Or fetch branch from employee table using filter with sno = session['sno'] and then use branch of that employee i.e. employee.branch to filter projects
    project1 = Projects.query.filter((Projects.branch == current_user.branch) & (Projects.status == 'ACTIVE')).all()
    project2 = Projects.query.filter((Projects.branch == current_user.branch) & (Projects.status == 'COMPLETED')).all()
    department = Departments.query.filter_by().all()
    return render_template('branch_head_module.html', user=current_user, project1=project1, project2=project2, department=department)


@dashboard.route('/employee/')
def employee_dashboard():
    # filter projects using email of the respective person
    projects = Projects.query.filter_by().all()
    assignedprojects = []
    for project in projects:
        stremp = project.employee
        listemp = json.loads(stremp)

        for email in listemp:
            if email == current_user.email:
                assignedprojects.append(project)
    department = Departments.query.filter_by().all()
    return render_template('employee_module.html', project=assignedprojects, user=current_user, department=department)


@dashboard.route('/<string:sno>/')
def project_dashboard(sno):
    projects = Projects.query.filter_by(sno=sno).first()
    stremp = projects.employee
    listemp = json.loads(stremp)
    listempnames = []
    for i in listemp:
        name = Employees.query.filter_by(email=i).first().name
        listempnames.append(name)
    strrep = projects.report
    listrep = json.loads(strrep)
    if current_user.designation == 'Founder':
        employees = Employees.query.filter_by().all()
    else:
        employees = Employees.query.filter_by(branch=current_user.branch).all()
    return render_template('project.html', user=current_user, projects=projects, employees=employees, listemp=listemp, listempnames=listempnames, listrep=listrep)


@dashboard.route('/delete_employee/<string:sno>/<string:i>')
def project_delete_employee(sno, i):
    projects = Projects.query.filter_by(sno=sno).first()
    stremp = projects.employee
    listemp = json.loads(stremp)
    listempnames = []
    for email in listemp:
        name = Employees.query.filter_by(email=email).first().name
        listempnames.append(name)
    a = listempnames.index(i)
    del listemp[a]
    stremp = json.dumps(listemp)
    db.session.query(Projects).filter_by(sno=sno).update(dict(employee=stremp))
    db.session.commit()
    return redirect('/dashboard/' + sno + '/')


@dashboard.route('/delete_report/<string:sno>/<string:i>')
def project_delete_report(sno, i):
    projects = Projects.query.filter_by(sno=sno).first()
    strrep = projects.report
    listrep = json.loads(strrep)
    listrep.remove(i)
    strrep = json.dumps(listrep)
    db.session.query(Projects).filter_by(sno=sno).update(dict(report=strrep))
    db.session.commit()
    return redirect('/dashboard/' + sno + '/')



@dashboard.route('/add_employee/<string:sno>/', methods=['GET', 'POST'])
def add_employee(sno):
    if request.method == 'POST':
        add_employee = request.form.get('add_employee')
        employee = Employees.query.filter_by(name=add_employee).first()
        projects = Projects.query.filter_by(sno=sno).first()

        # string received
        stremp = projects.employee

        # convert string to list and then append
        listemp = json.loads(stremp)
        listemp.append(employee.email)

        # convert list back to string and store in db
        stremp = json.dumps(listemp)
        db.session.query(Projects).filter_by(sno=sno).update(dict(employee=stremp))
        db.session.commit()
    return redirect('/dashboard/' + sno + '/')


@dashboard.route('/add_report/<string:sno>/', methods=['GET', 'POST'])
def add_report(sno):
    if request.method == 'POST':
        report = request.form.get('report')
        projects = Projects.query.filter_by(sno=sno).first()

        # string received
        strrep = projects.report

        # convert string to list and then append
        listrep = json.loads(strrep)
        listrep.append(report)

        # convert list back to string and store in db
        strrep = json.dumps(listrep)
        db.session.query(Projects).filter_by(sno=sno).update(dict(report=strrep))
        db.session.commit()
    return redirect('/dashboard/' + sno + '/')


@dashboard.route('/edit/<string:sno>/', methods=['GET', 'POST'])
def project_edit(sno):
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        status = request.form.get('status')
        branch = request.form.get('branch')
        department = request.form.get('department')
        db.session.query(Projects).filter_by(sno=sno).update(dict(name=name,
                                                                 description=description,
                                                                 status=status,
                                                                 branch=branch,
                                                                 department=department))
        db.session.commit()
        return redirect('/dashboard/' + sno + '/')
    total_branches = Branches.query.filter_by().all()
    project = Projects.query.filter_by(sno=sno).first()
    total_departments = Departments.query.filter_by().all()
    total_status = ['ACTIVE', 'COMPLETED']
    if current_user.designation == 'Founder':
        total_employees = Employees.query.filter_by().all()
    else:
        total_employees = Employees.query.filter_by(branch=current_user.branch).all()

    return render_template('project_edit.html',
                           project=project,
                           total_branches=total_branches,
                           total_departments=total_departments,
                           total_status=total_status,
                           total_employees=total_employees,
                           user=current_user)


@dashboard.route('/delete/<string:sno>/', methods=['GET', 'POST'])
def project_delete(sno):
    project = Projects.query.filter_by(sno=sno).first()
    db.session.delete(project)
    db.session.commit()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register_employee():
    # check if the user is in session part to be activates once we complete dashboard login part and thus set the session variable
    # if user in session and session['user'] ==:
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        passw = request.form.get('password')
        password = generate_password_hash(passw, method='sha256')
        branch = request.form.get('branch')
        department = request.form.get('department')
        designation = request.form.get('designation')
        entry = Employees(name=name,
                          email=email,
                          phone=phone,
                          password=password,
                          branch=branch,
                          department=department,
                          designation=designation)
        db.session.add(entry)
        db.session.commit()
    # query department and branches from table
    total_branches = Branches.query.filter_by().all()
    total_departments = Departments.query.filter_by().all()

    if current_user.designation == "Founder":
        total_designations = [{'designation': 'Founder'}, {'designation': 'Branch Head'}, {'designation': 'Employee'}]

    elif current_user.designation == "Branch Head":
        total_designations = [{'designation': 'Employee'}]

    return render_template('register.html',
                           total_branches=total_branches,
                           total_departments=total_departments,
                           total_designations=total_designations, user=current_user)


@app.route('/register_login', methods=['GET', 'POST'])
def register_login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone_no')
        passw = request.form.get('pass')
        password = generate_password_hash(passw, method='sha256')
        branch = request.form.get('branch')
        entry = New(name=name,
                    email=email,
                    password=password,
                    phone_no=phone,
                    branch=branch)
        db.session.add(entry)
        db.session.commit()
        return render_template('login.html')
    else:
        total_branches = Branches.query.filter_by().all()
        return render_template('register_login.html', total_branches=total_branches)


@new_employee.route('/', methods=['GET', 'POST'])
def new():
    # display table of employees with department or branch as not assigned also need to make frontend template
    # name email branch department (designation) assign delete
    if current_user.designation == "Founder":
        employees = New.query.filter_by().all()
        total_branches = Branches.query.filter_by().all()

    elif current_user.designation == "Branch Head":
        employees = New.query.filter_by(branch=current_user.branch).all()
        total_branches = Branches.query.filter_by(name=current_user.branch).all()
    return render_template('new.html', employees=employees, user=current_user, total_branches=total_branches)


# test the following
@new_employee.route('/assign/<string:id>', methods=['GET', 'POST'])
def new_assign(id):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        department = request.form.get('department')
        designation = request.form.get('designation')

        delete_new_user = New.query.filter_by(id=id).first()
        password = delete_new_user.password

        if current_user.designation == "Founder":
            branch = request.form.get('branch')

        elif current_user.designation == "Branch Head":
            branch = delete_new_user.branch

        entry = Employees(name=name,
                          email=email,
                          phone=phone,
                          password=password,
                          branch=branch,
                          department=department,
                          designation=designation)

        db.session.add(entry)
        db.session.delete(delete_new_user)
        db.session.commit()
        return redirect('/new/')

    new = New.query.filter_by(id=id).first()
    total_branches = Branches.query.filter_by().all()
    total_departments = Departments.query.filter_by().all()

    if current_user.designation == "Founder":
        total_designations = [{'designation': 'Founder'}, {'designation': 'Branch Head'}, {'designation': 'Employee'}]

    elif current_user.designation == "Branch Head":
        total_designations = [{'designation': 'Employee'}]

    return render_template('new_assign.html', employee=new,
                           total_branches=total_branches,
                           total_departments=total_departments,
                           total_designations=total_designations, user=current_user)


@new_employee.route('/deny/<string:id>', methods=['GET', 'POST'])
def new_deny(id):
    new = New.query.filter_by(id=id).first()
    db.session.delete(new)
    db.session.commit()
    return redirect('/new')


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        name = request.form.get('name')
        image = " "
        entry = Departments(name=name,image=image)
        db.session.add(entry)
        db.session.commit()
    return redirect('/departments/')

@app.route('/uploader/<string:sno>', methods=['GET', 'POST'])
def upload_image(sno):
    if request.method == 'POST':
        f = request.files['fileupload']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        db.session.query(Departments).filter_by(sno=sno).update(dict(image=secure_filename(f.filename)))
        db.session.commit()
    return redirect('/departments/')


@app.route('/delete_department/<string:sno>', methods=['GET', 'POST'])
def delete_department(sno):
    entry = Departments.query.filter_by(sno=sno).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect('/departments/')


@app.route('/add', methods=['GET', 'POST'])
def add():
    # sno, name, department, employee, branch, date, status, description
    if request.method == 'POST':
        name = request.form.get('name')
        employee = request.form.get('employee')
        emp = Employees.query.filter_by(name=employee).first()
        listemp = [emp.email, ]
        stremp = json.dumps(listemp)
        description = request.form.get('description')
        status = request.form.get('status')
        branch = request.form.get('branch')
        department = request.form.get('department')
        date = datetime.now()
        entry = Projects(name=name,
                         employee=stremp,
                         description=description,
                         status=status,
                         branch=branch,
                         department=department,
                         date=date,
                         report="[]")
        db.session.add(entry)
        db.session.commit()
    # query department and branches from table
    total_branches = Branches.query.filter_by().all()
    total_departments = Departments.query.filter_by().all()
    total_status = ['ACTIVE', 'COMPLETED']
    if current_user.designation == 'Founder':
        total_employees = Employees.query.filter_by().all()
    else:
        total_employees = Employees.query.filter_by(branch=current_user.branch).all()

    return render_template('add.html',
                           total_branches=total_branches,
                           total_departments=total_departments,
                           total_status=total_status,
                           total_employees=total_employees,
                           user=current_user)


# test entire employee module
@employee.route('/admin/')
def employee_admin():
    employees = Employees.query.filter_by().all()
    return render_template('employee_admin.html', employees=employees, user=current_user)


@employee.route('/branch_head/')
def employee_branch_head():
    branch = current_user.branch
    employees = Employees.query.filter((Employees.branch == branch) & (Employees.designation == 'Employee')).all()
    return render_template('employee_branch_head.html', employees=employees, user=current_user)


@employee.route('/admin/edit/<string:id>', methods=['GET', 'POST'])
def employee_admin_edit(id):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        branch = request.form.get('branch')
        department = request.form.get('department')
        designation = request.form.get('designation')
        db.session.query(Employees).filter_by(id=id).update(dict(name=name,
                                                                 email=email,
                                                                 phone=phone,
                                                                 branch=branch,
                                                                 department=department,
                                                                 designation=designation))

        db.session.commit()
        return redirect('/employee/admin/')
    employees = Employees.query.filter_by(id=id).first()
    total_branches = Branches.query.filter_by().all()
    total_departments = Departments.query.filter_by().all()
    total_designations = [{'designation': 'Founder'}, {'designation': 'Branch Head'}, {'designation': 'Employee'}]
    return render_template('employee_admin_edit.html', employee=employees,
                           total_branches=total_branches,
                           total_departments=total_departments,
                           total_designations=total_designations, user=current_user)


@employee.route('/admin/delete/<string:id>', methods=['GET', 'POST'])
def employee_admin_delete(id):
    employee = Employees.query.filter_by(id=id).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect('/employee/admin')


@employee.route('/branch_head/edit/<string:id>', methods=['GET', 'POST'])
def employee_branch_head_edit(id):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        branch = request.form.get('branch')
        department = request.form.get('department')
        designation = request.form.get('designation')
        db.session.query(Employees).filter_by(id=id).update(dict(name=name,
                                                                 email=email,
                                                                 phone=phone,
                                                                 branch=branch,
                                                                 department=department,
                                                                 designation=designation))

        db.session.commit()
        return redirect('/employee/branch_head/')
    employees = Employees.query.filter_by(id=id).first()
    total_departments = Departments.query.filter_by().all()
    total_designations = [{'designation': 'Employee'}]
    return render_template('employee_branch_head_edit.html', employee=employees,
                           total_departments=total_departments,
                           total_designations=total_designations, user=current_user)


@employee.route('/branch_head/delete/<string:id>', methods=['GET', 'POST'])
def employee_branch_head_delete(id):
    employee = Employees.query.filter_by(id=id).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect('/employee/branch_head')


@branch.route('/')
def branches():
    # display branches table only to founder
    # Create edit add delete options with separate pages i.e. create frontend for edit  and add
    branches = Branches.query.filter_by().all()
    return render_template('branches.html', branches=branches, user=current_user)


@app.route('/add_branch/', methods=['GET', 'POST'])
def add_branchs():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        entry = Branches(name = name, head=" ", address = address)
        db.session.add(entry)
        db.session.commit()
    return render_template('add_branch.html', user=current_user)



@branch.route('/edit/<string:sno>', methods=['GET', 'POST'])
# value repeating in dropdown(delhi delhi)
# update queries (for designation) accordingly if
# 1. branch-head is changed
# 2. branch is deleted
def edit_branch(sno):
    if request.method == 'POST':
        name = request.form.get('name')
        head = request.form.get('head')
        address = request.form.get('address')
        db.session.query(Branches).filter_by(sno=sno).update(dict(name=name,
                                                                  head=head,
                                                                  address=address))

        db.session.commit()
        return redirect('/branches')
    branch = Branches.query.filter_by(sno=sno).first()
    total_heads = Employees.query.filter_by(branch=branch.name).all()
    return render_template('branch_edit.html', branch=branch, total_heads=total_heads, user=current_user)


@branch.route('/delete/<string:sno>', methods=['GET', 'POST'])
def branch_delete(sno):
    branch = Branches.query.filter_by(sno=sno).first()
    db.session.delete(branch)
    db.session.commit()
    return redirect('/branches')


@department.route('/')
def departments():
    # display departments table only to founder
    # Create add and delete
    # create add by toggle option or drop down or drop down form
    departments = Departments.query.filter_by().all()
    return render_template('department.html', departments=departments, user=current_user)

@app.route('/profile')
def profile():
    # use session variable to get email and display details accordingly
    # improve frontend
    # profile edit option
    return render_template('profile.html', user=current_user)


@app.route('/forgot_password')
def forgot_password():
    # think the approach as we have prob with smtp server while hosting so cant send emails
    pass

#complete the code(backend)
@app.route('/change_password', methods=['GET','POST'])
def change_password():
    if request.method == 'POST':
        p1 = request.form.get('new_password')
        p2 = request.form.get('retype_password')
        if p1 == p2:
            p = generate_password_hash(p1)
            db.session.query(Employees).filter_by(id=current_user.id).update(dict(password=p))
            db.session.commit()
            return redirect('/logout')
    return render_template('change_password.html', user=current_user)


app.register_blueprint(dashboard)
app.register_blueprint(branch)
app.register_blueprint(department)
app.register_blueprint(employee)
app.register_blueprint(new_employee)
app.run(debug=True)