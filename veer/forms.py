import imp
from django.forms import ModelForm
from veer import models
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class create_person_form(ModelForm):
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = models.Person
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super(create_person_form, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Your full name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Your phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Your email address'
        self.fields['message'].widget.attrs['placeholder'] = 'Your message!'

    def clean(self):
 
        # data from the form is fetched using super function
        super(create_person_form, self).clean()
         
        # extract the username and text field from the data
        username = self.cleaned_data.get('name')
        phone = self.cleaned_data.get('phone')
        email = self.cleaned_data.get('email')
        message = self.cleaned_data.get('message')


        # conditions to be met for the username length

        def fun1(username):
            if username is None:
                return 1
            for x in username:
                if (x >= 'a' and x <= 'z') or (x >= 'A' and x <= 'Z') or (x == ' '):
                    continue
                else:
                    return 1
            return 0


        def fun2(phone):
            if phone is None:
                return 1
            for x in phone:
                if(x >= '0' and x <= '9'):
                    continue
                else:
                    return 1
            return 0


        def fun3(email):
            if email is None:
                return 1
            idx = len(email) - 9
            if email[idx] != 'g':
                return 1
            if(email[idx + 1] != 'm'):
                return 1
            if(email[idx + 2] != 'a'):
                return 1
            if(email[idx + 3] != 'i'):
                return 1
            if(email[idx + 4] != 'l'):
                return 1

            return 0 


        if username is not None and len(username) < 8:
            self._errors['name'] = self.error_class([
                'Minimum 8 characters required'])
        elif (fun1(username)):
            self._errors['name'] = self.error_class([
                'Characters should be uppercase, lowercase or whitespaces.'])


        if phone is not None and len(phone) < 10:
            self._errors['phone'] = self.error_class([
                'Phone number should be of the form 910123456789, where 91 is the country code.'])
        
        elif (fun2(phone)):
            self._errors['phone'] = self.error_class([
                'Phone number should be numeric.'])


        if(email is not None and len(email) < 11):
            self._errors['email'] = self.error_class([
                'Email should be of atleast 11 characters.'])

        elif(fun3(email)):
            self._errors['email'] = self.error_class([
                'Last 9 characters should be gmail.com.'])

        if message is None:
            self._errors['message'] = self.error_class([
                'Write something!.'])

        # return any errors if found
        return self.cleaned_data