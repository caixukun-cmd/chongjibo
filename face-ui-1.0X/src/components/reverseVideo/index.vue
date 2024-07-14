<template>
  <div>
    <input type="file" @change="handleFileChange">
    <br>
    <video ref="videoPlayer" controls width="640" height="360">
      Your browser does not support the video tag.
    </video>
  </div>
</template>

<script>
export default {
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;

      // 检查文件类型是否为 MP4
      if (file.type !== 'video/mp4') {
        alert('请上传 MP4 格式的视频文件！');
        return;
      }

      // 创建一个 URL 对象，用于视频播放
      const videoPlayer = this.$refs.videoPlayer;
      const videoURL = URL.createObjectURL(file);

      // 设置视频播放源
      videoPlayer.src = videoURL;
      videoPlayer.play();
    }
  }
}
</script>

<style>
/* Add your styles here if needed */
</style>
