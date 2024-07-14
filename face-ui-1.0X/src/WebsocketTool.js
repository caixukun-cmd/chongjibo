//需求：在JavaScript中实现WebSocket连接失败后3分钟内尝试重连3次的功能，你可以设置一个重连策略，
//     包括重连的间隔时间、尝试次数以及总时间限制。

/**
 * @param {string} url  Url to connect
 * @param {number} maxReconnectAttempts Maximum number of times
 * @param {number} reconnect Timeout
 * @param {number} reconnectTimeout Timeout
 *
 */
class WebSocketReconnect {
 
    constructor(url, maxReconnectAttempts = 3, reconnectInterval = 20000, maxReconnectTime = 180000) {
      this.url = url
      this.maxReconnectAttempts = maxReconnectAttempts
      this.reconnectInterval = reconnectInterval
      this.maxReconnectTime = maxReconnectTime
      this.reconnectCount = 0
      this.reconnectTimeout = null
      this.startTime = null
      this.socket = null
  
      this.connect()
    }
  
    //连接操作
    connect() {
      console.log('connecting...')
      this.socket = new WebSocket(this.url)
  
      //连接成功建立的回调方法
      this.socket.onopen = () => {
        console.log('WebSocket Connection Opened!')
        this.clearReconnectTimeout()
        this.reconnectCount = 0
      }
      //连接关闭的回调方法
      this.socket.onclose = (event) => {
        console.log('WebSocket Connection Closed:', event)
        this.handleClose()
      }
      //连接发生错误的回调方法
      this.socket.onerror = (error) => {
        console.error('WebSocket Connection Error:', error)
        this.handleClose() //重连
      }
    }
  
    //断线重连操作
    handleClose() {
      if (this.reconnectCount < this.maxReconnectAttempts && (this.startTime === null || 
      Date.now() - this.startTime < this.maxReconnectTime)) {
        this.reconnectCount++
        console.log(`正在尝试重连 (${this.reconnectCount}/${this.maxReconnectAttempts})次...`)
        this.reconnectTimeout = setTimeout(() => {
          this.connect()
        }, this.reconnectInterval)
  
        if (this.startTime === null) {
          this.startTime = Date.now()
        }
      } else {
        console.log('超过最大重连次数或重连时间超时，已放弃连接！Max reconnect attempts reached or exceeded max reconnect time. Giving up.')
        this.reconnectCount = 0 // 重置连接次数0
        this.startTime = null // 重置开始时间
      }
    }
  
    //清除重连定时器
    clearReconnectTimeout() {
      if (this.reconnectTimeout) {
        clearTimeout(this.reconnectTimeout)
        this.reconnectTimeout = null
      }
    }
  
    //关闭连接
    close() {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.close()
      }
      this.clearReconnectTimeout()
      this.reconnectCount = 0
      this.startTime = null
    }
  }
  
  // WebSocketReconnect 类封装了WebSocket的连接、重连逻辑。
  // maxReconnectAttempts 是最大重连尝试次数。
  // reconnectInterval 是每次重连尝试之间的间隔时间。
  // maxReconnectTime 是总的重连时间限制，超过这个时间后不再尝试重连。
  // reconnectCount 用于记录已经尝试的重连次数。
  // startTime 用于记录开始重连的时间。
  // connect 方法用于建立WebSocket连接，并设置相应的事件监听器。
  // handleClose 方法在WebSocket连接关闭或发生错误时被调用，根据条件决定是否尝试重连。
  // clearReconnectTimeout 方法用于清除之前设置的重连定时器。
  // close 方法用于关闭WebSocket连接，并清除重连相关的状态。
  
  // 使用示例
  // const webSocketReconnect = new WebSocketReconnect('ws://your-websocket-url')
  // 当不再需要WebSocket连接时，可以调用close方法
  // webSocketReconnect.close();
  
  export default WebSocketReconnect
  
  