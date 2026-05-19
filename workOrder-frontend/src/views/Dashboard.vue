<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useWorkOrdersStore } from '@/stores/workorders'

const authStore = useAuthStore()
const workOrdersStore = useWorkOrdersStore()

onMounted(async () => { if (authStore.isAuthenticated) await workOrdersStore.loadWorkOrders() })

const statusConfig = {
  open:        { color: 'blue-darken-1' },
  in_progress: { color: 'orange-darken-2' },
  closed:      { color: 'green-darken-2' },
  cancelled:   { color: 'red-darken-2' },
}

const priorityConfig = {
  high:   { color: 'green' },
  medium: { color: 'blue-grey' },
  low:    { color: 'grey' },
}

const todayFormatted = computed(() =>
  new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'long', day: 'numeric', year: 'numeric' })
)

const roleLabel = computed(() => {
  if (authStore.isAdmin) return 'Administrator'
  if (authStore.isSupervisor) return 'Supervisor'
  return 'Technician'
})

const dashboardTitle = computed(() => {
  if (authStore.isAdmin) return 'Admin Dashboard'
  if (authStore.isSupervisor) return 'Supervisor Dashboard'
  return 'My Dashboard'
})

const dashboardSubtitle = computed(() => {
  if (authStore.isAdmin) return `Welcome back, ${authStore.userName}. Here's your system overview.`
  if (authStore.isSupervisor) return `Welcome back, ${authStore.userName}. Manage your team's work orders.`
  return `Welcome back, ${authStore.userName}. Here are your assigned tasks.`
})

const stats = computed(() => workOrdersStore.stats)
const recentWorkOrders = computed(() => workOrdersStore.recentWorkOrders)

const myWorkOrders = computed(() => {
  const userId = authStore.user?.id
  const userName = authStore.userName
  return workOrdersStore.workOrders.filter(wo =>
    wo.assignedToId === userId || wo.assignedTo === userName
  )
})

const myOrdersCount     = computed(() => myWorkOrders.value.length)
const myOpenCount       = computed(() => myWorkOrders.value.filter(wo => wo.status === 'open').length)
const myInProgressCount = computed(() => myWorkOrders.value.filter(wo => wo.status === 'in_progress').length)
const myCompletedCount  = computed(() => myWorkOrders.value.filter(wo => wo.status === 'closed').length)

const urgentOrders = computed(() => {
  const list = authStore.isTechnician ? myWorkOrders.value : workOrdersStore.workOrders
  return list
    .filter(wo => wo.status !== 'closed' && wo.status !== 'cancelled')
    .filter(wo => isOverdue(wo.dueDate) || isDueSoon(wo.dueDate))
    .slice(0, 3)
})

const unassignedCount = computed(() =>
  workOrdersStore.workOrders.filter(wo => wo.assignedTo === 'Unassigned').length
)

const dueThisWeekCount = computed(() => {
  const today = new Date()
  const nextWeek = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000)
  return workOrdersStore.workOrders.filter(wo => {
    const due = new Date(wo.dueDate)
    return due >= today && due <= nextWeek && wo.status !== 'closed'
  }).length
})

function pct(val, total) {
  if (!total) return 0
  return Math.round((val / total) * 100)
}

const adminStats = computed(() => [
  { label: 'Total work orders', value: stats.value.total,      cardColor: 'white', cardClass: '',                textColor: 'text-dark', barColor: '#D4E97D', pct: 100 },
  { label: 'Open',              value: stats.value.open,        cardColor: '#D4E97D', cardClass: 'white--text',   textColor: '#064229', barColor: '#064229', pct: pct(stats.value.open, stats.value.total) },
  { label: 'In progress',       value: stats.value.inProgress,  cardColor: 'white', cardClass: '',                textColor: 'text-orange-darken-2', barColor: '#F4A430', pct: pct(stats.value.inProgress, stats.value.total) },
  { label: 'Closed',            value: stats.value.closed,      cardColor: 'white', cardClass: '',                textColor: 'text-green-darken-2', barColor: '#5EC95A', pct: pct(stats.value.closed, stats.value.total) },
])

const supervisorStats = computed(() => [
  { label: 'Total orders',        value: stats.value.total,      cardColor: 'white', cardClass: '',                textColor: 'text-dark', barColor: '#D4E97D', pct: 100 },
  { label: 'Awaiting assignment', value: unassignedCount.value,  cardColor: '#D4E97D', cardClass: 'white--text',   textColor: '#064229', barColor: '#064229', pct: pct(unassignedCount.value, stats.value.total) },
  { label: 'In progress',         value: stats.value.inProgress, cardColor: 'white', cardClass: '',                textColor: 'text-orange-darken-2', barColor: '#F4A430', pct: pct(stats.value.inProgress, stats.value.total) },
  { label: 'Due this week',       value: dueThisWeekCount.value, cardColor: 'red-lighten-5', cardClass: '',        textColor: 'text-red-darken-2', barColor: '#E05040', pct: pct(dueThisWeekCount.value, stats.value.total) },
])

const technicianStats = computed(() => [
  { label: 'Assigned to me', value: myOrdersCount.value,     cardColor: 'white', cardClass: '',                textColor: 'text-dark', barColor: '#D4E97D', pct: 100 },
  { label: 'My open tasks',  value: myOpenCount.value,       cardColor: '#D4E97D', cardClass: 'white--text',   textColor: '#064229', barColor: '#064229', pct: pct(myOpenCount.value, myOrdersCount.value) },
  { label: 'In progress',    value: myInProgressCount.value, cardColor: 'white', cardClass: '',                textColor: 'text-orange-darken-2', barColor: '#F4A430', pct: pct(myInProgressCount.value, myOrdersCount.value) },
  { label: 'Completed',      value: myCompletedCount.value,  cardColor: 'white', cardClass: '',                textColor: 'text-green-darken-2', barColor: '#5EC95A', pct: pct(myCompletedCount.value, myOrdersCount.value) },
])

const headers = [
  { title: 'ID',          key: 'id',         sortable: true, width: '15%' },
  { title: 'Title',       key: 'title',      sortable: true, width: '45%' },
  { title: 'Assigned',    key: 'assignedTo', sortable: true, width: '25%', class: 'hidden-xs' },
  { title: 'Status',      key: 'status',     sortable: true, width: '15%', class: 'hidden-sm-and-down' },
  { title: '',            key: 'actions',    sortable: false, align: 'end' },
]

const techHeaders = [
  { title: 'ID',       key: 'id',       sortable: true, width: '15%' },
  { title: 'Title',    key: 'title',    sortable: true, width: '50%' },
  { title: 'Site',     key: 'site',     sortable: true, width: '20%', class: 'hidden-xs' },
  { title: 'Status',   key: 'status',   sortable: true, width: '15%' },
  { title: '',         key: 'actions',  sortable: false, align: 'end' },
]

function formatStatus(status) { return status.replace('_', ' ') }

// Fix: Append T00:00:00 to avoid timezone shifts for YYYY-MM-DD strings
function formatDate(dateString) {
  if (!dateString) return '—'
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function isOverdue(dateString) {
  if (!dateString) return false
  const due = new Date(dateString + 'T00:00:00')
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return due < today
}

function isDueSoon(dateString) {
  if (!dateString) return false
  const due = new Date(dateString + 'T00:00:00')
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const threeDaysOut = new Date(today.getTime() + 3 * 24 * 60 * 60 * 1000)
  return due >= today && due <= threeDaysOut
}

function startWork(orderId) {
  workOrdersStore.updateStatus(orderId, 'in_progress')
}
</script>

<template>
  <div>
    <!-- Brand Stripe -->
    <v-sheet height="4" color="transparent" class="brand-stripe">
      <v-sheet height="4" color="#064229" class="w-100"></v-sheet>
    </v-sheet>

    <v-container fluid class="pa-6 pa-md-8" style="max-width: 1005px;">
      <!-- Page Header -->
      <div class="mb-8">
        <div class="d-flex flex-column flex-sm-row align-start justify-space-between ga-4 mb-6">
          <div class="d-flex align-center">
            <v-icon icon="mdi-circle" size="8" color="#D4E97D" class="me-2"></v-icon>
            <span class="font-weight-bold text-uppercase" style="color: #064229; letter-spacing: 0.1em;">
              {{ roleLabel }}
            </span>
          </div>
          <v-chip variant="tonal" color="#064229" size="small">
            {{ todayFormatted }}
          </v-chip>
        </div>

        <div class="text-center text-md-left">
          <h1 class="font-weight-bold" style="color: #064229;">{{ dashboardTitle }}</h1>
          <p style="color: #064229; opacity: 0.8;">{{ dashboardSubtitle }}</p>
        </div>
      </div>

      <!-- ADMIN DASHBOARD -->
      <template v-if="authStore.isAdmin">
        <!-- Stat Cards -->
        <v-row dense class="mb-6">
          <v-col v-for="(stat, i) in adminStats" :key="i" cols="12" sm="6" md="3">
            <v-card :color="stat.cardColor" :class="stat.cardClass" rounded="lg" elevation="0" class="pa-5">
              <div class="font-weight-bold text-uppercase" style="color: #064229; letter-spacing: 0.07em;">
                {{ stat.label }}
              </div>
              <div class="font-weight-bold mt-2" :class="stat.textColor">
                {{ stat.value }}
              </div>
              <v-progress-linear
                :model-value="stat.pct"
                :color="stat.barColor"
                bg-color="transparent"
                rounded
                height="3"
                class="mt-4"
              />
            </v-card>
          </v-col>
        </v-row>

        <!-- Main Content -->
        <v-row>
          <!-- Orders Table -->
          <v-col cols="12" md="8">
            <v-card rounded="lg" elevation="0" style="border: 1px solid #e2e0d8;">
              <v-card-title class="d-flex align-center justify-space-between px-6 py-4" style="background: #f9f8f4;">
                <span class="font-weight-bold" style="color: #064229;">Recent Work Orders</span>
              </v-card-title>              <v-divider style="border-color: #eeece4;"></v-divider>
              <v-data-table
                :headers="headers"
                :items="recentWorkOrders"
                :items-per-page="5"
                hover
                class="dash-table"
              >
                <template v-slot:item.id="{ item }">
                  <router-link :to="`/work-orders/${item.id}`" class="text-decoration-none font-weight-bold px-2 py-1 rounded" style="color: #064229; background: #edf5e8; border: 1px solid #c8ddc0; font-family: monospace; font-size: 11px;">
                    {{ item.id }}
                  </router-link>
                </template>
                <template v-slot:item.title="{ item }">
                  <div class="text-truncate" style="max-width: 150px;">{{ item.title }}</div>
                </template>
                <template v-slot:item.status="{ item }">
                  <v-chip :color="statusConfig[item.status]?.color" size="x-small" variant="tonal" class="text-capitalize font-weight-medium" label>
                    {{ formatStatus(item.status) }}
                  </v-chip>
                </template>
                <template v-slot:item.priority="{ item }">
                  <v-chip :color="priorityConfig[item.priority]?.color" size="x-small" variant="tonal" class="text-capitalize font-weight-medium" label>
                    {{ item.priority }}
                  </v-chip>
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn variant="tonal" size="x-small" icon="mdi-eye" :to="`/work-orders/${item.id}`" color="#064229" rounded="lg"></v-btn>
                </template>
              </v-data-table>
            </v-card>
          </v-col>

          <!-- Side Panel -->
          <v-col cols="12" md="4">
            <v-card v-if="urgentOrders.length > 0" rounded="lg" elevation="0" class="pa-5 mb-4" style="background: #fff8f5; border: 1px solid #f0c0b0;">
              <div class="d-flex align-center mb-3">
                <v-icon icon="mdi-alert-circle" color="error" size="18" class="me-2"></v-icon>
                <span class="font-weight-bold" style="color: #b83020;">Urgent — System wide</span>
              </div>
              <v-list density="compact" bg-color="transparent" class="pa-0">
                <v-list-item v-for="order in urgentOrders" :key="order.id" :to="`/work-orders/${order.id}`" rounded="lg" class="mb-2 px-3" style="border: 1px solid #f0c0b0; background: white;">
                  <template v-slot:title>
                    <span class="font-weight-bold" style="color: #064229;">{{ order.id }}</span>
                    <span class="text-caption ms-2" style="color: #6b7c6b;">{{ order.assignedTo }}</span>
                  </template>
                  <template v-slot:subtitle>
                    <div class="text-truncate" style="max-width: 100%;">{{ order.title }}</div>
                    <div class="font-weight-bold" :class="isOverdue(order.dueDate) ? 'text-error' : 'text-orange-darken-3'">
                      Due: {{ formatDate(order.dueDate) }}
                    </div>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>

            <v-card rounded="lg" elevation="0" class="pa-5 mb-4" style="border: 1px solid #e2e0d8;">
              <div class="font-weight-bold mb-4" style="color: #064229;">Admin actions</div>
              <v-btn color="#064229" variant="flat" to="/work-orders/new" prepend-icon="mdi-plus" block rounded="lg" class="mb-2" style="color: #D4E97D;">
                New work order
              </v-btn>
              <v-btn variant="outlined" to="/work-orders" prepend-icon="mdi-format-list-bulleted" block rounded="lg" color="#064229" class="mb-2">
                Manage orders
              </v-btn>
              <v-btn variant="outlined" to="/users" prepend-icon="mdi-account-cog" block rounded="lg" color="#064229">
                User management
              </v-btn>
            </v-card>

            <v-card rounded="lg" elevation="0" class="pa-5" style="border: 1px solid #064229;">
              <div class="font-weight-bold text-uppercase mb-1" style="color: #064229;">Access level</div>
              <div class="font-weight-bold mb-2" style="color: #064229;">(Full Admin)</div>
              <p class="text-decoration-none" style="color: #064229;">
                Manage all work orders, users, and system configuration.
              </p>
            </v-card>
          </v-col>
        </v-row>
      </template>

      <!-- SUPERVISOR DASHBOARD -->
      <template v-else-if="authStore.isSupervisor">
        <v-row dense class="mb-6">
          <v-col v-for="(stat, i) in supervisorStats" :key="i" cols="12" sm="6" md="3">
            <v-card :color="stat.cardColor" :class="stat.cardClass" rounded="lg" elevation="0" class="pa-5">
              <div class="font-weight-bold text-uppercase" style="color: #064229; letter-spacing: 0.07em;">
                {{ stat.label }}
              </div>
              <div class="font-weight-bold mt-2" :class="stat.textColor">
                {{ stat.value }}
              </div>
              <v-progress-linear
                :model-value="stat.pct"
                :color="stat.barColor"
                bg-color="transparent"
                rounded
                height="3"
                class="mt-4"
              />
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="8">
            <v-card rounded="lg" elevation="0" style="border: 1px solid #e2e0d8;">
              <v-card-title class="d-flex align-center justify-space-between px-6 py-4" style="background: #f9f8f4;">
                <span class="font-weight-bold" style="color: #064229;">Team Work Orders</span>
              </v-card-title>
              <v-divider style="border-color: #eeece4;"></v-divider>
              <v-data-table
                :headers="headers"
                :items="recentWorkOrders"
                :items-per-page="5"
                hover
                class="dash-table"
              >
                <template v-slot:item.id="{ item }">
                  <router-link :to="`/work-orders/${item.id}`" class="text-decoration-none font-weight-bold px-2 py-1 rounded" style="color: #064229; background: #edf5e8; border: 1px solid #c8ddc0; font-family: monospace; font-size: 11px;">
                    {{ item.id }}
                  </router-link>
                </template>
                <template v-slot:item.title="{ item }">
                  <div class="text-truncate" style="max-width: 150px;">{{ item.title }}</div>
                </template>
                <template v-slot:item.status="{ item }">
                  <v-chip :color="statusConfig[item.status]?.color" size="x-small" variant="tonal" class="text-capitalize font-weight-medium" label>
                    {{ formatStatus(item.status) }}
                  </v-chip>
                </template>
                <template v-slot:item.priority="{ item }">
                  <v-chip :color="priorityConfig[item.priority]?.color" size="x-small" variant="tonal" class="text-capitalize font-weight-medium" label>
                    {{ item.priority }}
                  </v-chip>
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn variant="tonal" size="x-small" icon="mdi-eye" :to="`/work-orders/${item.id}`" color="#064229" rounded="lg"></v-btn>
                </template>
              </v-data-table>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card v-if="urgentOrders.length > 0" rounded="lg" elevation="0" class="pa-5 mb-4" style="background: #fff8f5; border: 1px solid #f0c0b0;">
              <div class="d-flex align-center mb-3">
                <v-icon icon="mdi-alert-circle" color="error" size="18" class="me-2"></v-icon>
                <span class="font-weight-bold" style="color: #b83020;">Urgent — Team alerts</span>
              </div>
              <v-list density="compact" bg-color="transparent" class="pa-0">
                <v-list-item v-for="order in urgentOrders" :key="order.id" :to="`/work-orders/${order.id}`" rounded="lg" class="mb-2 px-3" style="border: 1px solid #f0c0b0; background: white;">
                  <template v-slot:title>
                    <span class="font-weight-bold" style="color: #064229;">{{ order.id }}</span>
                    <span class="text-caption ms-2" style="color: #6b7c6b;">{{ order.assignedTo }}</span>
                  </template>
                  <template v-slot:subtitle>
                    <div class="text-truncate" style="max-width: 100%;">{{ order.title }}</div>
                    <div class="font-weight-bold" :class="isOverdue(order.dueDate) ? 'text-error' : 'text-orange-darken-3'">
                      Due: {{ formatDate(order.dueDate) }}
                    </div>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>

            <v-card rounded="lg" elevation="0" class="pa-5 mb-4" style="border: 1px solid #e2e0d8;">
              <div class="font-weight-bold mb-4" style="color: #064229;">Supervisor actions</div>
              <v-btn color="#064229" variant="flat" to="/work-orders/new" prepend-icon="mdi-plus" block rounded="lg" class="mb-2" style="color: #D4E97D;">
                Create & Assign
              </v-btn>
              <v-btn variant="outlined" to="/work-orders" prepend-icon="mdi-account-group" block rounded="lg" color="#064229">
                Team Overview
              </v-btn>
            </v-card>
            <v-card rounded="lg" elevation="0" class="pa-5" style="border: 1px solid #064229;">
              <div class="font-weight-bold text-uppercase mb-1" style="color: #064229;">Access level</div>
              <div class="font-weight-bold mb-2" style="color: #064229;">(Supervisor)</div>
              <p class="text-decoration-none" style="color: #064229;">Create orders, assign to technicians, and monitor team progress.</p>
            </v-card>
          </v-col>
        </v-row>
      </template>

      <!-- TECHNICIAN DASHBOARD -->
      <template v-else-if="authStore.isTechnician">
        <v-row dense class="mb-6">
          <v-col v-for="(stat, i) in technicianStats" :key="i" cols="12" sm="6" md="3">
            <v-card :color="stat.cardColor" :class="stat.cardClass" rounded="lg" elevation="0" class="pa-5">
              <div class="font-weight-bold text-uppercase" style="color: #064229; letter-spacing: 0.07em;">
                {{ stat.label }}
              </div>
              <div class="font-weight-bold mt-2" :class="stat.textColor">
                {{ stat.value }}
              </div>
              <v-progress-linear
                :model-value="stat.pct"
                :color="stat.barColor"
                bg-color="transparent"
                rounded
                height="3"
                class="mt-4"
              />
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="8">
            <v-card rounded="lg" elevation="0" style="border: 1px solid #e2e0d8;">
              <v-card-title class="d-flex align-center justify-space-between px-6 py-4" style="background: #f9f8f4;">
                <span class="font-weight-bold" style="color: #064229;">My assigned Work Orders</span>
              </v-card-title>
              <v-divider style="border-color: #eeece4;"></v-divider>
              <v-data-table
                :headers="techHeaders"
                :items="myWorkOrders"
                :items-per-page="5"
                hide-default-footer
                hover
                class="dash-table"
              >
                <template v-slot:item.id="{ item }">
                  <router-link :to="`/work-orders/${item.id}`" class="text-decoration-none font-weight-bold px-2 py-1 rounded" style="color: #064229; background: #edf5e8; border: 1px solid #c8ddc0; font-family: monospace; font-size: 11px;">
                    {{ item.id }}
                  </router-link>
                </template>
                <template v-slot:item.status="{ item }">
                  <v-chip :color="statusConfig[item.status]?.color" size="x-small" variant="tonal" class="text-capitalize font-weight-medium" label>
                    {{ formatStatus(item.status) }}
                  </v-chip>
                </template>
                <template v-slot:item.priority="{ item }">
                  <v-chip :color="priorityConfig[item.priority]?.color" size="x-small" variant="tonal" class="text-capitalize font-weight-medium" label>
                    {{ item.priority }}
                  </v-chip>
                </template>
                <template v-slot:item.dueDate="{ item }">
                  <span :style="isOverdue(item.dueDate) ? 'color: #b83020; font-weight: 700;' : 'color: #6a7a6a;'">
                    {{ formatDate(item.dueDate) }}
                  </span>
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn v-if="item.status === 'open'" color="warning" variant="flat" size="x-small" rounded="lg" @click="startWork(item.id)">Start</v-btn>
                  <v-btn v-else-if="item.status === 'in_progress'" color="#064229" variant="flat" size="x-small" rounded="lg" :to="`/work-orders/${item.id}`" style="color: #D4E97D;">Complete</v-btn>
                  <v-btn v-else variant="tonal" size="x-small" icon="mdi-eye" :to="`/work-orders/${item.id}`" color="#064229" rounded="lg"></v-btn>
                </template>
              </v-data-table>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card v-if="urgentOrders.length > 0" rounded="lg" elevation="0" class="pa-5 mb-4" style="background: #fff8f5; border: 1px solid #f0c0b0;">
              <div class="d-flex align-center mb-3">
                <v-icon icon="mdi-alert-circle" color="error" size="18" class="me-2"></v-icon>
                <span class="font-weight-bold" style="color: #b83020;">Urgent — due soon</span>
              </div>
              <v-list density="compact" bg-color="transparent" class="pa-0">
                <v-list-item v-for="order in urgentOrders" :key="order.id" :to="`/work-orders/${order.id}`" rounded="lg" class="mb-2 px-3" style="border: 1px solid #f0c0b0; background: white;">
                  <template v-slot:title>
                    <span class="font-weight-bold" style="color: #2a2a2a;">{{ order.id }} — {{ order.title }}</span>
                  </template>
                  <template v-slot:subtitle>
                    <span class="font-weight-bold" :class="isOverdue(order.dueDate) ? 'text-error' : 'text-orange-darken-3'">
                      Due {{ formatDate(order.dueDate) }}
                    </span>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>

            <v-card rounded="lg" elevation="0" class="pa-5" style="border: 1px solid #064229;">
              <div class="font-weight-bold text-uppercase mb-1" style="color: #064229;">Access level</div>
              <div class="font-weight-bold mb-2" style="color: #064229;">(Technician)</div>
              <p class="text-decoration-none" style="color: #064229;">View and update orders assigned to you. Mark tasks complete.</p>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-container>
  </div>
</template>

<style scoped>
.dash-table :deep(th) {
  text-transform: uppercase;
  font-size: 0.7rem !important;
  font-weight: 700 !important;
  color: #6b7c6b !important;
  letter-spacing: 0.05em;
}

@media (max-width: 600px) {
  :deep(.hidden-xs) {
    display: none !important;
  }
}

@media (max-width: 960px) {
  :deep(.hidden-sm-and-down) {
    display: none !important;
  }
}

.text-lime {
  color: #D4E97D !important;
}
.text-dark {
  color: #064229 !important;
}
</style>