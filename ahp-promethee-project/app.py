from flask import Flask, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
from flask_bcrypt import check_password_hash
import secrets
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import numpy as np


app = Flask(__name__,static_url_path='/static', static_folder='static')

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ahp'
app.secret_key = secrets.token_hex(16)


mysql = MySQL(app)


class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[])
    email = StringField("Email",validators=[])
    password = PasswordField("Password",validators=[])
    submit = SubmitField("Register")

    def validate_email(self,field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where email=%s",(field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")


class EditProfileForm(FlaskForm):
    name = StringField("Name", validators=[])

    submit = SubmitField("Edit")



class EditProfileForm1(FlaskForm):
    email = StringField("Email", validators=[Email()])

    submit = SubmitField("Edit")


    def validate_email(self, field):
        if field.data != self.email:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (field.data,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                raise ValidationError('Email Already Taken')
class EditPassword(FlaskForm):

    current_password = PasswordField("Current Password", validators=[DataRequired(message="Current Password is required")])
    new_password = PasswordField("New Password", validators=[DataRequired(message="New Password is required")])
    submit = SubmitField("Edit")




@app.route('/')
def index1():
    return render_template('index1.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data.encode('utf-8')

        hashed_password = bcrypt.hashpw(password,bcrypt.gensalt())

        # store data into database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(name,email,hashed_password))
        mysql.connection.commit()
        cursor.close()
        flash('You have been successfully registered!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data.encode('utf-8')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.hashpw(password, user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))

    return render_template('login.html',form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where id=%s",(user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('dashboard.html',user=user)

    return redirect(url_for('dashboard'))


@app.route('/liste')
def liste():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where id=%s",(user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('liste.html',user=user)
    return render_template('liste.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        print("email1")
        if user:
            print("email2")
            form = EditProfileForm(obj=user)
            form1 = EditProfileForm1(obj=user)

            if form.validate_on_submit():
                # Récupérer les données du formulaire
                name = form.name.data
                cursor.execute("UPDATE users SET name=%s WHERE id=%s", (name, user_id))
                mysql.connection.commit()
                cursor.close()
                flash('Your profile has been successfully updated!', 'success')
                return redirect(url_for('profile'))

            if form1.validate_on_submit():
                # Récupérer les données du formulaire
                email = form1.email.data

                cursor.execute("UPDATE users SET email=%s WHERE id=%s", (email, user_id))
                mysql.connection.commit()
                cursor.close()
                flash('Your profile has been successfully updated!', 'success')
                return redirect(url_for('profile'))



            return render_template('profile.html', user=user, form=form, form1=form1)  # Passez form2 au modèle

    flash('You need to login first to access your profile.', 'warning')
    return redirect(url_for('login'))


@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        if user:
            form = EditPassword(obj=user)


            if form.validate_on_submit():
                new_password = form.new_password.data.encode('utf-8')
                cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new_password, user_id))
                mysql.connection.commit()
                cursor.close()
                flash('Your password has been successfully updated!', 'success')
                return redirect(url_for('Change'))


            return render_template('Change.html', user=user, form=form)  # Passez form2 au modèle

    flash('You need to login first to access your profile.', 'warning')
    return redirect(url_for('login'))








@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('index1'))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_project', methods=['POST'])
def create_project():
    projectName = request.form['projectName']
    numCriteria = request.form['numCriteria']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO projects (name, num_criteria) VALUES (%s, %s)", (projectName, numCriteria))
    mysql.connection.commit()
    project_id = cursor.lastrowid
    cursor.close()
    return redirect(url_for('project_details',
                            project_id=project_id))


@app.route('/project/<int:project_id>')
def project_details(project_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT num_criteria FROM projects WHERE id = %s", (project_id,))
    project = cursor.fetchone()
    cursor.execute("SELECT * FROM criteria WHERE project_id = %s ORDER BY id", (project_id,))
    criteria = cursor.fetchall()
    cursor.close()
    return render_template('project_details.html',
                           project_id=project_id,
                           num_criteria=project[0],
                           criteria=criteria)


@app.route('/add_criteria/<int:project_id>', methods=['POST'])
def add_criteria(project_id):
    cursor = mysql.connection.cursor()
    num_criteria = request.form.get('numCriteria', type=int)
    for i in range(num_criteria):
        criterion_name = request.form.get(f'criterionName_{i}')
        num_sub_criteria = request.form.get(f'numSubCriteria_{i}', type=int)
        cursor.execute("INSERT INTO criteria (project_id, name, num_sub_criteria) VALUES (%s, %s, %s)", (project_id, criterion_name, num_sub_criteria))
        criterion_id = cursor.lastrowid

        for j in range(num_sub_criteria):
            sub_criterion_name = request.form.get(f'subCriterionName_{i}_{j}')
            cursor.execute("INSERT INTO sub_criteria (criterion_id, name) VALUES (%s, %s)", (criterion_id, sub_criterion_name))
    mysql.connection.commit()
    cursor.close()
    # Redirect to the project hierarchy route
    return redirect(url_for('project_hierarchy', project_id=project_id))


@app.route('/project_hierarchy/<int:project_id>')
def project_hierarchy(project_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name FROM projects WHERE id = %s", (project_id,))
    project = cursor.fetchone()
    cursor.execute("SELECT * FROM criteria WHERE project_id = %s", (project_id,))
    criteria = cursor.fetchall()
    hierarchy = []
    for criterion in criteria:
        cursor.execute("SELECT * FROM sub_criteria WHERE criterion_id = %s", (criterion[0],))
        sub_criteria = cursor.fetchall()
        hierarchy.append({'id': criterion[0], 'criterion': criterion[2], 'sub_criteria': [{'name': sub[2]} for sub in sub_criteria]})
    cursor.close()
    return render_template('project_hierarchy.html', project_name=project[0], hierarchy=hierarchy, project_id=project_id)




# @app.route('/pairwise/<int:criterion_id>', methods=['GET', 'POST'])
# def pairwise(criterion_id):
#     if request.method == 'GET':
#         cursor = mysql.connection.cursor()
#
#         cursor.execute("SELECT name FROM criteria WHERE project_id = 12")
#         criteria_names = cursor.fetchall()  # Récupérer les noms des critères
#         cursor.close()
#
#         # Maintenant vous pouvez utiliser les noms des critères pour effectuer d'autres opérations
#         # Par exemple, vous pouvez les passer à un modèle HTML pour les afficher
#
#         return render_template('pairwise_ratings.html', criteria_names=criteria_names)
#     elif request.method == 'POST':
#         # Traitement des données du formulaire
#         # Assurez-vous de spécifier le traitement approprié pour les données envoyées par le formulaire
#         return redirect(url_for('pairwise', criterion_id=criterion_id))





# @app.route('/submit_pairwise/<int:criterion_id>', methods=['POST'])
# def submit_pairwise(criterion_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM sub_criteria WHERE criterion_id = %s", (criterion_id,))
#     sub_criteria = cursor.fetchall()
#     for i in range(len(sub_criteria)):
#         for j in range(len(sub_criteria)):
#             if i < j:
#                 rating = request.form[f'pair_{i}_{j}']
#                 cursor.execute("INSERT INTO pairwise_comparisons (criterion_id, sub_criterion1_id, sub_criterion2_id, rating) VALUES (%s, %s, %s, %s)", (criterion_id, sub_criteria[i]['id'], sub_criteria[j]['id'], rating))
#     mysql.connection.commit()
#     cursor.close()
#     return redirect(url_for('pairwise', project_id=criterion_id))


# @app.route('/calculate_weights/<int:criterion_id>')
# def calculate_weights(criterion_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM sub_criteria WHERE criterion_id = %s", (criterion_id,))
#     sub_criteria = cursor.fetchall()
#     # Assume there are n sub-criteria
#     n = len(sub_criteria)
#     matrix = [[1 if i == j else None for j in range(n)] for i in range(n)]
#
#     # Fill matrix with ratings
#     for i in range(n):
#         for j in range(n):
#             if i < j:
#                 cursor.execute(
#                     "SELECT rating FROM pairwise_comparisons WHERE sub_criterion1_id = %s AND sub_criterion2_id = %s",
#                     (sub_criteria[i]['id'], sub_criteria[j]['id']))
#                 rating = cursor.fetchone()['rating']
#                 matrix[i][j] = float(rating)
#                 matrix[j][i] = 1 / float(rating)
#     cursor.close()
#
#     # Calculate weights using the eigenvector method
#     eigenvalues, eigenvectors = np.linalg.eig(np.array(matrix))
#     max_eigenvalue_index = np.argmax(eigenvalues)
#     weights = np.abs(eigenvectors[:, max_eigenvalue_index])
#     weights_normalized = weights / np.sum(weights)
#
#     # Return weights to some template or directly show them
#     return str(weights_normalized.tolist())


def calculate_weights(criteria_with_sub_criteria):
    weights = {}
    for item in criteria_with_sub_criteria:
        sub_criteria = item['sub_criteria']
        num_sub_criteria = len(sub_criteria)
        matrix = np.ones((num_sub_criteria, num_sub_criteria))

        # Fill the pairwise comparison matrix with values
        cursor = mysql.connection.cursor()
        for i in range(num_sub_criteria):
            for j in range(i + 1, num_sub_criteria):
                cursor.execute(
                    'SELECT value FROM comparisons WHERE criterion_id = %s AND sub_criterion_id1 = %s AND sub_criterion_id2 = %s',
                    (item['criterion'][0], sub_criteria[i][0], sub_criteria[j][0])
                )
                result = cursor.fetchone()
                if result:
                    value = result[0]
                    matrix[i, j] = value
                    matrix[j, i] = 1 / value

        # Calculate the weights using the eigenvector method
        eigvals, eigvecs = np.linalg.eig(matrix)
        max_index = np.argmax(eigvals)
        max_eigvec = np.abs(eigvecs[:, max_index]).astype(float)
        weights[item['criterion'][0]] = (max_eigvec / np.sum(max_eigvec)).tolist()

    return weights


@app.route('/pairwise/<int:project_id>', methods=['GET', 'POST'])
def pairwise_comparison(project_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = %s', (project_id,))
    project = cursor.fetchone()

    if request.method == 'POST':
        comparisons = request.form.to_dict(flat=False)

        # Insert comparisons into the database
        for key, values in comparisons.items():
            if 'comparisons' in key:
                criterion_id, sub_criterion_id1, sub_criterion_id2 = key.split('[')[1:]
                criterion_id = criterion_id.replace(']', '')
                sub_criterion_id1 = sub_criterion_id1.replace(']', '')
                sub_criterion_id2 = sub_criterion_id2.replace(']', '')
                value_str = values[0]

                # Convert string value to float
                if '/' in value_str:
                    numerator, denominator = map(int, value_str.split('/'))
                    value = numerator / denominator
                else:
                    value = float(value_str)

                cursor.execute(
                    'INSERT INTO comparisons (criterion_id, sub_criterion_id1, sub_criterion_id2, value) VALUES (%s, %s, %s, %s)',
                    (criterion_id, sub_criterion_id1, sub_criterion_id2, value)
                )

        mysql.connection.commit()

        # Fetch the criteria and their sub-criteria for the project
        cursor.execute('SELECT * FROM criteria WHERE project_id = %s', (project_id,))
        criteria = cursor.fetchall()

        criteria_with_sub_criteria = []
        for criterion in criteria:
            cursor.execute('SELECT * FROM sub_criteria WHERE criterion_id = %s', (criterion[0],))
            sub_criteria = cursor.fetchall()
            criteria_with_sub_criteria.append({
                'criterion': criterion,
                'sub_criteria': sub_criteria
            })

        # Calculate weights for each criterion's sub-criteria
        weights = calculate_weights(criteria_with_sub_criteria)

        # Insert weights into the database
        for item in criteria_with_sub_criteria:
            criterion_id = item['criterion'][0]
            sub_criteria = item['sub_criteria']
            weights_vector = weights[criterion_id]

            for sub_criterion, weight in zip(sub_criteria, weights_vector):
                cursor.execute(
                    'INSERT INTO weights (criterion_id, sub_criterion_id, weight) VALUES (%s, %s, %s)',
                    (criterion_id, sub_criterion[0], weight)
                )

        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('enter_alternatives', project_id=project_id))

    # Fetch the criteria and their sub-criteria for the project
    cursor.execute('SELECT * FROM criteria WHERE project_id = %s', (project_id,))
    criteria = cursor.fetchall()

    criteria_with_sub_criteria = []
    for criterion in criteria:
        cursor.execute('SELECT * FROM sub_criteria WHERE criterion_id = %s', (criterion[0],))
        sub_criteria = cursor.fetchall()
        criteria_with_sub_criteria.append({
            'criterion': criterion,
            'sub_criteria': sub_criteria
        })

    return render_template('pairwise_comparison.html', project_name=project[1], project_id=project_id,
                           criteria_with_sub_criteria=criteria_with_sub_criteria, enumerate=enumerate)


@app.route('/enter_alternatives/<int:project_id>', methods=['GET', 'POST'])
def enter_alternatives(project_id):
    if request.method == 'POST':
        alternative_names = request.form.getlist('alternative_names')

        cursor = mysql.connection.cursor()
        for name in alternative_names:
            cursor.execute(
                'INSERT INTO alternatives (project_id, name) VALUES (%s, %s)',
                (project_id, name)
            )
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('enter_values', project_id=project_id))

    return render_template('enter_alternatives.html', project_id=project_id)


@app.route('/enter_values/<int:project_id>', methods=['GET', 'POST'])
def enter_values(project_id):
    cursor = mysql.connection.cursor()

    # Fetch alternatives for the project
    cursor.execute('SELECT id, name FROM alternatives WHERE project_id = %s', (project_id,))
    alternatives = cursor.fetchall()

    # Fetch sub-criteria and their weights for the project
    cursor.execute('''
        SELECT sc.id, sc.name, w.weight
        FROM sub_criteria sc
        JOIN weights w ON sc.id = w.sub_criterion_id
        JOIN criteria c ON sc.criterion_id = c.id
        WHERE c.project_id = %s
    ''', (project_id,))
    sub_criteria_weights = cursor.fetchall()

    if request.method == 'POST':
        values = request.form.to_dict(flat=False)

        for alternative in alternatives:
            alternative_id = alternative[0]
            for sub_criterion in sub_criteria_weights:
                sub_criterion_id = sub_criterion[0]
                value = float(values[f'value_{alternative_id}_{sub_criterion_id}'][0])
                cursor.execute(
                    'INSERT INTO alternative_values (project_id, alternative_id, sub_criterion_id, value) VALUES (%s, %s, %s, %s)',
                    (project_id, alternative_id, sub_criterion_id, value)
                )

        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('promethee_analysis', project_id=project_id))

    cursor.close()
    return render_template('enter_values.html', project_id=project_id, alternatives=alternatives,
                           sub_criteria_weights=sub_criteria_weights)


@app.route('/promethee_analysis/<int:project_id>')
def promethee_analysis(project_id):
    cursor = mysql.connection.cursor()

    # Fetch alternatives
    cursor.execute('SELECT id, name FROM alternatives WHERE project_id = %s', (project_id,))
    alternatives = cursor.fetchall()

    # Fetch sub-criteria and their weights
    cursor.execute('''
        SELECT sc.id, sc.name, w.weight
        FROM sub_criteria sc
        JOIN weights w ON sc.id = w.sub_criterion_id
        JOIN criteria c ON sc.criterion_id = c.id
        WHERE c.project_id = %s
    ''', (project_id,))
    sub_criteria_weights = cursor.fetchall()

    # Fetch alternative values
    cursor.execute('''
        SELECT alternative_id, sub_criterion_id, value
        FROM alternative_values
        WHERE project_id = %s
    ''', (project_id,))
    alternative_values = cursor.fetchall()

    # Reshape the alternative values into a matrix
    alt_values_matrix = {}
    for alt_id, sub_crit_id, value in alternative_values:
        if alt_id not in alt_values_matrix:
            alt_values_matrix[alt_id] = {}
        alt_values_matrix[alt_id][sub_crit_id] = value

    alternatives_list = [alt[0] for alt in alternatives]
    sub_criteria_list = [sc[0] for sc in sub_criteria_weights]
    weights_list = [sc[2] for sc in sub_criteria_weights]

    matrix = np.array([[alt_values_matrix[alt_id][sc_id] for sc_id in sub_criteria_list] for alt_id in alternatives_list])

    # Calculate preference functions and flow scores
    def preference_function(difference):
        return max(0, difference)

    def calculate_preference_indices(matrix, weights):
        num_alternatives = matrix.shape[0]
        num_criteria = matrix.shape[1]
        preference_matrix = np.zeros((num_alternatives, num_alternatives))

        for i in range(num_alternatives):
            for j in range(num_alternatives):
                if i != j:
                    for k in range(num_criteria):
                        preference_matrix[i][j] += weights[k] * preference_function(matrix[i][k] - matrix[j][k])

        return preference_matrix

    def calculate_flow_scores(preference_matrix):
        positive_flow = np.sum(preference_matrix, axis=1)
        negative_flow = np.sum(preference_matrix, axis=0)
        net_flow = positive_flow - negative_flow
        return positive_flow, negative_flow, net_flow

    preference_matrix = calculate_preference_indices(matrix, weights_list)
    positive_flow, negative_flow, net_flow = calculate_flow_scores(preference_matrix)

    ranking = np.argsort(net_flow)[::-1]
    ranked_alternatives = [(alternatives[i][1], net_flow[i]) for i in ranking]

    cursor.close()
    return render_template('promethee_analysis.html', ranked_alternatives=[(rank, alternatives[i][1]) for rank, i in enumerate(ranking, 1)], enumerate=enumerate)


@app.route('/success')
def success():
    return "Pairwise comparisons and weights saved successfully!"

@app.route('/add_alternatives/<int:project_id>', methods=['POST'])
def add_alternatives(project_id):
    numAlternatives = int(request.form['numAlternatives'])
    cursor = mysql.connection.cursor()
    for i in range(numAlternatives):
        alternativeName = request.form[f'alternative{i}']
        cursor.execute("INSERT INTO alternatives (project_id, name) VALUES (%s, %s)", (project_id, alternativeName))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('project_details', project_id=project_id))



if __name__ == '__main__':
    app.run(debug=True)

