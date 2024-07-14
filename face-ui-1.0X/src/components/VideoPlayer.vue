<template>
  <div class="video-player">
    <input type="file" @change="loadVideo" accept="video/mp4" />
    <video ref="videoPlayer" class="video-js vjs-default-skin" controls preload="auto">
      Your browser does not support the video tag.
    </video>
  </div>
</template>

<script>
import videojs from 'video.js';
import 'video.js/dist/video-js.css';

export default {
  name: 'VideoPlayer',
  data() {
    return {
      player: null
    };
  },
  methods: {
    loadVideo(event) {
      const file = event.target.files[0];
      if (file && file.type === 'video/mp4') {
        const videoElement = this.$refs.videoPlayer;
        const videoURL = URL.createObjectURL(file);

        if (!this.player) {
          this.player = videojs(videoElement, {
            autoplay: true,
            controls: true,
            sources: [{
              src: videoURL,
              type: 'video/mp4'
            }]
          });
        } else {
          this.player.src({ type: 'video/mp4', src: videoURL });
          this.player.load();
          this.player.play();
        }
      } else {
        alert('Please select a valid MP4 file.');
      }
    }
  },
  beforeDestroy() {
    if (this.player) {
      this.player.dispose();
    }
  }
};
</script>

<style scoped>
.video-player {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

video {
  width: 100%;
  max-width: 800px;
  margin-top: 20px;
}
</style>
