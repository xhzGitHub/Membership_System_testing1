from django.db import models

class User(models.Model):
    userPhone = models.CharField(max_length=11,unique=True)
    #账户由电话号码申请账户
    userpasswd = models.CharField(max_length=20)
    #账户密码
    userRank = models.CharField(max_length=20, default='黄金会员')
    #会员等级
    userBlance = models.IntegerField(default=0)
    #会员余额
    userIntegral = models.IntegerField(default=0)
    #会员积分
    userCoupon = models.CharField(max_length=150,default='无')
    #优惠券
    userExpensesRecord = models.CharField(max_length=150,default='无')
    #消费记录
    userLoginStatus = models.BooleanField(default=False)
    #是否登录
    userToken = models.CharField(max_length=50)
    @classmethod
    def createuser(cls,phone,passwd,rank,blance,integral,coupin,expensesrecord,loginstatus,token):
        u = cls(userPhone = phone, userpasswd = passwd,userRank = rank, userBlance = blance,
                userIntegral = integral, userCoupon = coupin,userExpensesRecord = expensesrecord,
                userLoginStatus=loginstatus, userToken =token)
        return u
