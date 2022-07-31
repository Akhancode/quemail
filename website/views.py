from django.shortcuts import render
from django.core.mail import send_mail,EmailMessage,send_mass_mail
import pandas as pd
entered_name = None;
entered_email=None;
entered_password=None;
entered_subject=None;
entered_dear=None;
entered_message=None;
entered_ending=None;
alert = None
dataTuple = ()
def printx():
    print('x')
def home(request):
    return render(request,'home.html',{'name':'Amjadkhan'})

def One_bulk(request):
    global entered_name,entered_email,entered_password,entered_subject,entered_dear,entered_message,entered_ending,dataTuple,alert
    var_choosed= request.POST.get('email', None)
    # on press submit
    if request.method == "POST":
        print("One bulk on passing Post form")
        print(entered_name,entered_password,entered_message)
        print(dataTuple)
        if entered_email and entered_password:
            content = "%s\n\n%s\n\n%s" % (entered_dear, entered_message, entered_ending)
            try:
                # send_mail(entered_subject, content, entered_email, ["akhan.crpt@gmail.com"], fail_silently=False,
                #           auth_user=entered_email, auth_password=entered_password)
                send_mass_mail(dataTuple,fail_silently=False,auth_user=entered_email,auth_password=entered_password)
                print("Done Mail send")
                return render(request, 'One_bulk.html', {
                    'email': entered_email,
                    'type': 'One_bulk',
                    'alert': "All mail send Successfully!!"
                })
            except Exception as e:
                if str(e) == "[Errno 11001] getaddrinfo failed":
                    print("connect to Internet")
                    return render(request, 'One_bulk.html', {
                        'email': entered_email,
                        'type': 'One_bulk',
                        'alert': "No Internet Connection"
                    })
                elif (str(e).find('Username and Password not accepted') != -1):
                    print("please check entered EMail and Password")
                    return render(request, 'One_bulk.html', {
                        'email': entered_email,
                        'type': 'One_bulk',
                        'alert': "please check entered EMail and Password"
                    })
                else:
                    print(e)

        else:
            print("*** SORRY Please Enter required details before submiting ***")
            print("entered_name" ,entered_name)
            return render(request, 'One_bulk.html', {
                "alert": "Make sure Excel uploaded and fill the entire form !!!"


            })


    else:
        entered_name = None;
        entered_email = None;
        entered_password = None;
        entered_subject = None;
        entered_dear = None;
        entered_message = None;
        entered_ending = None;
        alert = None;
        dataTuple = ()
        print("rendering one_bulk without posting main form (refresh)")
        print(entered_name)
        print("datatuple",dataTuple)
        return render(request, 'One_bulk.html', {
            'type': 'One_bulk',
        })
    # return  HttpResponse("Hello World")
def automate(request):

    # on press submit
    if request.method == "POST":
        entered_email = request.POST.get('email',None)
        entered_password = request.POST.get('password_entered',None)
        entered_name = request.POST.get('Entered_Name',None)
        entered_subject = request.POST.get('subject_msg',None)
        entered_dear = request.POST.get('dear_msg',None)
        entered_message = request.POST.get('message',None)
        entered_ending = request.POST.get('ending',None)



        # if entered_email and entered_password:
        #     # smtp library server connection
        #     server = smtplib.SMTP("smtp.gmail.com", 587)
        #     server.starttls()
        #     server.login("%s" % entered_email, "%s" % entered_password)
        #     msg=None
        #     msg = EmailMessage()
        #     msg['Subject'] = '%s' % entered_subject
        #     msg['From'] = entered_email
        #     msg['To'] = "akhan.crpt@gmail.com"
        #     msg.set_content("%s,\n\n%s\n\n%s" %(entered_dear,entered_message,entered_ending))
        #
        #     server.send_message(msg)

        if entered_email and entered_password and entered_message:
            content = "%s\n\n%s\n\n%s" %(entered_dear,entered_message,entered_ending)
            try:
                send_mail(entered_subject,content,entered_email,["akhan.crpt@gmail.com"],fail_silently=False,auth_user=entered_email,auth_password=entered_password)
                print("Done Mail send")
            except Exception as e:
                if str(e)=="[Errno 11001] getaddrinfo failed":
                    print("connect to Internet")
                elif (str(e).find('Username and Password not accepted') != -1):
                    print("please check entered EMail and Password")
                else:
                    print("8888888888888888888")
                    print(e)
        else:
            print("*** SORRY Please Enter required details before submiting ***")



        return render(request,'Automate.html',{
            'msg':entered_message,
            'name':entered_name,
            'email':entered_email,
            'type':'Single'
        })


    else:
        return render(request,'Automate.html',{'type':'Single'})
def variable_count(request):
    vari = request.POST.get('variable', None)
    print(vari)
    return render(request, 'One_bulk.html', {
        'type': 'One_bulk',
        'var_x':vari
    })
def Excel_Process(request):
    global entered_name,entered_email,entered_password,entered_subject,entered_dear,entered_message,entered_ending,dataTuple,alert
    dataTuple=()
    try:
        if request.method == "POST":
            entered_email = request.POST.get('email', None)
            entered_password = request.POST.get('password_entered', None)
            entered_name = request.POST.get('Entered_Name', None)
            entered_subject = request.POST.get('subject_msg', None)
            entered_dear = request.POST.get('dear_msg', None)
            entered_message = request.POST.get('message', None)
            entered_ending = request.POST.get('ending', None)


            print("this is excel function on pass Post in form")

            file = request.FILES["Myfile"]
            print(file)
            data = pd.read_excel(file)
            emails=[]

            columns = len(data.columns)
            column_names = list(data.columns)


            if columns == 2 : # Two variable
                str_match = list(filter(lambda x: 'EMAI' in x, column_names))
                email_col = str_match[0]
                column_names.remove(email_col)
                emails = data['%s' % (email_col)].values
                var_1 = data['%s' % (column_names[0])].values
                var_count = 1

                for v1, email in zip(var_1, emails):
                    t = (entered_subject,
                         "%s\n\n%s\n\n%s" % (entered_dear, entered_message.replace('%variable_1', str(v1)), entered_ending),
                         entered_email, [email])
                    dt = list(dataTuple)
                    dt.append(t)
                    dataTuple = tuple(dt)

                print("datatuple", dataTuple)
                mylist = zip(var_1, emails)
                return render(request, 'One_bulk.html', {
                    'entered_name': entered_name,
                    'entered_email': entered_email,
                    'entered_password': entered_password,
                    'entered_subject': entered_subject,
                    'entered_dear': entered_dear,
                    'entered_message': entered_message,
                    'entered_ending': entered_ending,
                    'type': 'One_bulk',
                    'excel_name': 'Excels',
                    "emails": emails,
                    "mylist": mylist,
                    "file_name": file,
                    'var_1_column': column_names[0],
                    "variable_1": var_1,
                    "var_count": var_count

                })
<<<<<<< HEAD
            elif columns == 1 : # Two variable
=======
            elif columns == 1 : # One variable
>>>>>>> origin/main
                print("enterto def function")
                str_match = list(filter(lambda x: 'EMAI'or'email'or'Email' in x, column_names))
                email_col = str_match[0]
                column_names.remove(email_col)
                emails = data['%s' % (email_col)].values
                var_count = 0

                for email in zip(emails):
                    t = (entered_subject,
                         "%s\n\n%s\n\n%s" % (entered_dear, entered_message, entered_ending),
                         entered_email, [email])
                    dt = list(dataTuple)
                    dt.append(t)
                    dataTuple = tuple(dt)

                print("datatuple", dataTuple)
                mylist = zip(emails)
                return render(request, 'One_bulk.html', {
                    'entered_name': entered_name,
                    'entered_email': entered_email,
                    'entered_password': entered_password,
                    'entered_subject': entered_subject,
                    'entered_dear': entered_dear,
                    'entered_message': entered_message,
                    'entered_ending': entered_ending,
                    'type': 'One_bulk',
                    'excel_name': 'Excels',
                    "emails": emails,
                    "mylist": mylist,
                    "file_name": file,
                    "var_count": var_count

                })


            elif columns == 3:
                str_match = list(filter(lambda x: 'EMAI' in x, column_names))
                email_col = str_match[0]
                print(column_names)
                column_names.remove(email_col)
                print(column_names)
                emails = data['%s'%(email_col)].values
                var_1 = data['%s' %(column_names[0])].values
                var_2 = data['%s' %(column_names[1])].values
                var_count = 2
                for v1,v2,email in zip(var_1,var_2, emails):
                    t = (entered_subject,
                         "%s\n\n%s\n\n%s" % (entered_dear, entered_message.replace('$var_1', str(v1)).replace('$var_2', str(v2)), entered_ending),
                         entered_email, [email])
                    dt = list(dataTuple)
                    dt.append(t)
                    dataTuple = tuple(dt)

                print("datatuple", dataTuple)

                mylist = zip(var_1,var_2, emails)
           
                return render(request, 'One_bulk.html', {
                    'entered_name': entered_name,
                    'entered_email': entered_email,
                    'entered_password': entered_password,
                    'entered_subject': entered_subject,
                    'entered_dear': entered_dear,
                    'entered_message': entered_message,
                    'entered_ending': entered_ending,
                    'type': 'One_bulk',
                    'excel_name': 'Excels',
                    "emails": emails,
                    "mylist": mylist,
                    "file_name": file,
                    'var_1_column': column_names[0],
                    'var_2_column': column_names[1],
                    "variable_1": var_1,
                    "variable_2": var_2,
                    "var_count": var_count

                })
            elif columns == 4:
                str_match = list(filter(lambda x: 'EMAI'or'Email'or'email' in x, column_names))
                email_col = str_match[0]
                print(column_names)
                column_names.remove(email_col)
                print(column_names)
                emails = data['%s'%(email_col)].values
                var_1 = data['%s' %(column_names[0])].values
                var_2 = data['%s' %(column_names[1])].values
                var_3 = data['%s' %(column_names[2])].values
                var_count = 3
                for v1,v2,v3,email in zip(var_1,var_2,var_3, emails):
                    t = (entered_subject,
                         "%s\n\n%s\n\n%s" % (entered_dear, entered_message.replace('$var_1', str(v1)).replace('$var_2', str(v2)).replace('$var_3', str(v3)), entered_ending),
                         entered_email, [email])
                    dt = list(dataTuple)
                    dt.append(t)
                    dataTuple = tuple(dt)

                print("datatuple", dataTuple)

                mylist = zip(var_1,var_2,var_3, emails)
            #
                return render(request, 'One_bulk.html', {
                    'entered_name': entered_name,
                    'entered_email': entered_email,
                    'entered_password': entered_password,
                    'entered_subject': entered_subject,
                    'entered_dear': entered_dear,
                    'entered_message': entered_message,
                    'entered_ending': entered_ending,
                    'type': 'One_bulk',
                    'excel_name': 'Excels',
                    "emails": emails,
                    "mylist": mylist,
                    "file_name": file,
                    'var_1_column': column_names[0],
                    'var_2_column': column_names[1],
                    'var_3_column': column_names[2],
                    "variable_1": var_1,
                    "variable_2": var_2,
                    "var_count": var_count

                })
            else:
                str_match = list(filter(lambda x: 'EMAI'or'Email'or'email' in x, column_names))
                email_col = str_match[0]
                print(column_names)
                column_names.remove(email_col)
                print(column_names)
                emails = data['%s'%(email_col)].values
                var_1 = data['%s' %(column_names[0])].values
                var_2 = data['%s' %(column_names[1])].values
                var_3 = data['%s' %(column_names[2])].values
                var_count = 3
                for v1,v2,v3,email in zip(var_1,var_2,var_3, emails):
                    t = (entered_subject,
                         "%s\n\n%s\n\n%s" % (entered_dear, entered_message.replace('$var_1', str(v1)).replace('$var_2', str(v2)).replace('$var_3', str(v3)), entered_ending),
                         entered_email, [email])
                    dt = list(dataTuple)
                    dt.append(t)
                    dataTuple = tuple(dt)

                print("datatuple", dataTuple)

                mylist = zip(var_1,var_2,var_3, emails)
            #
                return render(request, 'One_bulk.html', {
                    'entered_name': entered_name,
                    'entered_email': entered_email,
                    'entered_password': entered_password,
                    'entered_subject': entered_subject,
                    'entered_dear': entered_dear,
                    'entered_message': entered_message,
                    'entered_ending': entered_ending,
                    'type': 'One_bulk',
                    'excel_name': 'Excels',
                    "emails": emails,
                    "mylist": mylist,
                    "file_name": file,
                    'var_1_column': column_names[0],
                    'var_2_column': column_names[1],
                    'var_3_column': column_names[2],
                    "variable_1": var_1,
                    "variable_2": var_2,
                    "var_count": var_count

                })

        else:
            print("excel process without pass form")
            return render(request, 'One_bulk.html', {
                'name': "ajish",
                'type': 'One_bulk',
                'excel_name': 'Excel',
                'alert':'😁',

            })
    except Exception as e:
        if str(e) == "'Myfile'":
            return render(request, 'One_bulk.html', {
                'alert':"Upload the Excel file ! "
            })
        elif str(e) == "list index out of range":
            return render(request, 'One_bulk.html', {
                'alert':"Upload in the Instructed Format ! "
            })
        elif (str(e).find('Excel file format cannot be determined') != -1):
            print("please Upload Excel file !!")
            return render(request, 'One_bulk.html', {
                'email': entered_email,
                'type': 'One_bulk',
                'alert': "Please Upload Excel File !!"
            })
        else:
            print("0000000000000000")
            print(str(e) + "this is the errorllllllllllllllllllllllllllllllllllllll")
            return render(request, 'One_bulk.html', {
                'email': entered_email,
                'type': 'One_bulk',
                'alert': str(e)
            })

# def multiple_upload(request):
#     if request.method == "POST":
#         file = request.FILES["Myfile"]
#         print(file)
#         data = pd.read_excel(file)
#         emails = data['EMAILS'].values
#         company = data['COMPANY'].values
#         position = data['POSITION'].values
#
#         print(emails)
#         print(company)
#         print(position)
#         # csv = pd.read_csv(file)
#         # print(csv.head())
#         # arr = csv["sum"]
#         # sum = sum(arr)
#         return render(request,'multiple_fileupload.html',{
#             "some":True,
#             "emails":emails,
#             "company":company
#         })
#
#     return render(request,'multiple_fileupload.html',{
#         'name':'Amjadkhan',
#         'type': 'One_bulk',
#         'excel_name':'Excel result'
#     })

def multiple_upload_save(request):
    images = request.FILES.getlist("files[]")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(images)

