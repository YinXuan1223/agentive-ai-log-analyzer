<!-- <template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />
  </div>
</template> -->

<template>
  <div class="p-6 bg-white rounded-2xl shadow max-w-xl mx-auto space-y-4">
    <h2 class="text-xl font-bold text-gray-700">5G 網路狀況智慧助理</h2>

    <label class="block">
      <span class="text-sm text-gray-600">請輸入問題</span>
      <input v-model="question" type="text" class="input" placeholder="為什麼 throughput 下降？" />
    </label>

    <label class="block">
      <span class="text-sm text-gray-600">開始時間</span>
      <input v-model="startTime" type="datetime-local" class="input" />
    </label>

    <label class="block">
      <span class="text-sm text-gray-600">結束時間</span>
      <input v-model="endTime" type="datetime-local" class="input" />
    </label>

    <!-- button裡面的loading和下面的loading? '分析中' : '送出問題' 有關嗎 -->
    <button
      @click="askAgent"
      :disabled="loading" 
      class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-xl w-full"
    >
      {{ loading ? '分析中...' : '送出問題' }}
    </button>

    <div v-if="answer" class="mt-4 bg-gray-100 p-4 rounded">
      <strong class="block mb-2 text-gray-700">AI 回答：</strong>
      <p class="text-gray-800 whitespace-pre-wrap">{{ answer }}</p>
    </div>

    <button
      @click="checkLog" 
      class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-xl w-full"
    >
      查看 log 紀錄
    </button>
    

  </div>
</template>

<script setup>
import { ref } from 'vue'

const question = ref('') // v-model
const startTime = ref('')
const endTime = ref('')
const answer = ref('')
const loading = ref(false) // 按鈕是否在loading(能不能按)

const askAgent = async () => {
  loading.value = true
  answer.value = ''

  try {
    const res = await fetch('http://localhost:5000/api/ask', 
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: question.value,
          timestamp_range: [startTime.value, endTime.value]
        })
      }
    )

    const data = await res.json()
    answer.value = data.answer
  } 
  catch (error) {
    answer.value = '沒有連到lacalhost:5000'
  } 
  finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input {
  @apply mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:ring-blue-200;
}
</style>

