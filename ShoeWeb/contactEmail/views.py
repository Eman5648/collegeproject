from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.template.loader import get_template
from django.core.mail import EmailMessage

# redirect success page
def Success(request):
    return render(request, 'email/success.html')

def Contact(request):
    Contact_Form = ContactForm
    if request.method == 'POST':
        form = Contact_Form(data=request.POST)
        
        if form.is_valid():
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            contact_content = request.POST.get('content')

            template = get_template('email/contact_form.txt')
            content = {
                'contact_name' : contact_name,
                'contact_email' : contact_email,
                'contact_content' : contact_content,
            }

            content = template.render(content)

            email = EmailMessage(
            "New Email from",
            content,
            "Schuh Office web" + '',
            ['SchuhOffice@gmail.com'],
            headers = { 'Reply To': contact_email}
        )

        email.send()
        return redirect('email:success')
    return render(request, 'email/contact.html', {'form':Contact_Form})