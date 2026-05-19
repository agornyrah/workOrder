<template>
  <div>
    <!-- Brand Stripe -->
    <v-sheet height="4" color="#064229" class="w-100"></v-sheet>

    <v-container fluid class="pa-6 pa-md-8" style="max-width: 1005px;">
      <!-- Header -->
      <div class="d-flex align-start justify-space-between mb-8 flex-wrap gap-3">
        <div>
          <div class="d-flex align-center mb-2">
            <v-icon icon="mdi-circle" size="8" color="#D4E97D" class="me-2"></v-icon>
            <span class="text-caption font-weight-bold text-uppercase" style="color: #064229; letter-spacing: 0.1em;">
              {{ roleLabel }}
            </span>
          </div>
        </div>
        <v-chip variant="tonal" color="#064229" size="small" class="mt-1">
          {{ todayFormatted }}
        </v-chip>
      </div>

      <div class="text-center text-md-left">
        <h1 class="font-weight-bold" style="color: #064229;">{{ pageTitle }}</h1>
        <p class="mb-8" style="color: #6b7c6b;">{{ pageSubtitle }}</p>
      </div>

      <!-- Filters & Actions -->
      <v-card rounded="lg" elevation="0" class="mb-6" style="border: 1px solid #e2e0d8;">
        <v-card-text class="pa-4">
          <v-row dense align="center">
            <v-col cols="12" md="4" lg="3">
              <v-text-field
                v-model="searchQuery"
                label="Search orders..."
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="compact"
                hide-details
                clearable
                bg-color="white"
                rounded="lg"
              ></v-text-field>
            </v-col>
            
            <v-col cols="6" sm="4" md="2">
              <v-select
                v-model="filters.status"
                label="Status"
                :items="statusOptions"
                variant="outlined"
                density="compact"
                hide-details
                clearable
                bg-color="white"
                rounded="lg"
              ></v-select>
            </v-col>
            
            <v-col cols="6" sm="4" md="2">
              <v-select
                v-model="filters.priority"
                label="Priority"
                :items="priorityOptions"
                variant="outlined"
                density="compact"
                hide-details
                clearable
                bg-color="white"
                rounded="lg"
              ></v-select>
            </v-col>
            
            <v-col cols="12" sm="4" md="2">
              <v-select
                v-model="filters.site"
                label="Site"
                :items="siteOptions"
                variant="outlined"
                density="compact"
                hide-details
                clearable
                bg-color="white"
                rounded="lg"
              ></v-select>
            </v-col>
            
            <v-spacer class="hidden-sm-and-down"></v-spacer>

            <v-col
              v-if="authStore.isAdmin || authStore.isSupervisor"
              cols="12" md="auto"
              class="text-end"
            >
              <v-btn
                color="#064229"
                variant="flat"
                block
                to="/work-orders/new"
                prepend-icon="mdi-plus"
                rounded="lg"
                class="mt-2 mt-md-0"
                style="color: #D4E97D;"
              >
                New order
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Work Orders Table -->
      <v-card rounded="lg" elevation="0" style="border: 1px solid #e2e0d8;">
        <v-data-table
          :headers="tableHeaders"
          :items="displayedWorkOrders"
          :items-per-page="10"
          :loading="isLoading"
          hover
          class="wo-table"
        >
          <!-- ID Column -->
          <template v-slot:item.id="{ item }">
            <router-link
              :to="`/work-orders/${item.id}`"
              class="text-decoration-none font-weight-bold px-2 py-1 rounded"
              style="color: #064229; background: #edf5e8; border: 1px solid #c8ddc0; font-family: monospace; font-size: 11px;"
            >
              {{ item.id }}
            </router-link>
          </template>
          
          <!-- Title Column -->
          <template v-slot:item.title="{ item }">
            <div class="font-weight-medium text-truncate" style="max-width: 200px;">{{ item.title }}</div>
          </template>
          
          <!-- Site Column (Hidden on mobile) -->
          <template v-slot:item.site="{ item }">
            <span class="text-caption text-grey-darken-1">{{ item.site }}</span>
          </template>
          
          <!-- Status Column -->
          <template v-slot:item.status="{ item }">
            <v-chip
              :color="statusConfig[item.status]?.color"
              size="x-small"
              variant="tonal"
              class="text-capitalize font-weight-medium"
              label
            >
              {{ formatStatus(item.status) }}
            </v-chip>
          </template>
          
          <!-- Priority Column -->
          <template v-slot:item.priority="{ item }">
            <v-chip
              :color="priorityConfig[item.priority]?.color"
              size="x-small"
              variant="tonal"
              class="text-capitalize font-weight-medium"
              label
            >
              {{ item.priority }}
            </v-chip>
          </template>
          
          <!-- Actions Column -->
          <template v-slot:item.actions="{ item }">
            <div class="d-flex align-center justify-end ga-1">
              <v-btn
                variant="tonal"
                size="x-small"
                :to="`/work-orders/${item.id}`"
                icon="mdi-eye"
                color="#064229"
                rounded="lg"
              ></v-btn>

              <template v-if="authStore.isTechnician">
                <v-btn
                  v-if="item.status === 'open'"
                  color="warning"
                  variant="flat"
                  size="x-small"
                  rounded="lg"
                  @click="startWork(item.id)"
                  class="px-2"
                >
                  Start
                </v-btn>
              </template>

              <v-btn
                v-if="(authStore.isAdmin || authStore.isSupervisor)"
                variant="tonal"
                size="x-small"
                :to="`/work-orders/${item.id}/edit`"
                icon="mdi-pencil"
                color="#064229"
                rounded="lg"
              ></v-btn>
            </div>
          </template>
        </v-data-table>
      </v-card>

      <!-- Empty State -->
      <v-card
        v-if="displayedWorkOrders.length === 0 && !isLoading"
        rounded="lg"
        elevation="0"
        class="pa-8 text-center mt-4"
        style="border: 1px solid #e2e0d8;"
      >
        <v-icon icon="mdi-clipboard-text-outline" size="48" color="grey-lighten-1" class="mb-4"></v-icon>
        <h3 class="text-h6 font-weight-medium mb-2" style="color: #064229;">{{ emptyStateTitle }}</h3>
        <p class="text-body-2 mb-4" style="color: #6b7c6b;">
          {{ emptyStateMessage }}
        </p>
        <v-btn
          v-if="authStore.isAdmin || authStore.isSupervisor"
          color="#064229"
          variant="flat"
          to="/work-orders/new"
          prepend-icon="mdi-plus"
          rounded="lg"
          style="color: #D4E97D;"
        >
          Create work order
        </v-btn>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useWorkOrdersStore } from '@/stores/workorders'

const authStore = useAuthStore()
const workOrdersStore = useWorkOrdersStore()

// Initialize on mount
onMounted(() => {
  workOrdersStore.loadWorkOrders()
})

// Dynamic page title/subtitle based on role
const pageTitle = computed(() => {
  if (authStore.isTechnician) return 'My Tasks'
  return 'Work Orders'
})

const pageSubtitle = computed(() => {
  if (authStore.isTechnician) return 'View and update work orders assigned to you'
  if (authStore.isSupervisor) return 'Monitor and manage team work orders'
  return 'Manage and track all field work orders'
})

const emptyStateTitle = computed(() => {
  if (authStore.isTechnician) return 'No tasks assigned'
  return 'No work orders found'
})

const emptyStateMessage = computed(() => {
  if (authStore.isTechnician) return 'You have no work orders assigned to you right now.'
  return 'Try adjusting your filters or create a new work order.'
})

// Search query
const searchQuery = ref('')

// Filters
const filters = ref({
  status: '',
  priority: '',
  site: '',
})

// Watch filters and update store
watch(filters, (newFilters) => {
  workOrdersStore.setFilters(newFilters)
}, { deep: true })

watch(searchQuery, (newQuery) => {
  workOrdersStore.setFilters({ search: newQuery })
})

// Options for filters
const statusOptions = [
  { title: 'Open', value: 'open' },
  { title: 'In Progress', value: 'in_progress' },
  { title: 'Closed', value: 'closed' },
  { title: 'Cancelled', value: 'cancelled' },
]

const priorityOptions = [
  { title: 'Low', value: 'low' },
  { title: 'Medium', value: 'medium' },
  { title: 'High', value: 'high' },
  { title: 'Critical', value: 'critical' },
]

const todayFormatted = computed(() =>
  new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'long', day: 'numeric', year: 'numeric' })
)

const roleLabel = computed(() => {
  if (authStore.isAdmin) return 'Administrator'
  if (authStore.isSupervisor) return 'Supervisor'
  return 'Technician'
})

const statusConfig = {
  open:        { color: 'blue-darken-1' },
  in_progress: { color: 'orange-darken-2' },
  closed:      { color: 'green-darken-2' },
  cancelled:   { color: 'red-darken-2' },
}

const priorityConfig = {
  high:   { color: '#064229' },
  medium: { color: 'blue-grey' },
  low:    { color: 'grey' },
}

const siteOptions = computed(() => {
  return workOrdersStore.uniqueSites.map(site => ({ title: site, value: site }))
})

// Computed - Role-based data filtering
const displayedWorkOrders = computed(() => {
  let result = workOrdersStore.filteredWorkOrders

  // Technicians only see work orders assigned to them
  if (authStore.isTechnician) {
    const userId = authStore.user?.id
    const userName = authStore.userName
    result = result.filter(wo =>
      wo.assignedToId === userId || wo.assignedTo === userName
    )
  }

  return result
})

const isLoading = computed(() => workOrdersStore.isLoading)

// Table headers differ by role
const tableHeaders = computed(() => {
  if (authStore.isTechnician) {
    return [
      { title: 'ID', key: 'id', sortable: true, width: '10%' },
      { title: 'Title', key: 'title', sortable: true, width: '40%' },
      { title: 'Site', key: 'site', sortable: true, width: '20%', class: 'hidden-xs' },
      { title: 'Status', key: 'status', sortable: true, width: '15%' },
      { title: '', key: 'actions', sortable: false, align: 'end', width: '15%' },
    ]
  }
  return [
    { title: 'ID', key: 'id', sortable: true, width: '10%' },
    { title: 'Title', key: 'title', sortable: true, width: '30%' },
    { title: 'Site', key: 'site', sortable: true, width: '20%', class: 'hidden-sm-and-down' },
    { title: 'Assigned', key: 'assignedTo', sortable: true, width: '20%', class: 'hidden-xs' },
    { title: 'Status', key: 'status', sortable: true, width: '10%' },
    { title: '', key: 'actions', sortable: false, align: 'end', width: '10%' },
  ]
})

// Format status for display
function formatStatus(status) {
  return status.replace('_', ' ')
}

// Format date
function formatDate(dateString) {
  if (!dateString) return '—'
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

// Technician quick action: start work
function startWork(orderId) {
  workOrdersStore.updateStatus(orderId, 'in_progress')
}
</script>

<style scoped>
.wo-table :deep(th) {
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
</style>
