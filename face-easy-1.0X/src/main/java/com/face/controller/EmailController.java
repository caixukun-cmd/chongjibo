package com.face.controller;

import com.face.bean.result.FaceResult;
import com.face.pojo.EmailRequest;
import com.face.service.EmailService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;


@Api(value = "测试接口", tags = "用户管理相关的接口", description = "用户测试接口")
@RestController
@Slf4j
public class EmailController {

    @Autowired
    EmailService emailService;

    @ApiOperation(value="邮箱验证码发送", notes="发送邮箱验证码")
    @PostMapping("/email/send-code")
    public FaceResult EmailResult( @RequestBody EmailRequest emailRequest)
    {

        emailService.sendEmail(emailRequest.getEmail());
        return FaceResult.success();

    }


}
