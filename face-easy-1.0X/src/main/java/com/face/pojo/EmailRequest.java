package com.face.pojo;

import io.swagger.annotations.ApiOperation;
import lombok.Data;
import lombok.Getter;

@Getter
@Data
@ApiOperation(value="Email实体类", notes="接收前端的邮箱和验证码")
public class EmailRequest {

    // Getter和Setter方法
    private String email;

    private String code;


}