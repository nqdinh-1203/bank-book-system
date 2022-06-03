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
## [Kết nối đồ án với cơ sở dữ liệu PostgreSQL sau đó đưa lên AWS RDS]

<details><summary>Show</summary>
    
- Tải Postgres [(link)](https://www.postgresql.org/download/) và PgAdmin [(link)](https://www.pgadmin.org/download/pgadmin-4-windows/) (giao diện để thao tác trên Postgres) 
- Đăng nhập vào PgAdmin và tạo database
	- Tạo 1 Server Group mới (DEMO) rồi tạo 1 Server mới tại server group vừa tạo (DEMO_SERVER)
	- Tạo 1 database ở server vừa tạo
- Kết nối database với đồ án Django và chạy migrations
	- Cài đặt các package psycopg2 (cho phép Postgres giao tiếp với ứng dụng)
	- Ta sẽ tạo db trên AWS trước rồi mới kết nối với Django
- Tạo database trên AWS RDS
	- Tạo tài khoản AWS rồi tìm đến trang AWS RDS
	- [Đường dẫn đến AWS RDS)](https://us-west-2.console.aws.amazon.com/rds/home?region=us-west-2#)
	- Tạo database mới trên AWS RDS (các tham số khi tạo có thể xem thêm ở video tham khảo)
	- Sau khi tạo xong ta sẽ có được một **endpoint** ở mục Connectivity & Security
- Kết nối live AWS database trực tiếp với PgAdmin và Django
	- Tạo một database mới ở DEMO_SERVER (LIVE_DBS)
	- Ở mục Connection khi tạo, đặt Host name là endpoint của database vừa tạo trên AWS RDS
	- Sửa mục DATABASES ở file settings.py trong thư mục crm1
DATABASES = 
{'default': 
	{'ENGINE': 'django.db.backends.postgresql',
	'NAME': (tên database vừa tạo trên AWS),
	'USER': (tên user),
	'PASSWORD': (password),
	'HOST': (đường dẫn endpoint),
	'PORT':5432, #mặc định}
}
	- python manage.py migrate
<blockquote>

## Đường dẫn tới project trên Heroku
Link Heroku: https://theblues-crm1.herokuapp.com/ 
# Link demo
# Current status:
- Đã hoàn thành các tính năng cơ bản của sổ tiết kiệm
- Phần frontend vẫn còn gặp nhiều vấn đề nên vẫn đang được chỉnh sửa và sẽ được tiếp tục cập nhật
# Future works
