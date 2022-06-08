# Introduction to Software Engineering - HCMUS - 19_22

# Group 10 
**Các thành viên**

- 19120534: Phạm Đức Huy (leader)
- 19120478: Nguyễn Quang Định 
- 19120494: Huỳnh Quốc Duy
- 19120562: Lê Thành Lộc
- 19120602: Hồ Hữu Ngọc

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

**Playlist hướng dẫn về Django của youtuber DennisIvy:** https://www.youtube.com/playlist?list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO <br>
**Simple Banking System in Django with Source Code - CodeAstro**
https://codeastro.com/simple-banking-system-in-python-django-with-source-code/ 
https://www.youtube.com/watch?v=s-T0MbXjz34 <br>

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
## Kết nối đồ án với cơ sở dữ liệu PostgreSQL sau đó đưa lên AWS RDS

<details><summary>Click to expand</summary>
    
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
</details>

## Lưu các tệp (hình ảnh, html, css) ở AWS S3 Buckets thay vì lưu ở local
<details><summary>Click to expand</summary>

- Tạo bucket mới ở AWS S3 [link](https://s3.console.aws.amazon.com/s3/home?region=us-west-2)
- Cách config bucket mới có thể xem ở video sau: [File Storage with AWS S3 Buckets Upload](https://www.youtube.com/watch?v=inQyZ7zFMHM&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=22)
- Khi đã tạo thành công thì ta sẽ có được một Access key ID và Secret access key sau đó thêm các tham số vào file settings.py như trong video
- Cài đặt thư viện boto3 ( hỗ trợ người dùng Python liên kết ứng dụng với các dịch vụ của AWS
- Thêm 'storages' vào mục INSTALLED_APPS trong settings.py
- Upload các thư mục như images hay css trong /crm1/static vào S3 Bucket
- Lúc này khi muốn cập nhật các file ở local đến AWS thì ta chạy dòng lệnh python manage.py collectstatic 
- Lưu ý rằng khi kết nối từ local lên AWS thì các dữ liệu cũ sẽ đều bị reset nên ta sẽ phải chạy lệnh python manage.py createsuperuser để tạo superuser mới.
<blockquote>
</details>

## Deploy lên Heroku Server

<details><summary>Click to expand</summary>
 
- Đăng nhập vào Heroku và tạo 1 app mới
- Cài đặt và khởi động Heroku CLI [(link)](https://devcenter.heroku.com/articles/heroku-cli)
- *heroku login* để đăng nhập vào tài khoản heroku của bạn
-  Điều hướng về thư mục chứa ứng dụng sau đó chạy các lệnh sau trên CLI
	- git init
	- heroku git:remote -a (tên app vừa tạo) 
- Cài đặt thêm các package gunicorn và whitenoise
- Trên command prompt, điều hướng về thư mục chứa ứng dụng, sau đó chạy lệnh ''pip freeze > requirements.txt để tạo một tập tin chứa các package mà ứng dụng Django sử dụng
- Sửa các nội dung trong ứng dụng Django
	- Thêm file runtime.txt với nội dung là phiên bản Python đang sử dụng
	- Thêm tập tin Procfile với nội dung là 'web: gunicorn crm1.wsgi --log-file -'
	- Thêm domain của app vừa tạo vào ALLOWED_HOST trong settings.py đồng thời đặt biến DEBUG=False. (Lưu ý nếu gặp lỗi thì ta có thể thử nhiều domain của app như 'theblues-crm1.com', 'www.theblues-crm1.com', 'theblues-crm1.herokuapp.com' với tên ứng dụng là theblues-crm1) 
	- Package whitenoise mà ta cài đặt ở trên sẽ giúp Heroku liên kết với các static file của ứng dụng. Thêm dòng 'whitenoise.middleware.WhiteNoiseMiddleware,' vào danh sách MiddleWare trong settings.py
- Tiếp theo vào trang của ứng dụng vào tạo trong Heroku:
	- Cài đặt buildpack là Python
	- Ở phần deploy đặt Deployment method là Heroku Git
- Lúc này khi đã hoàn tất điều chỉnh các tham số, ta vào lại Heroku CLI:
	- git add . để thêm các thư mục và tập tin của ứng dụng Django vào git
	- git commit -am "first commit"
	- git push heroku master 
	- Lúc này ta đã push toàn bộ nội dung của ứng dụng lên Heroku, chạy câu lệnh *heroku run python manage.py migrate* để thực hiện kết nối 

<blockquote>
</details>

## Cuối cùng kết nối Heroku với Postgres 
<details><summary>Click to expand</summary>

- Vào mục Resources của Heroku, thêm Add-ons là Heroku Postgres
- Cài đặt thư viện dj-database-url 
	- Chạy lại lệnh git freeze > requirements.txt
	- Thêm dòng code sau vào settings.py:
	- import  dj_database_url 
	- df_from_env = dj_database_url.config(conn_max_age=60)
	- DATABASES['default'].update(df_from_env)
- Trong mục Settings của Heroku, thêm nội dung sau vào Config Vars:
	- postgres://USERNAME:PASSWORD@database url endpoint:PORT/DB NAME
		- USERNAME và PASSWORD là tên đăng nhập vào database trong PostgreSQL
		- databse url endpoint là đường dẫn endpoint đến database trong AWS RDS
		- Port thường là 5432
		- DB Name là tên của database
	- Lưu ý, để liên kết với database trong AWS thì ta cần điều chỉnh mục Inbound Rules của database (xem [video](https://www.youtube.com/watch?v=TFFtDLZnbSs&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=25) từ phút 9:40)
<blockquote>
</details>

## Đường dẫn tới project trên Heroku
Link Heroku: https://theblues-crm1.herokuapp.com/ 
### Để cập nhật code ở local đến project đã deploy lên Heroku ta thực hiện các bước sau:
- heroku git:clone -a theblues-crm1
- cd theblues-crm1
- git add .
- git commit -am "make it better"
- git push heroku master
# Link demo
# Current status:
- Đã hoàn thành các tính năng cơ bản của sổ tiết kiệm
- Phần frontend vẫn còn gặp nhiều vấn đề nên vẫn đang được chỉnh sửa và sẽ được tiếp tục cập nhật
# Future works
