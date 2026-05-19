<template>
  <div>
    <!-- Brand Stripe -->
    <v-sheet height="4" color="#064229" class="w-100"></v-sheet>

    <v-container v-if="workOrder" fluid class="pa-6 pa-md-8" style="max-width: 1005px;">
      <!-- Header -->
      <div class="mb-8">
        <v-btn
          variant="text"
          prepend-icon="mdi-arrow-left"
          :to="`/work-orders/${workOrderId}`"
          class="mb-4 ps-0"
          color="#064229"
        >
          Back to work order
        </v-btn>

        <div class="text-center text-md-left mt-n2">
          <h1 class="font-weight-bold" style="color: #064229;">Edit Work Order</h1>
          <p style="color: #6b7c6b;">
            <span class="px-2 py-1 rounded" style="color: #064229; background: #edf5e8; border: 1px solid #c8ddc0; font-family: monospace; font-size: 12px;">{{ workOrder.id }}</span>
            — {{ workOrder.title }}
          </p>
        </div>
      </div>

      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card rounded="lg" elevation="0" style="border: 1px solid #e2e0d8;">
            <v-card-text class="pa-6">
            <!-- Success Message -->
            <v-alert
              v-if="successMessage"
              type="success"
              variant="tonal"
              class="mb-4"
            >
              {{ successMessage }}
            </v-alert>

            <!-- Error Message -->
            <v-alert
              v-if="errorMessage"
              type="error"
              variant="tonal"
              class="mb-4"
            >
              {{ errorMessage }}
            </v-alert>

            <v-form ref="formRef" v-model="isFormValid" @submit.prevent="handleSubmit">
              <!-- Title -->
              <v-text-field
                v-model="form.title"
                label="Work order title"
                variant="outlined"
                class="mb-4"
                :rules="titleRules"
                required
              ></v-text-field>

              <!-- Site -->
              <v-select
                v-model="form.site"
                label="Site / Location"
                :items="siteOptions"
                variant="outlined"
                class="mb-4"
                :rules="siteRules"
                required
              ></v-select>

              <!-- Equipment -->
              <v-text-field
                v-model="form.equipment"
                label="Equipment (optional)"
                variant="outlined"
                class="mb-4"
              ></v-text-field>

              <!-- Assigned To -->
              <v-select
                v-model="form.assignedTo"
                label="Assigned to"
                :items="technicianOptions"
                variant="outlined"
                class="mb-4"
                :rules="assignedToRules"
                required
              ></v-select>

              <!-- Priority -->
              <v-select
                v-model="form.priority"
                label="Priority"
                :items="priorityOptions"
                variant="outlined"
                class="mb-4"
                :rules="priorityRules"
                required
              ></v-select>

              <!-- Due Date -->
              <v-text-field
                v-model="form.dueDate"
                label="Due date"
                type="date"
                :min="minDate"
                variant="outlined"
                class="mb-4"
                :rules="dueDateRules"
                required
              ></v-text-field>

              <!-- Description -->
              <v-textarea
                v-model="form.description"
                label="Description"
                variant="outlined"
                rows="4"
                class="mb-4"
              ></v-textarea>

              <!-- Action Buttons -->
              <div class="d-flex flex-column flex-sm-row ga-3 justify-end mt-6">
                <v-btn
                  variant="text"
                  :to="`/work-orders/${workOrderId}`"
                  color="#064229"
                  class="flex-grow-1 flex-sm-grow-0"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="#064229"
                  variant="flat"
                  type="submit"
                  :disabled="!isFormValid || isSubmitting"
                  :loading="isSubmitting"
                  rounded="lg"
                  class="flex-grow-1 flex-sm-grow-0"
                  style="color: #D4E97D;"
                >
                  Save changes
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
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
import { fetchTechnicians } from '@/api'

const minDate = computed(() => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString().split('T')[0]
})

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const workOrdersStore = useWorkOrdersStore()

// Get work order ID from route
const workOrderId = computed(() => route.params.id)
const workOrder = computed(() => {
  return workOrdersStore.getWorkOrderById(workOrderId.value)
})

// Initialize on mount
onMounted(async () => {
  await workOrdersStore.loadWorkOrders()
  await loadTechnicians()

  // Populate form with existing data
  if (workOrder.value) {
    form.value = {
      title: workOrder.value.title,
      site: workOrder.value.site,
      equipment: workOrder.value.equipment || '',
      assignedTo: workOrder.value.assignedTo,
      priority: workOrder.value.priority,
      dueDate: workOrder.value.dueDate,
      description: workOrder.value.description || '',
    }
  }
})

// Form state
const formRef = ref()
const isFormValid = ref(false)
const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const form = ref({
  title: '',
  site: '',
  equipment: '',
  assignedTo: '',
  priority: 'medium',
  dueDate: '',
  description: '',
})

// Options
const siteOptions = [
  { title: 'Site A', value: 'Site A' },
  { title: 'Site B', value: 'Site B' },
  { title: 'Site C', value: 'Site C' },
]

const technicians = ref([])

const technicianOptions = computed(() => {
  return [...technicians.value.map(t => ({ title: t.name, value: t.name })), { title: 'Unassigned', value: 'Unassigned' }]
})

async function loadTechnicians() {
  try {
    technicians.value = await fetchTechnicians()
  } catch (err) {
    technicians.value = []
  }
}


const priorityOptions = [
  { title: 'Low', value: 'low' },
  { title: 'Medium', value: 'medium' },
  { title: 'High', value: 'high' },
  { title: 'Critical', value: 'critical' },
]

// Validation rules
const titleRules = [
  (v) => !!v || 'Title is required',
  (v) => v.length >= 5 || 'Title must be at least 5 characters',
]

const siteRules = [
  (v) => !!v || 'Site is required',
]

const assignedToRules = [
  (v) => !!v || 'Please assign to someone',
]

const priorityRules = [
  (v) => !!v || 'Priority is required',
]

const dueDateRules = [
  (v) => !!v || 'Due date is required',
]

// Submit handler
async function handleSubmit() {
  const isValid = await formRef.value?.validate()
  if (!isValid.valid) return

  isSubmitting.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await workOrdersStore.updateWorkOrder(workOrderId.value, {
      title: form.value.title,
      site: form.value.site,
      equipment: form.value.equipment,
      assignedTo: form.value.assignedTo,
      priority: form.value.priority,
      dueDate: form.value.dueDate,
      description: form.value.description,
      status: workOrder.value.status,
      createdAt: workOrder.value.createdAt
    })

    successMessage.value = 'Work order updated successfully!'
    
    // Redirect after short delay
    setTimeout(() => {
      router.push(`/work-orders/${workOrderId.value}`)
    }, 1500)
  } catch (err) {
    errorMessage.value = err.message || 'Failed to update work order'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
</style>
