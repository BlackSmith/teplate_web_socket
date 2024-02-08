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
    }
  }

}

</script>

<template>
  <input type="text" ref="msg">
  <button @click="ws_emit($refs.msg.value)">X</button>
  <h3>{{counter.count}}</h3>
  <RouterView />
</template>

<style scoped>

</style>
