$(document).ready(function () {
    var account = document.getElementById('account')
    var accounterr = document.getElementById('accounterr')
    var checkerr = document.getElementById('checkerr')

    var pass = document.getElementById('pass')
    var passerr = document.getElementById('passerr')

    var passwd = document.getElementById('passwd')
    var passwderr = document.getElementById('passwderr')



    //var userDoesNotExist = document.getElementById('userDoesNotExist')
    //var login_passwd = document.getElementById('login_passwd')

    //初始化***err的状态，即不显示
    accounterr.style.display = "none"
    checkerr.style.display = "none"

    //只要聚焦，就不显示输入错误
    account.addEventListener("focus",function () {

        accounterr.style.display = "none"
        checkerr.style.display = "none"

    },false)
/*
    login_passwd.addEventListener("focus",function () {
        userDoesNotExist.style.display = "none"
    },false)
*/

    //离焦，验证输入格式是否正确
    account.addEventListener('blur',function () {
        instr = this.value
        if (instr.length != 11){
            console.log('123')
            accounterr.style.display = 'block'
            return
        }

        $.post('/checkuserid/',{'userid':instr},function (data) {
            console.log(data.status)
            if (data.status == 'error'){
                checkerr.style.display = 'block'
            }

        })

    },false)


    //密码：
    //只要聚焦，就不显示输入错误

    passerr.style.display = "none"

    pass.addEventListener("focus",function () {
        passerr.style.display = "none"
    },false)

    //离焦，验证输入格式是否正确
    pass.addEventListener('blur',function () {
        instr = this.value
        if (instr.length < 6 || instr.length > 16){
            passerr.style.display = 'block'
            return
        }

    },false)

    //验证密码：
    passwderr.style.display = "none"

    passwd.addEventListener("focus",function () {
        passwderr.style.display = "none"
    },false)

    //离焦，验证输入格式是否正确
    passwd.addEventListener('blur',function () {
        instr = this.value
        if ( instr != pass.value){
            passwderr.style.display = "block"
        }
    },false)


})