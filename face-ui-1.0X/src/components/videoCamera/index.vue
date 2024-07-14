<template>
  <div id="app">
    <VideoPlayer />
  </div>
</template>

<script>
import VideoPlayer from '@/components/VideoPlayer.vue'; // 确保路径正确

export default {
  name: 'App',
  components: {
    VideoPlayer
  }
};
</script>

<style scoped>
#app {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
}
</style>
