<template>
  <div class="min-h-screen bg-gray-100">
    <div class="container mx-auto px-4 py-8">
      <div class="mb-6">
        <NuxtLink to="/switches" class="text-blue-500 hover:text-blue-700">
          ← Back to Switches
        </NuxtLink>
      </div>

      <h1 class="text-3xl font-bold mb-8">Switch {{ route.params.id }}</h1>

      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>

      <div v-if="loading" class="flex justify-center items-center h-32">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>

      <div v-else>
        <!-- Switch Description -->
        <div class="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 class="text-xl font-semibold mb-4">Switch Description</h2>
          <div class="grid grid-cols-2 gap-4">
            <div v-for="(value, key) in description" :key="key" class="p-2">
              <span class="font-medium">{{ key }}:</span>
              <span class="ml-2">{{ value }}</span>
            </div>
          </div>
        </div>

        <!-- Flow Table -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-xl font-semibold mb-4">Flow Table</h2>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Match</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timeouts</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(flow, index) in flows" :key="index">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div v-for="(value, key) in flow.match" :key="key">
                      {{ key }}: {{ value }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    {{ flow.actions }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    {{ flow.priority }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div>Idle: {{ flow.idle_timeout }}</div>
                    <div>Hard: {{ flow.hard_timeout }}</div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Add Flow Form -->
        <div class="bg-white p-6 rounded-lg shadow-md mt-6">
          <h2 class="text-xl font-semibold mb-4">Add Flow Entry</h2>
          <form @submit.prevent="submitFlow" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Cookie</label>
                <input v-model="flowForm.cookie" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Priority</label>
                <input v-model="flowForm.priority" type="number" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Match In Port</label>
                <input v-model="flowForm.match.in_port" type="number" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Match Eth Dst</label>
                <input v-model="flowForm.match.eth_dst" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
              </div>
            </div>
            <div class="flex justify-end">
              <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
                Add Flow
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

const route = useRoute()
const config = useRuntimeConfig()
const flows = ref([])
const description = ref({})
const loading = ref(true)
const error = ref('')

const flowForm = ref({
  cookie: '',
  priority: 0,
  match: {
    in_port: '',
    eth_dst: ''
  }
})

const fetchSwitchData = async () => {
  try {
    const [flowResponse, descResponse] = await Promise.all([
      fetch(`/api/stats/flow/${route.params.id}`),
      fetch(`/api/stats/desc/${route.params.id}`)
    ])

    if (!flowResponse.ok || !descResponse.ok) {
      throw new Error('Failed to fetch switch data')
    }

    const flowData = await flowResponse.json()
    const descData = await descResponse.json()

    flows.value = flowData[route.params.id]
    description.value = descData[route.params.id]
  } catch (e) {
    error.value = 'Failed to fetch switch data. Please make sure the RYU controller is running.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

const submitFlow = async () => {
  try {
    const response = await fetch(`${config.public.ryuApiUrl}/stats/flowentry/add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        dpid: route.params.id,
        cookie: flowForm.value.cookie,
        priority: flowForm.value.priority,
        match: flowForm.value.match,
        actions: []
      })
    })

    if (!response.ok) {
      throw new Error('Failed to add flow entry')
    }

    await fetchSwitchData()
    flowForm.value = {
      cookie: '',
      priority: 0,
      match: {
        in_port: '',
        eth_dst: ''
      }
    }
  } catch (e) {
    error.value = 'Failed to add flow entry'
    console.error(e)
  }
}
onMounted(fetchSwitchData)
</script> 