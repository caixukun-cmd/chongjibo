package com.face.service.impl;

import cn.hutool.core.util.RandomUtil;
import com.face.bean.Face;
import com.face.bean.result.FaceResult;
import com.face.service.EmailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Service
public class EmailServiceImpl implements EmailService {


    private Integer code;
    @Value("${spring.mail.username}")
    private String from="";

    @Autowired
    private JavaMailSender javaMailSender;
    public void sendEmail(String email) {
        // 发送邮件的逻辑
        code = RandomUtil.randomInt(100000, 999999);
        SimpleMailMessage simpleMailMessage = new SimpleMailMessage();
        simpleMailMessage.setFrom(from);
        simpleMailMessage.setTo(email);
        simpleMailMessage.setSubject("test");
        simpleMailMessage.setText("Code:" + code.toString());
        javaMailSender.send(simpleMailMessage);
        System.out.println(code);

    }

    @Override
    public FaceResult loginemail(String code1) {
        System.out.println(code);
        System.out.println(code1);
        if(Objects.equals(String.valueOf(code1), String.valueOf(code)))
        {
            return FaceResult.success("登录成功");
        }else {

            return FaceResult.error(400);
        }
    }
}
