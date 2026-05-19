<template>
  <div>
    <!-- Brand Stripe -->
    <v-sheet height="4" color="#064229" class="w-100"></v-sheet>

    <!-- Access Denied for technicians viewing others' work orders -->
    <v-container v-if="accessDenied" fluid class="pa-6 pa-md-8" style="max-width: 1005px;">
      <v-card rounded="lg" elevation="0" class="pa-8 text-center" style="border: 1px solid #e2e0d8;">
        <v-icon icon="mdi-lock-outline" size="48" color="grey-lighten-1" class="mb-4"></v-icon>
        <h3 class="font-weight-medium mb-2" style="color: #064229;">Access Denied</h3>
        <p class="text-body-2 mb-4" style="color: #6b7c6b;">
          You do not have permission to view this work order.
        </p>
        <v-btn color="#064229" variant="flat" to="/work-orders" rounded="lg" style="color: #D4E97D;">
          Back to my tasks
        </v-btn>
      </v-card>
    </v-container>

    <v-container v-else-if="workOrder" fluid class="pa-6 pa-md-8" style="max-width: 1005px;">
      <!-- Header with Back Button -->
      <!-- Header with Back Button -->
      <div class="mb-8">
        <v-btn
          variant="text"
          prepend-icon="mdi-arrow-left"
          to="/work-orders"
          class="mb-4 ps-0"
          color="#064229"
        >
          {{ authStore.isTechnician ? 'Back to my tasks' : 'Back to work orders' }}
        </v-btn>
        
        <div class="d-flex flex-column flex-md-row align-md-center justify-space-between ga-4">
          <div class="text-center text-md-left">
            <div class="d-flex align-center justify-center justify-md-start ga-2 mb-3 flex-wrap">
              <span class="font-weight-bold px-2 py-1 rounded" style="color: #064229; background: #edf5e8; border: 1px solid #c8ddc0; font-family: monospace; font-size: 14px;">
                {{ workOrder.id }}
              </span>
              <v-chip
                :color="statusConfig[workOrder.status]?.color"
                size="small"
                variant="tonal"
                class="text-capitalize font-weight-medium"
                label
              >
                {{ formatStatus(workOrder.status) }}
              </v-chip>
              <v-chip
                :color="priorityConfig[workOrder.priority]?.color"
                size="small"
                variant="tonal"
                class="text-capitalize font-weight-medium"
                label
              >
                {{ workOrder.priority }}
              </v-chip>
            </div>
            <h1 class="font-weight-bold" style="color: #064229; line-height: 1.2;">{{ workOrder.title }}</h1>
          </div>
          
          <!-- Admin/Supervisor actions only -->
          <div v-if="authStore.isAdmin || authStore.isSupervisor" class="d-flex ga-2 justify-center">
            <v-btn
              variant="outlined"
              prepend-icon="mdi-pencil"
              :to="`/work-orders/${workOrder.id}/edit`"
              color="#064229"
              rounded="lg"
              class="flex-grow-1 flex-md-grow-0"
            >
              Edit
            </v-btn>
            <v-btn
              v-if="canDelete"
              variant="outlined"
              color="error"
              prepend-icon="mdi-delete"
              @click="showDeleteDialog = true"
              rounded="lg"
              class="flex-grow-1 flex-md-grow-0"
            >
              Delete
            </v-btn>
          </div>
        </div>
      </div>

    <v-row>
      <!-- Left Column: Details -->
      <v-col cols="12" md="8">
        <!-- Status Actions Card -->
        <v-card v-if="canChangeStatus" rounded="lg" elevation="0" class="mb-4" style="border: 1px solid #e2e0d8;">
          <v-card-title class="font-weight-bold px-6 py-4" style="color: #064229; background: #f9f8f4;">
            Status Actions
          </v-card-title>
          <v-divider style="border-color: #eeece4;"></v-divider>
          <v-card-text class="pa-4">
            <div class="d-flex ga-2 flex-wrap">
              <!-- Technician-specific actions: Start and Complete only -->
              <template v-if="authStore.isTechnician">
                <v-btn
                  v-if="workOrder.status === 'open'"
                  color="warning"
                  variant="flat"
                  prepend-icon="mdi-play"
                  @click="updateStatus('in_progress')"
                  rounded="lg"
                >
                  Start Work
                </v-btn>
                <v-btn
                  v-if="workOrder.status === 'in_progress'"
                  color="#064229"
                  variant="flat"
                  prepend-icon="mdi-check"
                  @click="showCloseDialog = true"
                  rounded="lg"
                  style="color: #D4E97D;"
                >
                  Mark Completed
                </v-btn>
              </template>

              <!-- Admin/Supervisor actions: full control -->
              <template v-else>
                <v-btn
                  v-if="workOrder.status === 'open'"
                  color="warning"
                  variant="flat"
                  prepend-icon="mdi-play"
                  @click="updateStatus('in_progress')"
                  rounded="lg"
                >
                  Start Work
                </v-btn>
                <v-btn
                  v-if="workOrder.status === 'in_progress'"
                  color="#064229"
                  variant="flat"
                  prepend-icon="mdi-check"
                  @click="showCloseDialog = true"
                  rounded="lg"
                  style="color: #D4E97D;"
                >
                  Mark Closed
                </v-btn>
                <v-btn
                  v-if="['open', 'in_progress'].includes(workOrder.status)"
                  color="error"
                  variant="outlined"
                  prepend-icon="mdi-close"
                  @click="showCancelDialog = true"
                  rounded="lg"
                >
                  Cancel Order
                </v-btn>
              </template>
            </div>
          </v-card-text>
        </v-card>

        <!-- Work Order Details -->
        <v-card rounded="lg" elevation="0" class="mb-4" style="border: 1px solid #e2e0d8;">
          <v-card-title class="font-weight-bold px-6 py-4" style="color: #064229; background: #f9f8f4;">
            Details
          </v-card-title>
          <v-divider style="border-color: #eeece4;"></v-divider>
          <v-card-text class="pa-4">
            <v-row>
              <v-col cols="12" sm="6">
                <div class="mb-4">
                  <div class="text-caption text-grey-darken-1">Site / Location</div>
                  <div class="text-body-1">{{ workOrder.site }}</div>
                </div>
              </v-col>
              <v-col cols="12" sm="6">
                <div class="mb-4">
                  <div class="text-caption text-grey-darken-1">Equipment</div>
                  <div class="text-body-1">{{ workOrder.equipment || '-' }}</div>
                </div>
              </v-col>
              <v-col cols="12" sm="6">
                <div class="mb-4">
                  <div class="text-caption text-grey-darken-1">Assigned to</div>
                  <div class="text-body-1">{{ workOrder.assignedTo }}</div>
                </div>
              </v-col>
              <v-col cols="12" sm="6">
                <div class="mb-4">
                  <div class="text-caption text-grey-darken-1">Due date</div>
                  <div class="text-body-1">{{ formatDate(workOrder.dueDate) }}</div>
                </div>
              </v-col>
            </v-row>
            
            <v-divider class="my-4"></v-divider>
            
            <div>
              <div class="text-caption text-grey-darken-1 mb-2">Description</div>
              <div class="text-body-1">{{ workOrder.description || 'No description provided.' }}</div>
            </div>
          </v-card-text>
        </v-card>

        <!-- Completion Summary (only for closed orders) -->
        <v-card v-if="workOrder.status === 'closed'" rounded="lg" elevation="0" class="mb-4" style="border: 1px solid #c4ddb8; background: #f0f8ec;">
          <v-card-title class="font-weight-bold px-6 py-4 text-green-darken-2">
            <v-icon icon="mdi-check-circle" class="me-2"></v-icon>
            Completion Summary
          </v-card-title>
          <v-divider style="border-color: #c4ddb8;"></v-divider>
          <v-card-text class="pa-4">
            <div class="mb-4">
              <div class="text-caption text-grey-darken-1">Completed on</div>
              <div class="text-body-1">{{ formatDate(workOrder.completedAt) }}</div>
            </div>
            <div>
              <div class="text-caption text-grey-darken-1">Completion notes</div>
              <div class="text-body-1">{{ workOrder.completionNotes || 'No notes provided.' }}</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Right Column: Metadata -->
      <v-col cols="12" md="4">
        <v-card rounded="lg" elevation="0" style="border: 1px solid #e2e0d8;">
          <v-card-title class="font-weight-bold px-6 py-4" style="color: #064229; background: #f9f8f4;">
            Information
          </v-card-title>
          <v-divider style="border-color: #eeece4;"></v-divider>
          <v-card-text class="pa-4">
            <div class="mb-3">
              <div class="text-caption text-grey-darken-1">Created by</div>
              <div class="text-body-2">{{ workOrder.createdBy || 'Unknown' }}</div>
            </div>
            <div class="mb-3">
              <div class="text-caption text-grey-darken-1">Created on</div>
              <div class="text-body-2">{{ formatDate(workOrder.createdAt) }}</div>
            </div>
            <div v-if="workOrder.status === 'cancelled'">
              <div class="text-caption text-grey-darken-1 text-error">Cancelled</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

      <!-- Close Work Order Dialog -->
      <v-dialog v-model="showCloseDialog" max-width="500">
        <v-card rounded="lg">
          <v-card-title class="text-h6 font-weight-bold" style="color: #064229;">
            {{ authStore.isTechnician ? 'Complete Work Order' : 'Close Work Order' }}
          </v-card-title>
          <v-card-text class="pt-4">
            <p class="text-body-2 mb-4">Please provide completion notes before closing this work order.</p>
            <v-textarea
              v-model="completionNotes"
              label="Completion notes"
              variant="outlined"
              rows="4"
              placeholder="Describe what was done..."
            ></v-textarea>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showCloseDialog = false" color="#064229">Cancel</v-btn>
            <v-btn color="#064229" variant="flat" @click="closeWorkOrder" rounded="lg" style="color: #D4E97D;">
              {{ authStore.isTechnician ? 'Mark Completed' : 'Mark as Closed' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Cancel Work Order Dialog (Admin/Supervisor only) -->
      <v-dialog v-model="showCancelDialog" max-width="400">
        <v-card rounded="lg">
          <v-card-title class="text-h6 font-weight-bold text-error">Cancel Work Order</v-card-title>
          <v-card-text class="pt-4">
            <p class="text-body-2">Are you sure you want to cancel this work order? This action cannot be undone.</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showCancelDialog = false" color="#064229">No, keep it</v-btn>
            <v-btn color="error" variant="flat" @click="cancelWorkOrder" rounded="lg">Yes, cancel</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Delete Work Order Dialog (Admin/Supervisor only) -->
      <v-dialog v-model="showDeleteDialog" max-width="400">
        <v-card rounded="lg">
          <v-card-title class="text-h6 font-weight-bold text-error">Delete Work Order</v-card-title>
          <v-card-text class="pt-4">
            <p class="text-body-2">Are you sure you want to delete this work order? This action cannot be undone.</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showDeleteDialog = false" color="#064229">Cancel</v-btn>
            <v-btn color="error" variant="flat" @click="deleteWorkOrder" rounded="lg">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>

    <!-- Not Found State -->
    <v-container v-else fluid class="pa-6 pa-md-8" style="max-width: 1240px;">
      <v-card rounded="lg" elevation="0" class="pa-8 text-center" style="border: 1px solid #e2e0d8;">
        <v-icon icon="mdi-alert-circle-outline" size="48" color="grey-lighten-1" class="mb-4"></v-icon>
        <h3 class="text-h6 font-weight-medium mb-2" style="color: #064229;">Work order not found</h3>
        <p class="text-body-2 mb-4" style="color: #6b7c6b;">
          The work order you're looking for doesn't exist or has been removed.
        </p>
        <v-btn color="#064229" variant="flat" to="/work-orders" rounded="lg" style="color: #D4E97D;">
          Back to work orders
        </v-btn>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useWorkOrdersStore } from '@/stores/workorders'

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

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const workOrdersStore = useWorkOrdersStore()

// Dialog states
const showCloseDialog = ref(false)
const showCancelDialog = ref(false)
const showDeleteDialog = ref(false)
const completionNotes = ref('')

// Initialize on mount
onMounted(() => {
  workOrdersStore.loadWorkOrders()
})

// Get work order by ID from route
const workOrderId = computed(() => route.params.id)
const workOrder = computed(() => {
  return workOrdersStore.getWorkOrderById(workOrderId.value)
})

// Access control: technicians can only view their own work orders
const accessDenied = computed(() => {
  if (!workOrder.value) return false // let "not found" state handle missing orders
  if (authStore.isAdmin || authStore.isSupervisor) return false
  // Technician check
  if (authStore.isTechnician) {
    const userId = authStore.user?.id
    const userName = authStore.userName
    return workOrder.value.assignedToId !== userId && workOrder.value.assignedTo !== userName
  }
  return false
})

// Permissions
const canDelete = computed(() => {
  return authStore.isAdmin || authStore.isSupervisor
})

const canChangeStatus = computed(() => {
  if (!workOrder.value) return false
  if (['closed', 'cancelled'].includes(workOrder.value.status)) return false
  if (authStore.isAdmin || authStore.isSupervisor) return true
  // Technicians can change status of their own assigned work orders
  if (authStore.isTechnician) {
    const userId = authStore.user?.id
    const userName = authStore.userName
    return workOrder.value.assignedToId === userId || workOrder.value.assignedTo === userName
  }
  return false
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

// Update status
function updateStatus(newStatus) {
  workOrdersStore.updateStatus(workOrderId.value, newStatus)
}

// Close work order with notes
function closeWorkOrder() {
  workOrdersStore.updateStatus(workOrderId.value, 'closed', completionNotes.value)
  showCloseDialog.value = false
  completionNotes.value = ''
}

// Cancel work order (Admin/Supervisor only)
function cancelWorkOrder() {
  workOrdersStore.updateStatus(workOrderId.value, 'cancelled')
  showCancelDialog.value = false
}

// Delete work order (Admin/Supervisor only)
function deleteWorkOrder() {
  workOrdersStore.deleteWorkOrder(workOrderId.value)
  showDeleteDialog.value = false
  router.push('/work-orders')
}
</script>

<style scoped>
</style>
