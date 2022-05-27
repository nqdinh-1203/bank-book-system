# Introduction to Software Engineering - HCMUS - 19_22

# Group 10 
**Các thành viên**

- 19120534: Phạm Đức Huy (leader)
- 19120478: Nguyễn Quang Định 
- 19120494: Huỳnh Quốc Duy
- 19120562: Lê Thành Lộc
- 1912062: Hồ Hữu Ngọc

# Giới thiệu project
**Tên đề tài: Quản lý sổ tiết kiệm**

Một số tính năng chính:
- Mở sổ tiết kiệm
- Lập phiếu gửi tiền
- Lập phiếu rút tiền
- Tra cứu sổ
- Lập báo cáo ngày/tháng
- Thay đổi một số quy định, ràng buộc

# Các project được tham khảo

**Simple Banking System in Django with Source Code - CodeAstro**
https://codeastro.com/simple-banking-system-in-python-django-with-source-code/ 
https://www.youtube.com/watch?v=s-T0MbXjz34

**Phần front end** được vẽ ở trang https://www.figma.com/ từ đó dùng 1 số công cụ để chuyển sang html và css

# Môi trường thực thi
- Phiên bản hệ điều hành: Windows 11
- SDK: Python Django, Javascript
- Dev Tools: Visual Studio Code
- Cơ sở dữ liệu: PostgreSQL, AWS RDS, AWS S3
# Hướng dẫn cấu hình project chạy local PC
- Chạy command prompt và điều hướng đến thư mục chạy project
- Cài đặt requirements: pip install -r requirements.txt
- Thực hiện di chuyển cơ sở dữ liệu: python manage.py makemigrations
- python manage.py migrate
- Chạy ứng dụng: python manage.py runserver
# Hướng dẫn deploy project lên Heroku
Link Heroku: https://theblues-crm1.herokuapp.com/ 
# Link demo
# Current status:
- Đã hoàn thành các tính năng cơ bản của sổ tiết kiệm
- Phần frontend vẫn còn gặp nhiều vấn đề nên vẫn đang được chỉnh sửa và sẽ được tiếp tục cập nhật
# Future works
