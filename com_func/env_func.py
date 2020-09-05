from com_func.re_replace import phone_create
from com_func.confread import config
from com_func.confread import config_write
from com_func.test_log import log
from com_func.com_request_func import com_request
from jsonpath import jsonpath


def env_params_init():
    '''预置账号写入'''
    # 新增一个项目项目借款金额10000000
    # 将账号信息写入conf.ini文件
    try:
        env_params_regist()
        env_params_add_audit()
        env_params_recharge(config.getint("PRESET", "preset_recharge_amount"), config.getint("PRESET", "preset_recharge_times"))
    except Exception as e:
        print(e)
        log.error("测试环境数据初始化失败", exc_info=True)
        raise ValueError("测试环境数据初始化失败")


def env_params_regist():
    '''生成一组借款人/投资人/管理员账号,将账号信息写入conf.ini文件'''
    try:
        type_dic = {"loan_params": 1, "admin_params": 0, "invest_params": 1}
        for type_key, type_value in type_dic.items():
            params = {"mobile_phone": int(phone_create("new")), "pwd": "334498sun", "type": type_value}
            respone = com_request(env_params_regist, "register", params=params)
            if respone["msg"] == "OK":
                params.pop("type")
                config_write("PRESET", type_key, str(params))
            else:
                raise ValueError
    except Exception as e:
        log.error("测试环境数据初始化失败", exc_info=True)
        raise ValueError("测试环境数据初始化失败")


def env_params_recharge(amount, times):
    # ---------------------普通账户登录--------------------------------
    params = config.get("PRESET", "loan_params")
    respone = com_request(env_params_regist, "login", params=params)
    token = "Bearer" + " " + jsonpath(respone, "$..token")[0]
    # ---------------------普通账户充值--------------------------------
    params = {
            "member_id": jsonpath(respone, "$..id")[0],
            "amount": amount
            }
    for i in range(times): 
        respone = com_request(env_params_add_audit, "recharge", params=params, token=token)


def env_params_add_audit():
    '''预置投资项目100000000'''
    # ---------------------借款账户登录--------------------------------
    params = config.get("PRESET", "invest_params")
    respone = com_request(env_params_regist, "login", params=params)
    token = "Bearer" + " " + jsonpath(respone, "$..token")[0]
    # ---------------------普通账户添加项目--------------------------------
    params = {
            "member_id": jsonpath(respone, "$..id")[0],
            "title": "预置投资项目100000000",
            "amount": 100000000,
            "loan_rate": 1,
            "loan_term": 1,
            "loan_date_type": 1,
            "bidding_days": 1
            }
    respone = com_request(env_params_add_audit, "add", params=params, token=token)
    loan_id = jsonpath(respone, "$..id")[0]

    # ---------------------管理账户登录--------------------------------
    params = config.get("PRESET", "admin_params")
    respone = com_request(env_params_add_audit, "login", params=params)
    token = "Bearer" + " " + jsonpath(respone, "$..token")[0]
    # ---------------------管理账户审核--------------------------------
    params = {
            "loan_id": loan_id,
            "approved_or_not": True
            }
    respone = com_request(env_params_add_audit, "audit", params=params, token=token)
    assert respone["code"] == 0
    config_write("SETUPDATA", "audit_loan", {"loan_id": loan_id, "amount": 100000000})