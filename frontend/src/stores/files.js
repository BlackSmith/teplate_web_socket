import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import {socket} from "@/socket.ts";
import jsonpatch from "json-patch";

export const useFilesStore = defineStore('files', () => {
  const files = ref({})
  // update files from public handler
  socket.client.on('files', (patch) => {
    files.value = jsonpatch.apply(files.value, patch);
  })

  // update files from private handler
  socket.pclient.on('files', (patch) => {
    files.value = jsonpatch.apply(files.value, patch);
  })
  return { files }
})
