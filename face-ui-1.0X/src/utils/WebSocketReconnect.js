class WebSocketReconnect {
    constructor(url) {
      this.url = url;
      this.connect();
    }
  
    connect() {
      this.socket = new WebSocket(this.url);
      this.socket.onopen = () => {
        console.log('WebSocket connection established');
      };
      this.socket.onclose = () => {
        console.log('WebSocket connection closed, reconnecting...');
        setTimeout(() => this.connect(), 1000); // Reconnect after 1 second
      };
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.socket.close();
      };
    }
  
    send(data) {
      if (this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(data);
      } else {
        console.warn('WebSocket is not open. Ready state:', this.socket.readyState);
      }
    }
  
    close() {
      this.socket.close();
    }
  }
  
  export default WebSocketReconnect;
  