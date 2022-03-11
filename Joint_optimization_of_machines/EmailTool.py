# smtplib 用于邮件的发信动作
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header


def sendEmail(subject,context):
    # 用于构建邮件头

    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = 'yours addr'
    password = 'your pwd'

    # 收信方邮箱
    # to_addr = ['1198984639@qq.com','1577263944@qq.com']
    to_addr = 'addr'
    QQEmail(from_addr,to_addr,subject,context,password)


def QQEmail(from_addr,to_addr,subject,context,password=None,):
    '''
        :param from_addr:Email sender address
        :param to_addr:receiver(s), it may be a string or list
        :param subject:title of your mail
        :param context:main body of your mail
        :param password: the password of sender ,it is neccesery in qq email
        '''

    if isinstance (to_addr,str):
        tostr = to_addr
    elif isinstance (to_addr,list):
        tostr = to_addr[0]
        if len(to_addr)>1:
            for i in to_addr[1:]:
                tostr+=(';'+i)
    else:
        raise Exception("目标地址参数错误")
        # 发信服务器
  #   smtp_server = 'smtp.qq.com'

    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(context, 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(tostr)
    msg['Subject'] = Header(subject)

    smtp_server = 'smtp.qq.com'
    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL()
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
# sendEmail('test','cool')