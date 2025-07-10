from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Cấu hình database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/mydb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Định nghĩa model đơn giản
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

    def __init__(self, content):
        self.content = content

@app.route('/')
def hello():
    # Tạo bảng nếu chưa tồn tại
    db.create_all()
    
    # Kiểm tra nếu chưa có message nào thì thêm "Hello, World!"
    if Message.query.count() == 0:
        db.session.add(Message("Hello, World!"))
        db.session.commit()
    
    # Lấy message đầu tiên
    message = Message.query.first()
    return message.content

if __name__ == '__main__':
    app.run(debug=True)
