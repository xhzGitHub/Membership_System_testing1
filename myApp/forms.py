from django import forms

class LoginForm(forms.Form):
    userphone = forms.CharField(max_length=11, required=True,
                               error_messages={'required':'账户不可以为空','invalid':'格式错误'},
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                'placeholder':"请输入11位电话号码",'style':'width:276px'}))
    passwd = forms.CharField(max_length=16,min_length=6,widget=forms.PasswordInput(attrs=
                            {'class': 'form-control','placeholder':"请输入6~16位字符",
                             'style':'width:276px'}))

