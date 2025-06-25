<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <h1 class="text-3xl font-bold mb-8 text-center">流量监控</h1>
    
    <!-- 实时协议统计 -->
    <div class="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">实时协议统计</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div 
          v-for="(stats, protocol) in filteredProtocols" 
          :key="protocol"
          class="border rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <h3 class="font-medium capitalize">{{ protocol }}</h3>
          <div class="mt-2 text-sm text-gray-600">
            <p>数据包: {{ stats.packets.toLocaleString() }}</p>
            <p>流量: {{ formatBytes(stats.bytes) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- 历史数据图表 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">历史流量趋势</h2>
        <div class="h-64">
          <canvas ref="lineChart"></canvas>
        </div>
        
      </div>
      
      <!-- 流量占比饼图 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">流量占比分布</h2>
        <div class="h-64">
          <canvas ref="pieChart"></canvas>
        </div>
      </div>
    </div>
    
    <div class="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4">最新数据包摘要</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">时间</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">交换机</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">入端口</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">源MAC</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">目的MAC</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">源IP</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">目的IP</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">源端口</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">目的端口</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">协议</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">长度</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="packet in packetSummaries" :key="packet.timestamp + '-' + packet.packet_len + '-' + packet.eth_src"
                :style="{ backgroundColor: getProtocolColor(packet.protocol_identified, 0.05) }"
            >
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-800">{{ formatPacketTime(packet.timestamp) }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-600">{{ packet.dpid }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-600">{{ packet.in_port }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-800">{{ packet.eth_src || 'N/A' }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-800">{{ packet.eth_dst || 'N/A' }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-600">{{ packet.ip_src || 'N/A' }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-600">{{ packet.ip_dst || 'N/A' }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-600">{{ packet.src_port || 'N/A' }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-600">{{ packet.dst_port || 'N/A' }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm font-medium capitalize">{{ packet.protocol_identified || 'N/A' }}</td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-600">{{ formatBytes(packet.packet_len) }}</td>
            </tr>
            <tr v-if="packetSummaries.length === 0">
                <td colspan="11" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">
                    暂无数据包摘要。请确保流量正在通过网络。
                </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, onBeforeUnmount, computed, watch } from 'vue'
import { Chart, registerables } from 'chart.js'

// 只在客户端导入
if (process.client) {
  Chart.register(...registerables)
}

interface ProtocolStats {
  packets: number
  bytes: number
}

interface ProtocolData {
  [key: string]: ProtocolStats
}

interface HistoryRecord {
  timestamp: number
  data: ProtocolData
}

interface PacketSummary {
  timestamp: number
  dpid: number
  in_port: number
  eth_src: string
  eth_dst: string
  eth_type: string
  ip_src: string | null
  ip_dst: string | null
  ip_proto: number | null
  src_port: number | null
  dst_port: number | null
  packet_len: number
  protocol_identified: string
}

// 响应式数据
const protocolData = ref<ProtocolData>({})
const localHistory = ref<HistoryRecord[]>([])
const packetSummaries = ref<PacketSummary[]>([])
const loading = ref(true)
const error = ref('')
const lineChart = ref<HTMLCanvasElement | null>(null)
const pieChart = ref<HTMLCanvasElement | null>(null)
const timeRange = ref<'5m' | '15m' | '30m' | '1h'>('15m')
let lineChartInstance: Chart | null = null
let pieChartInstance: Chart | null = null
let refreshInterval: NodeJS.Timeout | null = null

// 过滤掉不需要显示的协议
const filteredProtocols = computed(() => {
  const { dns, other, ...rest } = protocolData.value
  return rest
})

// 计算总流量用于饼图
const totalTraffic = computed(() => {
  return Object.values(filteredProtocols.value).reduce((sum, stats) => sum + stats.bytes, 0)
})

// 根据时间范围筛选历史数据
const filteredHistory = computed(() => {
  const now = Math.floor(Date.now() / 1000)
  let seconds: number
  
  switch (timeRange.value) {
    case '5m': seconds = 300; break
    case '15m': seconds = 900; break
    case '30m': seconds = 1800; break
    case '1h': seconds = 3600; break
    default: seconds = 900
  }
  
  return localHistory.value.filter(record => 
    record.timestamp >= now - seconds
  )
})

// 格式化字节大小
const formatBytes = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化时间
const formatTime = (timestamp: number) => {
  const date = new Date(timestamp * 1000)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// 新增：格式化数据包摘要时间（精确到秒）
const formatPacketTime = (timestamp: number) => {
  const date = new Date(timestamp * 1000)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

// 协议颜色映射
const getProtocolColor = (protocol: string, opacity = 1) => {
  const colors: Record<string, string> = {
    http: `rgba(75, 192, 192, ${opacity})`,
    https: `rgba(54, 162, 235, ${opacity})`,
    ftp: `rgba(255, 159, 64, ${opacity})`,
    smtp: `rgba(153, 102, 255, ${opacity})`,
    pop3: `rgba(255, 99, 132, ${opacity})`,
    imap: `rgba(255, 205, 86, ${opacity})`
  }
  return colors[protocol] || `rgba(199, 199, 199, ${opacity})`
}

// 初始化折线图
const initLineChart = () => {
  if (!lineChart.value) return
  
  // 销毁旧图表实例
  if (lineChartInstance) {
    lineChartInstance.destroy()
  }
  
  const ctx = lineChart.value.getContext('2d')
  if (!ctx) return
  
  // 获取所有协议类型
  const protocols = Object.keys(filteredProtocols.value)
  
  lineChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: filteredHistory.value.map(record => formatTime(record.timestamp)),
      datasets: protocols.map(protocol => ({
        label: protocol,
        data: filteredHistory.value.map(record => record.data[protocol]?.bytes || 0),
        borderColor: getProtocolColor(protocol),
        backgroundColor: getProtocolColor(protocol, 0.1),
        tension: 0.1,
        fill: true
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.dataset.label || ''
              const value = context.raw as number
              return `${label}: ${formatBytes(value)}`
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => formatBytes(Number(value))
          }
        }
      }
    }
  })
}

// 初始化饼图
const initPieChart = () => {
  if (!pieChart.value) return
  
  // 销毁旧图表实例
  if (pieChartInstance) {
    pieChartInstance.destroy()
  }
  
  const ctx = pieChart.value.getContext('2d')
  if (!ctx) return
  
  const protocols = Object.keys(filteredProtocols.value)
  const trafficData = protocols.map(protocol => filteredProtocols.value[protocol].bytes)
  
  pieChartInstance = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: protocols,
      datasets: [{
        data: trafficData,
        backgroundColor: protocols.map(p => getProtocolColor(p)),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.label || ''
              const value = context.raw as number
              const percentage = Math.round((value / totalTraffic.value) * 100)
              return `${label}: ${formatBytes(value)} (${percentage}%)`
            }
          }
        }
      }
    }
  })
}

// 改变时间范围
const changeTimeRange = (range: '5m' | '15m' | '30m' | '1h') => {
  timeRange.value = range
}

// 获取协议数据
const fetchProtocolStats = async () => {
  try {
    const response = await fetch('/api/stats/protocol')
    if (!response.ok) throw new Error('获取协议数据失败')
    const data = await response.json()
    
    // 更新当前协议数据
    protocolData.value = data.protocols
    
    // 添加新记录到本地历史数据
    const now = Math.floor(Date.now() / 1000)
    localHistory.value.push({
      timestamp: now,
      data: { ...data.protocols } // 深拷贝防止引用问题
    })
    
    // 限制历史数据数量，避免内存问题
    if (localHistory.value.length > 120) { // 最多保存120个点(2小时数据，每分钟一个点)
      localHistory.value.shift()
    }
    
    // 更新图表
    await nextTick()
    initLineChart()
    initPieChart()
  } catch (e) {
    error.value = '获取协议数据失败，请检查API服务状态'
    console.error('API请求错误:', e)
  } finally {
    loading.value = false
  }
}

// 新增：获取数据包摘要
const fetchPacketSummaries = async () => {
  try {
    const response = await fetch('/api/stats/packet_summaries')
    if (!response.ok) throw new Error(`获取数据包摘要失败: ${response.statusText}`)
    const data = await response.json()
    // 反转数组，确保最新数据在表格顶部显示
    packetSummaries.value = data.packet_summaries.reverse()
  } catch (e) {
    console.error('API请求错误 (数据包摘要):', e)
    // 可以在这里设置一个错误状态，如果需要显示给用户
  }
}

// 监听时间范围变化
watch(timeRange, () => {
  initLineChart()
})

// 组件挂载时获取数据
onMounted(() => {
  // Ensure running only on client side
  if (process.client) {
    // Initial fetches
    fetchProtocolStats()
    fetchPacketSummaries()

    // Set up refresh interval for both data types
    refreshInterval = setInterval(() => {
      fetchProtocolStats()
      fetchPacketSummaries()
    }, 5000) // Fetch data every 5 seconds
  }
})

// 组件卸载前清除定时器
onBeforeUnmount(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  if (lineChartInstance) {
    lineChartInstance.destroy()
  }
  if (pieChartInstance) {
    pieChartInstance.destroy()
  }
})
</script>
