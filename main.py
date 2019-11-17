import imaplib
import email
import email.message
import bs4
bsoup = bs4.BeautifulSoup
import config


# Ссылки
# https://yandex.ru/support/mail/mail-clients.html  - инфа яндекса
# https://eax.me/python-imap/ -  статья про почту
# Видос хороший https://www.youtube.com/watch?v=bbPwv0TP2UQ
# Второй видос https://www.youtube.com/watch?v=Jt8LizzxkPU

#подкоючаемся к серверу почты и логинимся
mail = imaplib.IMAP4_SSL('imap.yandex.ru')
mail.login(config.login, config.password)


#берем то что у нас в ящике
mail.select('INBOX')

# это выподит письма в инбоксе
# mail.list()

# возвращает тапл из двух элеметво и вот мы их раскидали, в data хряанится не лист а стрнг
result, data = mail.uid('search', None, "ALL")

# раскидываем стринг на лист, точнее лист состоящий из 1-го стринга. так как к первому и единтсвненому элементу мы
# и обрашаемся
inbox_item_list = data[0].split()
# last = inbox_item_list[-1]
# result2, email_data = mail.uid('fetch', last, '(RFC822)')
# raw_mail = email_data[0][1].decode("utf-8")
# email_message = email.message_from_string(raw_mail)
# from_ = email_message["From"]
# print(from_)
mar = '"Marquiz Robot" <robot@marquiz.ru>'


for item in inbox_item_list:
    # вот оно нащше письмецо
    result2, email_data = mail.uid('fetch', item, '(RFC822)')
    # этот элмент потому что именно он тот что нам нужен
    raw_mail = email_data[0][1].decode("utf-8")
    # Превращаем в объект email библиотеки, это нужно чтобы дальше удобно воркать
    email_message = email.message_from_string(raw_mail)
    # От кого письмо
    to_ = email_message["To"]
    from_ = email_message["From"]
    subject_ = email_message["Subject"]
    counter = 1
    if from_ == mar:
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            filename = part.get_filename()
            if not filename:
                ext = 'html'
                filename = 'msg-part-%08d%s' %(counter, ext)
            counter += 1
            # save file
            content_type = part.get_content_type()
            print(subject_)
            print(content_type)
            if "plain" in content_type:
                # print(part.get_payload())
                pass
            elif "html" in content_type:
                html_ = part.get_payload()
                soup = bsoup(html_, "html.parser")
                text = soup.get_text()
                print(text)
                print(subject_)

            else:
                # print(content_type)
                pass



    # email_message.get_payload()