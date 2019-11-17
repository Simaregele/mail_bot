import imaplib
import email
import email.message
import bs4
bsoup = bs4.BeautifulSoup
import config

# логика элементов td mother_class > table_class > main_class > table > tr > 2-d td

mother_class = "e4fcf49d339e49e54d8e4094ff5b6c35content-cell"
table_class = "e87955b57e36bb84a36d9833e3cb5c27attributes"
main_class = "172dd1c6341983508c65d5aa419917f8attributes_content"
element_class = "7c3f8f7bc09d253c9189b3ec2e244faeattributes_item"


def find_all(soup):
    element = soup.find('table')
    td_tr = element.tbody.tr.td.text
    print(td_tr)

    # for element in soup.find_all('td', class_=element_class):
    #     print(element.text)


# Ссылки
# https://yandex.ru/support/mail/mail-clients.html  - инфа яндекса
# https://eax.me/python-imap/ -  статья про почту
# Видос хороший https://www.youtube.com/watch?v=bbPwv0TP2UQ
# Второй видос https://www.youtube.com/watch?v=Jt8LizzxkPU
# https://www.youtube.com/watch?v=ng2o98k983k  про BS

#подкоючаемся к серверу почты и логинимся
mail = imaplib.IMAP4_SSL('imap.yandex.ru')
mail.login(config.login, config.password)


#берем то что у нас в папке, в данном случае выбираю папку Quiz
mail.select('Quiz')

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
            # print(subject_)
            # print(content_type)
            if "plain" in content_type:
                # print(part.get_payload())
                pass
            elif "html" in content_type:
                html_ = part.get_payload()
                soup = bsoup(html_, "html.parser")
                # text = soup.get_text()
                # print(soup.prettify())
                # print(subject_)
                find_all(soup)

            else:
                # print(content_type)
                pass



    # email_message.get_payload()