<template>
  <div class="min-h-screen bg-gray-100">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-8">网络交换机</h1>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>

      <div v-if="loading" class="flex justify-center items-center h-32">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="switchId in switches" :key="switchId" 
             class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-semibold mb-2">交换机 {{ switchId }}</h2>
          <NuxtLink :to="`/switches/${switchId}`" 
                   class="inline-block mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
            查看详情
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 响应式数据
const switches = ref<string[]>([]) // 交换机列表
const loading = ref(true)         // 加载状态
const error = ref('')             // 错误信息

// 组件挂载后获取数据
onMounted(async () => {
  try {
    const response = await fetch('/api/stats/switches')
    if (!response.ok) throw new Error('获取交换机列表失败')
    switches.value = await response.json()
  } catch (e) {
    error.value = '获取交换机列表失败，请确保RYU控制器正在运行'
    console.error('API请求错误:', e)
  } finally {
    loading.value = false
  }
})
</script>