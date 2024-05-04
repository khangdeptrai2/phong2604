from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Kết nối đến cơ sở dữ liệu MySQL
connection = mysql.connector.connect(user='root', password='', host='localhost', database='quan_li_nhan_vien')
cursor = connection.cursor()

# Route để hiển thị trang chính
@app.route('/')
def index():
    return render_template('index.html')


# Route để thêm nhân viên
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        # Nhận dữ liệu từ biểu mẫu
        name = request.form['name']
        age = int(request.form['age'])
        job = request.form['job']
        salary = int(request.form['salary'])
        # Thêm nhân viên vào cơ sở dữ liệu
        add_employee_query = "INSERT INTO nhanvien (name, age, job, salary) VALUES (%s, %s, %s, %s)"
        cursor.execute(add_employee_query, (name, age, job, salary))
        connection.commit()
        return "Nhân viên đã được thêm thành công."
    return render_template('add_employee.html')

# Route để xóa nhân viên
@app.route('/delete_employee', methods=['GET', 'POST'])
def delete_employee():
    if request.method == 'POST':
        id_employee_delete = int(request.form['id'])
        # Xóa nhân viên từ cơ sở dữ liệu
        delete_query = "DELETE FROM nhanvien WHERE id = %s"
        cursor.execute(delete_query, (id_employee_delete,))
        connection.commit()
        return f"Nhân viên có ID {id_employee_delete} đã được xóa."
    return render_template('delete_employee.html')

# Route để cập nhật thông tin nhân viên
@app.route('/update_employee', methods=['GET', 'POST'])
def update_employee():
    if request.method == 'POST':
        employee_id = int(request.form['id'])
        new_name = request.form['name']
        new_age = int(request.form['age'])
        new_job = request.form['job']
        new_salary = int(request.form['salary'])
        # Cập nhật thông tin nhân viên trong cơ sở dữ liệu
        update_query = "UPDATE nhanvien SET name = %s, age = %s, job = %s, salary = %s WHERE id = %s"
        cursor.execute(update_query, (new_name, new_age, new_job, new_salary, employee_id))
        connection.commit()
        return f"Thông tin của nhân viên có ID {employee_id} đã được cập nhật."
    return render_template('update_employee.html')

# Route để in thông tin nhân viên
@app.route('/print_employee')
def print_employee():
    # Truy vấn cơ sở dữ liệu để lấy thông tin của tất cả nhân viên
    code = "SELECT * FROM nhanvien"
    cursor.execute(code)
    employees = cursor.fetchall()
    return render_template('print_employee.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
