<script lang="ts">
import {useCounterStore} from '@/stores/counter'

export default {
  setup() {
    let counter = useCounterStore();
    return {counter}
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
      this.$socket.client.emit("topic", msg);
    },
    admin_emit(msg) {
      console.info('admin emit: ' + msg)
      this.$socket.userLogin('admin', 'passwd')
      this.$socket.user.emit("reset", msg);
    }
  }

}

</script>

<template>
  <input type="text" ref="msg">
  <button @click="ws_emit($refs.msg.value)">X</button>
  <button @click="admin_emit($refs.msg.value)">A</button>
  <h3>{{counter.count}}</h3>
  <RouterView />
</template>

<style scoped>

</style>
