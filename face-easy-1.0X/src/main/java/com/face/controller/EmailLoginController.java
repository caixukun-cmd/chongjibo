package com.face.controller;


import com.face.bean.result.FaceResult;
import com.face.pojo.EmailRequest;
import com.face.service.EmailService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;


@Api(value = "测试接口", tags = "用户管理相关的接口", description = "用户测试接口")
@RestController
public class EmailLoginController {
    @Autowired
    EmailService emailService;


    @ApiOperation(value="邮箱验证码登录验证", notes="验证邮箱验证码")
    @PostMapping("/email/login")
    public FaceResult emaillogin(@RequestBody EmailRequest emailRequest)
    {
        return emailService.loginemail(emailRequest.getCode());

    }
}
