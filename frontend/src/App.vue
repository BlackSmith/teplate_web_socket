<script lang="ts">
import {useFilesStore} from '@/stores/files'

export default {
  setup() {
    let files = useFilesStore();
    return {files}
  },
  data() {
    return {

    }
  },
  computed: {

  },
  mounted() {

  },
  methods: {
    ws_emit(msg) {
      console.info('emit: '+msg)
      // Sent to public entrypoint
      this.$socket.client.emit("topic", msg);
    },
    admin_login() {
      // Login user
      this.$socket.userLogin('admin', 'passwd')
    },
    admin_emit(msg)
      {
      console.info('admin emit: ' + msg)
      // Send to message to private entrypoint
      this.$socket.pclient.emit("private_topic", msg);
    }
  }

}

</script>

<template>
  <input type="text" ref="msg">
  <button @click="ws_emit($refs.msg.value)">public</button>
  <button @click="admin_login()">login</button>
  <button @click="admin_emit($refs.msg.value)">private</button>
  <h3>{{files.files}}</h3>

</template>

<style scoped>

</style>
