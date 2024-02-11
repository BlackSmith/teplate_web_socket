import {Manager} from "socket.io-client";


class WebSocketService {
  client = null;       //  socket for anonymous user
  pclient = null;      //  socket for logged user
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
    this.manager = new Manager(null, {
      transports: ["websocket", "webtransport"],
      autoConnect: false,
    });
    this.connect();
  }

  connect() {
    if (this.client && typeof this.client === 'object') {
      return
    }
    this.client = this.manager.socket('/');

    this.client.on('connect', () => {
      console.info('Public socket connected: '+ this.client.connected);
      this.client.io.engine.once("upgrade", () => {
        console.log(
            "Public socket upgrade to " + this.client.io.engine.transport.name
        );
      });
    });

    this.client.on('disconnect', (reason) => {
      console.info('Public socket disconnected: ' + reason);
      if (reason === "io server disconnect") {
        // the disconnection was initiated by the server,
        // need to reconnect manually
        this.client.connect();
      }
    });

    this.client.on("connect_error", () => {
      console.info('Public socket connect error.');
      setTimeout(() => {
        this.client.connect();
      }, 1000);
    });
    this.client.connect()

    // Private socket
    if (this.pclient && typeof this.pclient === 'object') {
      return
    }
    this.pclient = this.manager.socket('/private', {
      withCredentials: true,
      multiplex: false
    })

    this.pclient.on('connect', () => {
      console.info('Private socket connected: ' + this.pclient.connected);
      this.pclient.io.engine.once("upgrade", () => {
        console.log("Private socket upgrade to ", this.pclient.io.engine.transport.name);
      });
    });

    this.pclient.on('disconnect', (reason) => {
      console.info('Private socket disconnected: ' + reason);
    });

    this.pclient.on("connect_error", (reason) => {
      console.info('Private socket admin connect error. ' + reason);
    });
  }

  userLogin(username, password) {
    this.pclient.auth = { username: username, password: password }
    this.pclient.connect()
  }

  ispclientLogged() {
    return this.pclient.connected;
  }

}

export const socket = new WebSocketService()
