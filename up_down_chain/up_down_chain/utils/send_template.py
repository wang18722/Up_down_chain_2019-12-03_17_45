from django.conf import settings
import requests

from Users.models import PayCertificationInfo, EnterpriseCertificationInfo
from oauth.models import CustomerInformation
import json
import datetime


class Send_template(object):
    def Payment_notice_Template(self, openid, total_fee, order_id, access_token, time):
        # access_token = WeChatClient(appid=settings.WXAPPID, secret=settings.WXAPPSECRET).access_token
        """
        {【上下链】平台有新的企业申请认证，请尽快审核。}
        收款金额：{200.00元}
        商户名称：{企业名称}
        订单号：{订单编号}
        付款用户：{付款的微信昵称}
        订单时间：{2018-12-24 18:18}
        {今日累计****家企业申请认证。}

        """
        certificat = PayCertificationInfo.objects.get(order_id=order_id)
        user = CustomerInformation.objects.get(username=openid)
        for i in range(2):
            if i == 0:
                openids = "oO5Eq6Gii1YiUQ2r_PBdgq8swz3Q"
            else:
                openids = "oO5Eq6NGE1zV94yoHgLZnhcAJNOc"
            total_fee = int(total_fee) / 100
            data = {
                "touser": openids,
                "url": "http://www.shangxialian.net/js/#/company-cert",
                "template_id": settings.TEMPLATE_DICT["2"],
                "data": {
                    "first": {
                        "value": "【上下链】平台有新的企业申请认证，请尽快审核。"
                    },
                    "keyword1": {
                        "value": str(total_fee) + "元",
                        "color": "#09a3a3"
                    },
                    "keyword2": {
                        "value": certificat.company_name,
                        "color": "#09a3a3"
                    },
                    "keyword3": {
                        "value": order_id,
                        "color": "#09a3a3"
                    },
                    "keyword4": {
                        "value": user.first_name,
                        "color": "#09a3a3"
                    },
                    "keyword5": {
                        "value": time[0:4] + '-' + time[4:6] + '-' + time[6:8] + ' ' + time[8:10] + ':' + time[10:12],
                        "color": "#09a3a3"
                    },
                    "remark": {
                        "value": "",
                    }
                }
            }
            i += 1
            requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                          data=json.dumps(data))

    def Authentication_adopt(self, access_token, company_name, user_id, state):
        user = CustomerInformation.objects.get(id=user_id)
        if state == 2:
            state = "通过"
        else:
            state = "不通过"
        data = {
            "touser": user.username,
            "url": "http://www.shangxialian.net/",
            "template_id": settings.TEMPLATE_DICT["7"],
            "data": {
                "first": {
                    "value": "【上下链】尊敬的" + user.first_name + "恭喜您，您申请的企业已通过上下链企业认证审核。",


                },
                "keyword1": {
                    "value": company_name,
                },
                "keyword2": {
                    "value": str(datetime.datetime.today())[:19],
                },
                "remark": {
                    "value": "用上下链触客  AI赋能营销",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                      data=json.dumps(data))

    def To_examine_template(self, id, content, access_token):
        """
        短信模板审核通知
        :param id:
        :param content:
        :return:
        """
        # access_token = WeChatClient(appid=settings.WXAPPID, secret=settings.WXAPPSECRET).access_token

        user = CustomerInformation.objects.get(id=id)

        for i in range(2):
            if i == 0:
                openid = "oO5Eq6Gii1YiUQ2r_PBdgq8swz3Q"
            else:
                openid = "oO5Eq6NGE1zV94yoHgLZnhcAJNOc"
            data = {
                "touser": openid,
                "url": "http://www.shangxialian.net/js/#/operator",
                "template_id": settings.TEMPLATE_DICT["15"],
                "data": {
                    "first": {
                        "value": "【上下连】" + user.first_name + "：" + "已提交短信模板资料，请尽快审核！",

                    },
                    "keyword1": {
                        "value": content,
                        "color": "#09a3a3"
                    },
                    "keyword2": {
                        "value": str(datetime.datetime.today())[:19],
                        "color": "#09a3a3"
                    },
                    "remark": {
                        "value": "请点击审核！",
                    }
                }
            }
            i += 1
            requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                          data=json.dumps(data))

    def To_examine_template_result(self, user_id, state, access_token):
        """
        审核结果通知
        :param token:
        :param state:
        :return:
        """
        user = CustomerInformation.objects.get(id=user_id)
        # access_token = WeChatClient(appid=settings.WXAPPID, secret=settings.WXAPPSECRET).access_token
        if state == 2:
            states = "通过"
        else:
            states = "不通过"
        data = {
            "touser": user.username,
            "url": "http://www.shangxialian.net/",
            "template_id": settings.TEMPLATE_DICT["17"],
            "data": {
                "first": {
                    "value": "【上下链】尊敬的" + user.first_name + "用户，您上传的短信模板内容审核结果已出。",

                },
                "keyword1": {
                    "value": states,
                },
                "keyword2": {
                    "value": str(datetime.datetime.today())[:19],
                },
                "remark": {
                    "value": "现在您可以进行短信触客推送。",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                      data=json.dumps(data))

    def To_Examine_Template_Subscribe(self, user, keywords_array, area_name, access_token):
        # access_token = WeChatClient(appid=settings.WXAPPID, secret=settings.WXAPPSECRET).access_token

        data = {
            "touser": user.username,
            "url": "http://www.shangxialian.net/",
            "template_id": settings.TEMPLATE_DICT["1"],
            "data": {
                "first": {
                    "value": "【上下链】" + user.first_name + ",您订阅推送关键词内容设置成功。每日为您‘订阅推送’最新采招商机及微信提醒通知服务",

                },
                "keyword1": {
                    "value": str(datetime.datetime.today())[:19],
                },
                "keyword2": {
                    "value": "每日提醒",
                },
                "keyword3": {
                    "value": keywords_array,
                },
                "keyword4": {
                    "value": area_name,
                },
                "remark": {
                    "value": "用上下链触客  AI赋能营销",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                      data=json.dumps(data))

    def Notification_fail_Template(self, access_token, company_name, user_id):
        user = CustomerInformation.objects.get(id=user_id)

        data = {
            "touser": user.username,
            "url": "http://www.shangxialian.net/",
            "template_id": settings.TEMPLATE_DICT["8"],
            "data": {
                "first": {
                    "value": "【上下链】" + user.first_name +"您好，您申请的上下链企业认证审核不通过。请修改后重新提交。",

                },
                "keyword1": {
                    "value": str(datetime.datetime.today())[:19],
                    "color": "#09a3a3"
                },
                "keyword2": {
                    "value": "不通过",
                    "color": "#09a3a3"
                },
                "keyword3": {
                    "value": "资料审核失败",
                    "color": "#09a3a3"
                },
                "remark": {
                    "value": "用上下链触客  AI赋能营销",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                      data=json.dumps(data))

    def SubscriptionPushTemplate(self, openid, total_fee, access_token, time, user_id, balance, first_name):
        """充值"""
        enterprise = EnterpriseCertificationInfo.objects.get(user=user_id)
        data = {
            "touser": openid,
            "template_id": settings.TEMPLATE_DICT["4"],
            "data": {
                "first": {
                    "value": "【上下链】" + first_name + "您好，您的企业账户已充值成功！",

                },
                "keyword1": {
                    "value": enterprise.name,
                    "color": "#09a3a3"
                },
                "keyword2": {
                    "value": str(time),
                    "color": "#09a3a3"
                },
                "keyword3": {
                    "value": str(total_fee)+"元",
                    "color": "#09a3a3"
                },
                "keyword4": {
                    "value": str(balance)+"元",
                    "color": "#09a3a3"
                },
                "remark": {
                    "value": "用上下链触客  AI赋能营销",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,data=json.dumps(data))

    def RefillAlertAdministrator(self,access_token,total_fee,user_id,first_name):
        enterprise = EnterpriseCertificationInfo.objects.get(user=user_id)
        for i in range(2):
            if i == 0:
                openids = "oO5Eq6Gii1YiUQ2r_PBdgq8swz3Q"
            else:
                openids = "oO5Eq6NGE1zV94yoHgLZnhcAJNOc"
            data = {
                "touser": openids,
                "template_id": settings.TEMPLATE_DICT["4"],
                "data": {
                    "first": {
                        "value": "【上下链】上下链有企业充值成功。"
                    },
                    "keyword1": {
                        "value": str(total_fee) + "元",
                        "color": "#09a3a3"
                    },
                    "keyword2": {
                        "value": enterprise.name,
                        "color": "#09a3a3"
                    },
                    "keyword3": {
                        "value": enterprise.company_id,
                        "color": "#09a3a3"
                    },
                    "keyword4": {
                        "value": first_name,
                        "color": "#09a3a3"
                    },
                    "keyword5": {
                        "value": str(datetime.datetime.today())[:19],
                        "color": "#09a3a3"
                    },
                    "remark": {
                        "value": "【"+ enterprise.name +"】企业充值成功",
                    }
                }
            }
            i += 1
            requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                          data=json.dumps(data))


    def CertificationNotice(self, openid, access_token):
        """认证通知"""
        user = CustomerInformation.objects.get(username=openid)
        enterprise = EnterpriseCertificationInfo.objects.get(user=user.id)

        data = {
            "touser": openid,
            "template_id": settings.TEMPLATE_DICT["5"],
            "data": {
                "first": {
                    "value": "【上下链】" + user.first_name + "您好，您申请的（企业名称）上下链企业认证已提交成功。",

                },
                "keyword1": {
                    "value": "上下链企业认证",
                    "color": "#09a3a3"
                },
                "keyword2": {
                    "value": enterprise.contacts,
                    "color": "#09a3a3"
                },
                "keyword3": {
                    "value": str(datetime.datetime.today())[:19],
                    "color": "#09a3a3"
                },
                "remark": {
                    "value": "用上下链触客  AI赋能营销",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                      data=json.dumps(data))
