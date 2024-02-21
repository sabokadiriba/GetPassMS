from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
from . import Emailbackend
def Login(request):
    return render(request,"login_form.html")
def doLogin(request):
    if request.method == "POST":
        user = Emailbackend.authenticate(request,
                                           username = request.POST.get('username'),
                                           password = request.POST.get('password'),)

        if user!=None:

            login(request,user)
            user_type= user.user_type
            if user_type =='1':
                return redirect('supervisor_home')
            elif user_type =='2':
                return redirect('employee_home')
            elif user_type=='3':
                return redirect('getkeeper_home')
            else:
                messages.error(request, 'username or password wrong')
                return redirect('login_form')
        else:
            messages.error(request, 'username or password wrong')
            return redirect('login_form')
    return HttpResponse(messages)
def doLogout(request):
    logout(request)
    return redirect('login_form')




@login_required(login_url='/')
def base(request):
    return render(request,"base.html")

@login_required(login_url='/')
def SuperVisorHome(request):
    total_Request =GuestRequest.objects.all().count() + Invitation.objects.all().count()
    total_approved_visitor =GuestRequest.objects.filter(approval_status="approved").count() + Invitation.objects.filter(approval_status="approved").count()
    total_badge=Badge.objects.all().count() + InvitationBadge.objects.all().count()
    total_Pending_Request =GuestRequest.objects.filter(approval_status="pending").count() + Invitation.objects.filter(approval_status="pending").count()
    requests=GuestRequest.objects.all()
    invitations =Invitation.objects.all()
  
    context={
        'total_Request':total_Request,
        'total_approved_visitor':total_approved_visitor,
        'total_Pending_Request':total_Pending_Request,
        'total_badge':total_badge,
        'invitations':invitations,
        'requests':requests,


    }
    return render(request,"Supervisor/supervisor_home.html",context)

@login_required(login_url='/')
def EmployeeHome(request):
    return render(request,"Employee/employee_home.html")

login_required(login_url='/')
def GetKeeperHome(request):
    return render(request,"Getkeeper/getkeeper_home.html")


def createAccount(request):
    departments=Department.objects.all()
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type=request.POST.get('user_type')
        department_name = request.POST.get('department_name')
        print(department_name,'==================')
        department=Department.objects.get(id=department_name)
        

        if user_type =='Supervisor':
            type=1
        elif user_type == 'Employee':
            type=2
        elif user_type == 'Getkeeper':
            type=3
        else:
            pass

        if CustomizedUser.objects.filter(email=email).exists():
            messages.warning(request, "email is already taken")
            return redirect('create_account')

        if CustomizedUser.objects.filter(username=username).exists():
            messages.warning(request, "username is already taken")
            return redirect('create_account')
        else:
            user = CustomizedUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=type
            )

            user.set_password(password)
            user.save()

            employee=Employee(
                customizeduser=user,
                department=department,
            )
            employee.save()

    context={
        'department':departments,
    }
    return render(request,"create_account.html",context)



def GuestRequestForm(request):
    requests=GuestRequest.objects.all()
    departments=Department.objects.all()
    context={
        'requests':requests,
        'departments':departments
    }
    if request.method == 'POST':
        identification_card = request.FILES.get('identification_card')
        guest_name = request.POST.get('guest_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        campany = request.POST.get('campany')
        date_of_visit=request.POST.get('date_of_visit')
        purpose_of_visit=request.POST.get('purpose_of_visit')
        department=Department.objects.get(id=request.POST.get('department'))
        responsible_person=request.POST.get('responsible_person')
        # print(profile_pic,first_name,last_name,email,username,password,user_type)

        requests = GuestRequest(
            guest_name=guest_name,
            phone=phone,
            email=email,
            identification_card=identification_card,
            date_of_visit=date_of_visit,
            purpose_of_visit=purpose_of_visit,
            visit_department=department,
            responsible_person=responsible_person, 
        )
        requests.save()
        return redirect('login_form')
    return render(request,"guest_request_form.html",context)






def ViewGuestRequest(request):
    employees=Employee.objects.all()
    requests=GuestRequest.objects.all()
    
    
    context={
        'requests':requests,
        'employees':employees,
        
    }
    
    return render(request,"Employee/view_guest_request.html",context)

def ManageRequest(request,id):
    from django.core.mail import EmailMessage
    import qrcode
    from io import BytesIO
    from django.core.files import File
    requests=GuestRequest.objects.filter(id=id)
    instance=GuestRequest.objects.get(id=id)
    if request.method == "POST":
        feedback=request.POST.get('feedback')
        arrival_time=request.POST.get('arrival_time')
        departure_time=request.POST.get('departure_time')
        email=request.POST.get('email')
        if 'approve' in request.POST:
            instance.approval_status = 'approved'
            instance.feedback=feedback
            instance.arrival_time=arrival_time
            instance.departure_time=departure_time
            #apply logic  here
            from django.core.mail import EmailMessage
            import qrcode
            from io import BytesIO
            from django.core.files import File

            # Function to generate a QR code and return the image file
            def generate_qr_code(data):
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                # Save the QR code image to a BytesIO buffer
                buffer = BytesIO()
                img.save(buffer)

                # Create a Django File object from the buffer
                image_file = File(buffer)
                return image_file

            # Example usage
            subject = 'QR Code Message '
            message = 'use this QR Code to Pass the get'
            from_email = 'sabokadiriba@gmail.com'
            recipient_list = [email]

            # Data to be encoded in the QR code
            qr_data = '{first_name},{last_name}'

            # Generate the QR code image file
            qr_code_file = generate_qr_code(qr_data)

            # HTML message with the QR code image
            html_message = f"""
            <html>
            <body>
                <h1>your Request is approved for detail view the following message .</h1>
                <p>This is Getpass Id with a QR code.</p>
                <img src="cid:{qr_code_file.name}" alt="QR Code">
            </body>
            </html>
            """

            # Create an EmailMessage object
            email = EmailMessage(
                subject,
                message,
                from_email,
                recipient_list,
            )

            # Attach the QR code file to the email
            email.attach(qr_code_file.name, qr_code_file.read(), "image/png")
            email.content_subtype = "html"
            email.body = html_message

            # Send the email
            email.send(fail_silently=False)

            #Create badge
            createBadge = Badge(
                            badge_id=instance,
                            )
            createBadge.save()

            #save instance here
            instance.save()
            return redirect('view_guest_request')
        elif 'disapprove' in request.POST:
            instance.approval_status = 'disapproved'
            instance.feedback=feedback
            instance.arrival_time=arrival_time
            instance.departure_time=departure_time
            #apply logic  here
            instance.save()
            return redirect('view_guest_request')
    context={
        'requests':requests,
    }
    
    return render(request,"Employee/manage_guest_request.html",context)
    


def Get_responsible_persons(request):
    from django.http import JsonResponse
    department_id = request.GET.get('department_id')
    # Filter responsible persons based on the selected department
    persons = Employee.objects.filter(department_id=department_id)
    # Create a list of dictionaries for JsonResponse
    data = [{'id': person.id, 'name': person.customizeduser.first_name + ' '+ person.customizeduser.last_name} for person in persons]
    
    return JsonResponse(data, safe=False)


def Invites(request):
    invitations=Invitation.objects.all()
    context={
        'invitations':invitations,
    }
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_visit=request.POST.get('date_of_visit')
        purpose_of_visit=request.POST.get('purpose_of_visit')

        responsible_person=CustomizedUser.objects.get(id=request.user.id)
        # print(profile_pic,first_name,last_name,email,username,password,user_type)

        invite = Invitation(
            guest_name=guest_name,
            phone=phone,
            email=email,
            arrival_date=date_of_visit,
            purpose_of_visit=purpose_of_visit,
            responsible_person=responsible_person, 
        )
        invite.save()
    return render(request,'Employee/invitation.html',context)



def ViewInvitation(request):
    invitations=Invitation.objects.all()
    context={
        'invitations':invitations,
        
    }
    
    return render(request,'Supervisor/view_invitation.html',context)


def ManageInvitation(request,id):
    from django.core.mail import EmailMessage
    import qrcode
    from io import BytesIO
    from django.core.files import File
    invitations=Invitation.objects.filter(id=id)
    instance=Invitation.objects.get(id=id)
    if request.method == "POST":
        feedback=request.POST.get('feedback')
        email=request.POST.get('email')
        if 'approve' in request.POST:
            instance.approval_status = 'approved'
            instance.feedback=feedback
            
            #apply logic  here
            from django.core.mail import EmailMessage
            import qrcode
            from io import BytesIO
            from django.core.files import File

            # Function to generate a QR code and return the image file
            def generate_qr_code(data):
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                # Save the QR code image to a BytesIO buffer
                buffer = BytesIO()
                img.save(buffer)

                # Create a Django File object from the buffer
                image_file = File(buffer)
                return image_file

            # Example usage
            subject = 'QR Code Message '
            message = 'use this QR Code to Pass the get'
            from_email = 'sabokadiriba@gmail.com'
            recipient_list = [email]

            # Data to be encoded in the QR code
            qr_data = '{first_name},{last_name}'

            # Generate the QR code image file
            qr_code_file = generate_qr_code(qr_data)

            # HTML message with the QR code image
            html_message = f"""
            <html>
            <body>
                <h1>your Request is approved for detail view the following message .</h1>
                <p>This is Getpass Id with a QR code.</p>
                <img src="cid:{qr_code_file.name}" alt="QR Code">
            </body>
            </html>
            """

            # Create an EmailMessage object
            email = EmailMessage(
                subject,
                message,
                from_email,
                recipient_list,
            )

            # Attach the QR code file to the email
            email.attach(qr_code_file.name, qr_code_file.read(), "image/png")
            email.content_subtype = "html"
            email.body = html_message

            # Send the email
            email.send(fail_silently=False)

            #Create badge
            createBadge = InvitationBadge(
                            badge_id=instance,
                            )
            createBadge.save()

            #save instance here
            instance.save()
            return redirect('view_invitation')
        elif 'disapprove' in request.POST:
            instance.approval_status = 'disapproved'
            instance.feedback=feedback 
            #apply logic  here
            instance.save()
            return redirect('view_invitation')
    context={
        'invitations':invitations,
    }
    
    return render(request,"Supervisor/manage_invitation.html",context)
    



def Deligation(request):
    if request.method == "POST":
       responsible_person=Employee.objects.get(id=request.POST.get("responsible_person"))
       reponsible_person_name=responsible_person.customizeduser.first_name + " " + responsible_person.customizeduser.last_name
       
       request=GuestRequest.objects.get(id=request.POST.get('request_id'))
       request.responsible_person=reponsible_person_name
       #applay notification logic here such as sending email
       
       request.save()
       return redirect("view_guest_request")

def CheckBadge(request):
    request_badge=Badge.objects.all()
    invitation_badge=InvitationBadge.objects.all()
    context={
        'request_badge':request_badge,
        'invitation_badge':invitation_badge,
        
    }
    
    return render(request,'Getkeeper/check_badge.html',context)



def BadgeDiteil(request,id):
    deteil1=Badge.objects.filter(id=id)
   
    context={
        'deteil1':deteil1,
       
    }
    return render(request,'Getkeeper/badge_detail.html',context)
def BadgeDiteil2(request,id):
    deteil2=InvitationBadge.objects.filter(id=id)
    context={    
        'deteil2':deteil2,
    }
    return render(request,'Getkeeper/badge_detail2.html',context)