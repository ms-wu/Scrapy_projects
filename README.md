# Scrapy_projects
This project can get some datas on Jobbole.com or zhihu.com.

Jobbole.com part：
Such as title, create_date, author, content etc.
On settings file, you can select some methods to transmit the data.
1.save as a json file.
2.save a front image.
3.desposited in a database.(host:localhost, account:root, passwd: Null)
(this methods are in pipeline.py)

zhihu.com part:
you need add your email and password in the zhihu.py file's line 135 and line 136.
then you should create two MYSQL's table, the table's params is in the items.py(ZhihuQuestionItem function and ZhihuAnswerItem function).
