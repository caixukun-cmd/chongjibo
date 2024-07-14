package com.face.server;

import com.face.bean.result.FaceResult;
import com.tencentcloudapi.common.AbstractModel;

import com.tencentcloudapi.common.Credential;
import com.tencentcloudapi.common.profile.ClientProfile;
import com.tencentcloudapi.common.profile.HttpProfile;
import com.tencentcloudapi.common.exception.TencentCloudSDKException;
import com.tencentcloudapi.iai.v20200303.IaiClient;
import com.tencentcloudapi.iai.v20200303.models.*;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * @author tanyongpeng
 * <p>调用腾讯接口</p>
 **/
@Component
@Data
@Slf4j
public class DetectLiveFace {

    @Value("${tencentcloudapi.secretId}")
    private String secretId;
    @Value("${tencentcloudapi.secretKey}")
    private String secretKey;
    @Value("${tencentcloudapi.endpoint}")
    private String endpoint;
    @Value("${tencentcloudapi.region}")
    private String region;

    public FaceResult detectLiveFace(String image){
        FaceResult faceResult = new FaceResult();
        try{
            Credential cred = new Credential(secretId, secretKey);
            HttpProfile httpProfile = new HttpProfile();
            httpProfile.setEndpoint(endpoint);
            ClientProfile clientProfile = new ClientProfile();
            clientProfile.setHttpProfile(httpProfile);
            IaiClient client = new IaiClient(cred, region, clientProfile);
            DetectLiveFaceRequest req = new DetectLiveFaceRequest();
            req.setImage(image);
            DetectLiveFaceResponse resp = client.DetectLiveFace(req);
            faceResult.setScore(resp.getScore());
            faceResult.setCode(FaceResult.LIVE_FACE);
        } catch (TencentCloudSDKException e) {
            faceResult.setCode(FaceResult.FACE_ERROR);
            faceResult.setMsg(e.getMessage());
            e.printStackTrace();
        }
        return faceResult;
    }
}
