import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import {socket} from "@/socket.ts";
import jsonpatch from "json-patch";

export const useCounterStore = defineStore('counter', () => {
  const count = ref({})
  const doubleCount = computed(() => count.value * 2)
  socket.client.on('counter', (data) => {
    console.log(data)
    // console.warn(jsonpatch.apply(count.value, data))
    count.value = jsonpatch.apply(count.value, data);
  })
  function increment() {
    count.value++
  }

  return { count, doubleCount, increment }
})
