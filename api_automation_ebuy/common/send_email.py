# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

class SendEmail(object):

    @staticmethod
    def send_qq_file_mail(title, message, file_path, file_name):

        # 创建一个SMTP对象并连接smtp服务
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)

        # 登录SMTP服务器
        msg_from = '991627540@qq.com'
        passwd = 'bjnowvnkbtuvbcdb'

        msg_to = ['991627540@qq.com', '3023087535@qq.com']

        s.login(user=msg_from, password=passwd)

        # 构建邮件内容
        # 创建一个邮件，文本类型
        content = MIMEText(message, _charset='utf8')

        # 构造附件
        # part = MIMEApplication(open(file_path, 'rb').read(), _subtype=False)
        part = MIMEApplication(open(file_path, 'rb').read(),_charset='utf8')
        # 自定义文件名称
        part.add_header('content-disposition', 'attachment', filename=file_name)

        # part=MIMEText('TEST!!!')
        # part = MIMEApplication(open(file_path, 'rb').read(), _charset='utf8')
        # part.add_header('content-disposition', 'attachment', filename='test.xlsx')

        # 封装邮件添加邮件主题
        msg = MIMEMultipart()
        # msg = MIMEText(content, 'html', 'UTF-8')
        # 添加文本内容和附件
        msg.attach(content)
        msg.attach(part)

        # part = MIMEText('<html><h1>test!</h1></html>', 'html', 'utf-8')
        # msg.attach(part)

        # 邮件内容构成
        msg['Subject'] = Header(title, 'utf-8')
        msg['From'] = msg_from  # 可以修改成任意名称
        msg['To'] = ','.join(msg_to)

        # 发送邮件
        try:
            s.sendmail(from_addr=msg_from, to_addrs=msg_to, msg=msg.as_string())
            print("Send qq_email successfully")
        except Exception as e:
            print("Send qq_mail failed")
            raise e
        finally:
            s.quit()


if __name__ == '__main__':

    import os
    from api_automation_ebuy.common.constant import DATA_DIR

    mail_title = "这是测试邮件"
    mail_message = "这是测试邮件"

    SendEmail.send_qq_file_mail(
        title=mail_title,
        message=mail_message,
        file_path=os.path.join(DATA_DIR, 'api_automation_course.xlsx'),
        file_name='api_automation_course.xlsx')



