<template>
  <div>
    <!-- Brand Stripe -->
    <v-sheet height="4" color="#064229" class="w-100"></v-sheet>

    <v-container fluid class="pa-6 pa-md-8" style="max-width: 1005px;">
      <!-- Header -->
      <div class="mb-8">
        <v-btn
          variant="text"
          prepend-icon="mdi-arrow-left"
          to="/work-orders"
          class="mb-4 ps-0"
          color="#064229"
        >
          Back to work orders
        </v-btn>

        <div class="text-center text-md-left mt-n2">
          <h1 class="font-weight-bold" style="color: #064229;">Create Work Order</h1>
          <p style="color: #6b7c6b;">Create a new field work order</p>
        </div>
      </div>

      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card rounded="lg" elevation="0" style="border: 1px solid #e2e0d8;">
            <v-card-text class="pa-6">
            <v-form ref="formRef" v-model="isFormValid" @submit.prevent="handleSubmit">
              <!-- Title -->
              <v-text-field
                v-model="form.title"
                label="Work order title"
                placeholder="e.g., Valve inspection - Well 3A"
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
                placeholder="e.g., Wellhead valve, Pump P-101"
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
                placeholder="Describe the work to be done..."
                variant="outlined"
                rows="4"
                class="mb-4"
              ></v-textarea>

              <!-- Action Buttons -->
              <div class="d-flex flex-column flex-sm-row ga-3 justify-end mt-6">
                <v-btn
                  variant="text"
                  to="/work-orders"
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
                  Create work order
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useWorkOrdersStore } from '@/stores/workorders'
import { fetchTechnicians } from '@/api'

const minDate = computed(() => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString().split('T')[0]
})

const router = useRouter()
const authStore = useAuthStore()
const workOrdersStore = useWorkOrdersStore()

// Initialize on mount
onMounted(() => {
  workOrdersStore.loadWorkOrders()
  loadTechnicians()
})

// Form state
const formRef = ref()
const isFormValid = ref(false)
const isSubmitting = ref(false)

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

// Load technicians dynamically from database
const technicians = ref([])

const technicianOptions = computed(() => {
  return technicians.value.map(t => ({ title: t.name, value: t.name }))
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

  try {
    const newWorkOrder = await workOrdersStore.createWorkOrder({
      title: form.value.title,
      site: form.value.site,
      equipment: form.value.equipment,
      assignedTo: form.value.assignedTo,
      priority: form.value.priority,
      dueDate: form.value.dueDate,
      description: form.value.description,
      createdBy: authStore.userName,
    })

    // Redirect after short delay
    setTimeout(() => {
      router.push(`/work-orders/${newWorkOrder.id}`)
    }, 1200)
  } catch (err) {
    const { useSnackbarStore } = await import('@/stores/snackbar')
    useSnackbarStore().error(err.message || 'Failed to create work order')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
</style>
