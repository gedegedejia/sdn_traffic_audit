<template>
  <div class="min-h-screen bg-gray-100">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-center mb-8">RYU Controller Dashboard</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <NuxtLink to="/switches" class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-semibold mb-2">交换机管理</h2>
          <p class="text-gray-600">View and manage network switches</p>
        </NuxtLink>
        <NuxtLink to="/topology" class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-semibold mb-2">网络拓扑</h2>
          <p class="text-gray-600">View network topology and connections</p>
        </NuxtLink>
        <NuxtLink to="/statistics" class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-semibold mb-2">流量审计</h2>
          <p class="text-gray-600">View network statistics and monitoring</p>
        </NuxtLink>
      </div>
    </div>
  </div>
</template> 

<script></script>