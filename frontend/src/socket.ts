import {Manager} from "socket.io-client";


class WebSocketService {
  client = null;    //  anonymous user
  user = null;      //  logged user
  manager = null;

  install(Vue) {
    const version = Number(Vue.version.split('.')[0])
    if (version >= 3) {
      Vue.config.globalProperties.$socket = this;
    } else {
      Vue.prototype.$socket = this;
    }
    console.info('WebSocketService plugin is enabled');
  }

  constructor() {
    this.manager = new Manager();
    this.connect();
  }

  connect() {
    if (this.client && typeof this.client === 'object') {
      return
    }
    this.client = this.manager.socket('/');

    this.client.on('connect', () => {
      console.info('Socket connected: '+ this.client.connected);
      this.client.io.engine.once("upgrade", () => {
        console.log("Socket upgrade to ", this.client.io.engine.transport.name);
      });
    });

    this.client.on('disconnect', (reason) => {
      console.info('Socket disconnected: ' + reason);
    });

    this.client.on("connect_error", () => {
      console.info('Socket connect error.');
      setTimeout(() => {
        this.client.connect();
      }, 1000);
    });
  }

  userLogin(username, password) {
    if (this.user && typeof this.user === 'object') {
      return
    }
    this.user = this.manager.socket('/user', {
      withCredentials: true
    })
    this.user.auth = { username: username, password: password }

    this.user.on('connect', () => {
      console.info('Private socket connected: ' + this.user.connected);
      this.user.io.engine.once("upgrade", () => {
        console.log("Private socket upgrade to ", this.user.io.engine.transport.name);
      });
    });

    this.user.on('disconnect', (reason) => {
      console.info('Private socket disconnected: ' + reason);
      this.user = null;
    });

    this.user.on("connect_error", (reason) => {
      console.info('Private socket admin connect error. ' + reason );
      this.user = null;
    });
  }

  isUserLogged() {
    return this.user != null && this.user.connected;
  }

}

export const socket = new WebSocketService()
