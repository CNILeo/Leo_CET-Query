# Leo_CET-Query
        本脚本适用于2017年12月的四六级准考证暴力找回,已经通过伪造IP的方式绕过验证码  
        QQ群:362699550  
        本群将会实时更新查询脚本
        
        使用说明:  
            学信网(CHSI)版本须在Python 3环境运行，且运行前须在cmd内输入pip3 install requests,并且修改参数
            中国教育考试网（NEEA）须在Python 2环境运行，且运行前须在cmd内输入pip2 install requests
        
        2018.2.28 0.2 更新说明
            增加了固定座位号的功能
            新增了防止requests.exceptions.ChunkedEncodingError的错误
            现在查询接口速度已经恢复正常
            使用说明见源码，将有说明的地方修改成自己的参数即可。
            
    	已知问题
            1.输入已经的准考证和姓名会显示尝试失败，这是由于该正确的准考证和姓名查询太多次已经被列入查询黑名单
            2.没有查询成功过的正确准考证和姓名不会出现该情况
            
        2018.3.1 新增中国教育考试网（NEEA）接口：
            中国教育考试网（NEEA） Beta 0.1版本说明：
            1.该版本使用TensorFlow训练出来的CNN模型直接识别验证码
            2.直接运行即可,无需修改参数
            3.尚未发现任何问题
        
        感谢大家的支持！
        
<div style="align: center"> <img src="http://www.iot-leo.cn/AliPay.jpg"> </div>