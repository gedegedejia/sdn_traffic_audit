<template>
  <div>
    <nav class="bg-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <NuxtLink to="/" class="text-xl font-bold text-gray-800">
                RYU Controller
              </NuxtLink>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <NuxtLink to="/" class="inline-flex items-center px-1 pt-1 text-gray-500 hover:text-gray-700">
                Home
              </NuxtLink>
              <NuxtLink to="/switches" class="inline-flex items-center px-1 pt-1 text-gray-500 hover:text-gray-700">
                Switches
              </NuxtLink>
              <NuxtLink to="/topology" class="inline-flex items-center px-1 pt-1 text-gray-500 hover:text-gray-700">
                Topology
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main>
      <slot />
    </main>
  </div>
</template> 