/**
 * Created by Administrator on 2018/1/31.
 */

$(function () {
    var submitBtn = $("#submit");
    submitBtn.click(function (event) {
        event.preventDefault();
        // 获取标签
        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $('input[name=newpwd2]');

        // 获取值
        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        // 发送ajax请求
        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('恭喜！密码修改成功！');
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                }else{
                    var message = data['message'];
                    zlalert.alertInfoToast(message);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});