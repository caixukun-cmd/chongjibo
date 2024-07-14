package com.face.service;

import com.face.bean.result.FaceResult;

public interface EmailService {
    void sendEmail(String email);

    FaceResult loginemail(String code);
}
