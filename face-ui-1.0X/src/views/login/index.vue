<template>
  <div>
    <div class="login"></div>

    <!--登录中间块-->
    <div class="login-mid">
      <div class="login-mid-top">
        <div class="shadow-top-left"></div>
        <div class="shadow-top-right"></div>
      </div>
      <div class="login-mid-mid">

        <!--捕获人脸区域-->
        <div class="videoCamera-canvasCamera">
          <video id="videoCamera" :width="videoWidth" :height="videoHeight" autoplay></video>
          <canvas
            style="display: none"
            id="canvasCamera"
            :width="videoWidth"
            :height="videoHeight"
          ></canvas>

          <!--人脸特效区域-->
          <div v-if="faceImgState" class="face-special-effects-2"></div>
          <div v-else class="face-special-effects"></div>
        </div>

        <!--按钮区域-->
        <div class="face-btn">
          <button @click="faceVef()">{{ faceImgState ? '正在识别中...' : '开始识别' }}</button>
        </div>

        <!--邮箱验证码登录区域-->
        <div class="email-login">
          <input type="email" v-model="email" placeholder="请输入邮箱" />
          <button @click="sendVerificationCode">发送验证码</button>
          <input type="text" v-model="verificationCode" placeholder="请输入验证码" />
          <button @click="emailLogin">邮箱验证码登录</button>
        </div>

        <!--消息区域-->
        <div class="msg">
          <div class="server-msg">{{ msg }}</div>
          <div class="welcome">Welcome to face recognition</div>
        </div>

      </div>
      <div class="login-mid-bot">
        <div class="shadow-bot-left"></div>
        <div class="shadow-bot-right"></div>
      </div>
    </div>
  </div>
</template>

<script>
import $camera from '../../camera/index.js'
export default {
  data() {
    return {
      videoWidth: 200,
      videoHeight: 200,
      msg: '',
      faceImgState: false,
      faceOption: {},
      email: '',
      verificationCode: '',
      faceVerified: false,
      emailVerified: false
    };
  },
  mounted() {
    //调用摄像头
    this.faceOption = $camera.getCamera({
      videoWidth: 200,
      videoHeight: 200,
      thisCancas: null,
      thisContext: null,
      thisVideo: null,
      canvasId: 'canvasCamera',
      videoId: 'videoCamera'
    });
  },
  methods: {
    // 调用后台接口
    faceVef() {
      // 开始绘制图片
      let imageBase = $camera.draw(this.faceOption)
      if (this.faceImgState) {
        return
      }
      this.faceImgState = true
      if (imageBase === '' || imageBase === null || imageBase === undefined) {
        this.$message.error("图片数据为空")
      } else {
        this.$http.post("/face/vef", { imageBase }).then(res => {
          console.log(res)
          this.faceImgState = false
          if (res.data.code === 200) {
            this.faceVerified = true;
            this.checkLoginStatus();
          } else {
            this.$message.error(res.data.msg)
          }
        }, onerror => {
          this.faceImgState = false
        })
      }
    },
    // 发送验证码方法
    sendVerificationCode() {
      if (this.email === '') {
        this.$message.error("请输入邮箱")
        return
      }
      this.$http.post("/email/send-code", { email: this.email }).then(res => {
        if (res.data.code === 200) {
          this.$message.success("验证码已发送到您的邮箱")
        } else {
          this.$message.error(res.data.msg)
        }
      }).catch(err => {
        console.error(err)
        this.$message.error("发送验证码失败，请重试")
      })
    },
    // 邮箱验证码登录方法
    emailLogin() {
      if (this.email === '' || this.verificationCode === '') {
        this.$message.error("请输入邮箱和验证码")
        return
      }
      this.$http.post("/email/login", { email: this.email, code: this.verificationCode }).then(res => {
        if (res.data.code === 200) {
          this.emailVerified = true;
          this.checkLoginStatus();
        } else {
          this.$message.error(res.data.msg)
        }
      }).catch(err => {
        console.error(err)
        this.$message.error("登录失败，请重试")
      })
    },
    checkLoginStatus() {
      if (this.faceVerified && this.emailVerified) {
        this.$message.success("登录成功");
        this.$router.push("/home");
      } else if (this.faceVerified && !this.emailVerified) {
        this.$message.info("人脸识别成功，请完成邮箱验证码验证");
      } else if (!this.faceVerified && this.emailVerified) {
        this.$message.info("邮箱验证成功，请完成面部识别");
      }
    }
  },
};
</script>

<style>
@import "./index.css";

/* 添加邮箱登录框的样式 */
.email-login {
  margin-top: 20px;
}
.email-login input {
  padding: 10px;
  margin-right: 10px;
}
.email-login button {
  padding: 10px;
}
</style>
