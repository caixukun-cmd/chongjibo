<template>
  <div class="video-stream-viewer">
    <div class="stream-grid">
      <div v-for="stream in streams" :key="stream.id" class="stream-container">
        <h3>{{ stream.name }}</h3>
        <img v-if="stream.isFetching" :src="stream.currentImage" :alt="stream.name" @error="handleImageError(stream.id)"/>
        <div v-else class="placeholder">视频流未获取</div>
        <button @click="fetchStream(stream)">{{ stream.isFetching ? '刷新视频流' : '获取视频流' }}</button>
        <div class="controls">
          <input v-model="stream.x1" placeholder="左上角x:">
          <input v-model="stream.y1" placeholder="左上角y:">
          <input v-model="stream.x2" placeholder="右下角x:">
          <input v-model="stream.y2" placeholder="右下角y:">
          <button @click="setDangerArea(stream)">确认</button>
        </div>
      </div>
    </div>
    <textarea v-model="messages" placeholder="警告信息" readonly></textarea>
  </div>
</template>

<script>
import axios from 'axios';
import io from 'socket.io-client';

export default {
  name: 'VideoStreamViewer',
  data() {
    return {
      videoFeedBaseUrl: 'http://127.0.0.1:5000/video_feed/stream_',
      streams: [
        {id: '1', name: 'Stream 1', x1: '', y1: '', x2: '', y2: '', isFetching: false,imageQueue: [], currentImageIndex:0},
        {id: '2', name: 'Stream 2', x1: '', y1: '', x2: '', y2: '', isFetching: false,imageQueue: [], currentImageIndex:0},
        {id: '3', name: 'Stream 3', x1: '', y1: '', x2: '', y2: '', isFetching: false,imageQueue: [], currentImageIndex:0},
        {id: '4', name: 'Stream 4', x1: '', y1: '', x2: '', y2: '', isFetching: false,imageQueue: [], currentImageIndex:0},
        {id: '5', name: 'Stream 5', x1: '', y1: '', x2: '', y2: '', isFetching: false,imageQueue: [], currentImageIndex:0},
        {id: '6', name: 'Stream 6', x1: '', y1: '', x2: '', y2: '', isFetching: false,imageQueue: [], currentImageIndex:0},
      ],
      socket: null,
      messages: '',
      preloadCount:10,
      updateInterval:1000
    };
  },
  mounted() {
    this.setupWebSocket();
  },
  methods: {
    getVideoFeedUrl(streamId) {
      return `${this.videoFeedBaseUrl}${streamId}`;
    },
    handleImageError(streamId) {
      console.error(`Failed to load the video stream image for Stream ${streamId}.`);
    },
    setupWebSocket() {
      this.socket = io('http://127.0.0.1:5000');
      this.socket.on('exception_message', (data) => {
        this.messages += data.message + '\n';
      });
    },
    preloadImages(stream) {
      for (let i =0; i < this.preloadCount; i++) {
        const imageUrl = `${this.getVideoFeedUrl(stream.id)}`;
        stream.imageQueue.push(imageUrl);
      }
      stream.currentImage = stream.imageQueue[0];
    },
    fetchStream(stream) {
      if (stream.fetchInterval) {
         clearInterval(stream.fetchInterval);
         stream.imageQueue = [];
         stream.currentImageIndex =0;
      }

      stream.isFetching = true;
      this.preloadImages(stream);

      stream.fetchInterval = setInterval(() => {
        if (stream.imageQueue.length >0) {
          stream.currentImageIndex = (stream.currentImageIndex +1) % stream.imageQueue.length;
          stream.currentImage = stream.imageQueue[stream.currentImageIndex];
        }
      }, this.updateInterval);
    },
    setDangerArea(stream) {
      const area = {
        stream: stream.id,
        x1: parseInt(stream.x1),
        y1: parseInt(stream.y1),
        x2: parseInt(stream.x2),
        y2: parseInt(stream.y2)
      };

      if (isNaN(area.x1) || isNaN(area.y1) || isNaN(area.x2) || isNaN(area.y2)) {
        alert('请输入有效的数字');
        return;
      }

      axios.post('http://127.0.0.1:5000/set_area', area)
          .then(response => {
            console.log(response.data.message);
            alert(`已为 ${stream.name} 设置危险区域`);
          })
          .catch(error => {
            console.error('Error setting danger area:', error);
            alert('设置危险区域失败');
          });
    }
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }
};
</script>

<style scoped>
.video-stream-viewer {
  display: flex;
  flex-direction: column;
}

.stream-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stream-container {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
}

img {
  max-width: 100%;
  height: auto;
}

.placeholder {
  height: 240px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0;
  color: #888;
}

.controls {
  margin-top: 10px;
}

.controls input {
  width: 60px;
  margin-right: 5px;
}

textarea {
  width: 100%;
  height: 100px;
  margin-top: 20px;
  resize: vertical;
}
</style>
