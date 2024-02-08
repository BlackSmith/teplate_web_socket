import {Manager} from "socket.io-client";

const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';

class WebSocketService {
  pingTimeout = null;
  client = null;
  manager = null;
  engine = null;

  constructor() {
    this.connect()
  }

  install(Vue) {
    const version = Number(Vue.version.split('.')[0])
    if (version >= 3) {
      Vue.config.globalProperties.$socket = this;
    } else {
      Vue.prototype.$socket = this;
    }
    console.info('WebSocketService plugin is enabled');
  }

  connect() {
    if (this.client && typeof this.client === 'object') {
      return
    }
    this.manager = new Manager();
    this.client = this.manager.socket('/');

    this.engine

    this.client.on('connect', () => {
      console.info('Socket connected: '+ this.client.connected);
      this.engine = this.client.io.engine;

      this.engine.once("upgrade", () => {
        console.log("Socket upgrade: ", this.engine.transport.name);
      });
    });

    this.client.on('disconnect', (reason) => {
      // clearTimeout(this.pingTimeout);
      console.info('Socket disconnected: ' + reason);
    });

    this.client.on("connect_error", () => {
      console.info('Socket connect error.');
      setTimeout(() => {
        this.client.connect();
      }, 1000);
    });

    this.client.on("topic2", (data) => {
      console.info(data);
    });
  }
}


export const socket = new WebSocketService()
