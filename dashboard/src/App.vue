<script setup>
import { ref } from 'vue';
import { useHttpStore } from './stores/http.js';
import axios from 'axios';

const httpStore = useHttpStore();
const resultList = ref([]);

const baseWWW =
  location.origin.indexOf('us-east-1') !== -1
    ? 'https://www.disaster-us-east-1.thienlinh.link'
    : 'https://www.disaster-ap-southeast-1.thienlinh.link';

async function load() {
  const res = await httpStore.find('/list');
  resultList.value = res.map((item) => ({
    object: item.object.S,
    bucket: item.bucket.S,
    region: item.region.S,
    kind: item.kind.S,
    created: new Date(parseInt(item.created.S) * 1000).toISOString()
  }));
}

async function doUpload(e) {
  const file = e.target.files[0];

  const name = `uploads/${file.name}`;
  const fileReader = new FileReader();
  fileReader.readAsArrayBuffer(file);
  fileReader.onloadend = (e) => {};

  const res = await httpStore.create('/upload', {
    name,
    content_type: file.type
  });

  await axios.put(res, file, {
    headers: {
      'Content-Type': file.type
    },
    onUploadProgress: (e) => {
      const percentCompleted = Math.round((e.loaded * 100) / e.total);
      console.log(percentCompleted);
    }
  });

  e.target.value = null;
  alert(`Uploaded`);
  load();
}

load();

setInterval(() => load(), 5000);
</script>

<template>
  <div class="p-3 flex flex-wrap">
    <div class="w-1/4 p-3">
      <div class="bg-white p-6 rounded-lg flex items-center mb-6">
        <div class="w-1/2 pr-6">
          <img src="/disaster.png" alt="Disaster Logo" class="w-full h-auto" />
        </div>
        <h1 class="flex flex-col w-1/2 text-xl leading-[1.5em] font-black">
          <span>Disaster</span> <span>Classification</span> <span>System</span>
        </h1>
      </div>

      <input type="file" class="hidden" id="uploadFile" @change="doUpload" />

      <label
        for="uploadFile"
        class="bg-white p-6 rounded-lg w-full h-36 flex items-center justify-center"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="ionicon w-12 h-12"
          viewBox="0 0 512 512"
          fill="currentColor"
        >
          <path
            d="M473.66 210c-16.56-12.3-37.7-20.75-59.52-24-6.62-39.18-24.21-72.67-51.3-97.45-28.69-26.3-66.63-40.76-106.84-40.76-35.35 0-68 11.08-94.37 32.05a149.61 149.61 0 00-45.32 60.49c-29.94 4.6-57.12 16.68-77.39 34.55C13.46 197.33 0 227.24 0 261.39c0 34.52 14.49 66 40.79 88.76 25.12 21.69 58.94 33.64 95.21 33.64h104V230.42l-48 48-22.63-22.63L256 169.17l86.63 86.62L320 278.42l-48-48v153.37h124c31.34 0 59.91-8.8 80.45-24.77 23.26-18.1 35.55-44 35.55-74.83 0-29.94-13.26-55.61-38.34-74.19zM240 383.79h32v80.41h-32z"
          />
        </svg>
      </label>
    </div>

    <!-- <div class="w-1/4 p-3">
      <div class="bg-white p-6 rounded-lg">ok</div>
    </div> -->

    <div class="w-3/4 p-3">
      <div class="bg-white p-6 rounded-lg">
        <div class="relative overflow-x-auto">
          <table
            class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400"
          >
            <thead
              class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
            >
              <tr>
                <th scope="col" class="px-6 py-3">Object</th>
                <th scope="col" class="px-6 py-3">Bucket</th>
                <th scope="col" class="px-6 py-3">Region</th>
                <th scope="col" class="px-6 py-3">Kind</th>
                <th scope="col" class="px-6 py-3">Created</th>
              </tr>
            </thead>
            <tbody>
              <tr
                class="bg-white border-b dark:bg-gray-800 dark:border-gray-700"
                v-for="item in resultList"
              >
                <th
                  scope="row"
                  class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <a
                    :href="`${baseWWW}/${item.object}`"
                    target="_blank"
                    class="underline font-bold text-teal-700"
                  >
                    {{ item.object.split('/')[1] }}
                  </a>
                </th>
                <td class="px-6 py-4">{{ item.bucket }}</td>
                <td class="px-6 py-4">{{ item.region }}</td>
                <td class="px-6 py-4 text-rose-500">
                  {{ item.kind }}
                </td>
                <td class="px-6 py-4">{{ item.created }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="w-1/4 p-3"></div>
  </div>
</template>
