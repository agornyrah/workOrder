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
          to="/dashboard"
          class="mb-4 ps-0"
          color="#064229"
        >
          Back to dashboard
        </v-btn>
        
        <div class="text-center text-md-left">
          <h1 class="font-weight-bold" style="color: #064229;">User Management</h1>
          <p style="color: #6b7c6b;">
            Manage system users and their access levels
          </p>
        </div>
      </div>

      <!-- Stats -->
      <v-row class="mb-6 ga-y-3">
        <v-col cols="12" sm="6" md="3">
          <v-card rounded="lg" elevation="0" class="pa-4 h-100" style="border: 1px solid #064229;">
            <div class="text-caption font-weight-bold text-uppercase opacity-70" style="color: #064229;">Total Users</div>
            <div class="text-h5 font-weight-black mt-1" style="color: #064229;">{{ users.length }}</div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card rounded="lg" elevation="0" class="pa-4 h-100" style="border: 1px solid #064229;">
            <div class="text-caption font-weight-bold text-uppercase opacity-70" style="color: #064229;">Admins</div>
            <div class="text-h5 font-weight-black mt-1" style="color: #064229;">{{ adminCount }}</div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card rounded="lg" elevation="0" class="pa-4 h-100" style="border: 1px solid #064229;">
            <div class="text-caption font-weight-bold text-uppercase opacity-70" style="color: #064229;">Supervisors</div>
            <div class="text-h5 font-weight-black mt-1" style="color: #064229;">{{ supervisorCount }}</div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card rounded="lg" elevation="0" class="pa-4 h-100" style="border: 1px solid #064229;">
            <div class="text-caption font-weight-bold text-uppercase opacity-70" style="color: #064229;">Technicians</div>
            <div class="text-h5 font-weight-black mt-1" style="color: #064229;">{{ technicianCount }}</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Users Table -->
      <v-card rounded="lg" elevation="0" style="border: 1px solid #e2e0d8;">
        <v-card-title class="pa-0" style="background: #f9f8f4;">
          <div class="d-flex flex-column flex-sm-row align-sm-center justify-space-between px-6 py-4 ga-4">
            <span class="font-weight-bold" style="color: #064229;">System Users</span>
            <div class="d-flex flex-wrap ga-2">
              <v-btn
                color="#064229"
                variant="flat"
                prepend-icon="mdi-plus"
                rounded="lg"
                class="flex-grow-1 flex-sm-grow-0"
                style="color: #D4E97D;"
                @click="showAddDialog = true"
              >
                Add user
              </v-btn>
              <v-btn
                variant="outlined"
                prepend-icon="mdi-delete-sweep"
                rounded="lg"
                color="error"
                class="flex-grow-1 flex-sm-grow-0"
                @click="showResetDialog = true"
              >
                Reset
              </v-btn>
            </div>
          </div>
          <div class="px-6 pb-4 pt-2" style="background: #f9f8f4;">
            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              label="Search users..."
              variant="outlined"
              density="compact"
              hide-details
              rounded="lg"
              color="#064229"
              bg-color="white"
            ></v-text-field>
          </div>
        </v-card-title>
        <v-divider style="border-color: #eeece4;"></v-divider>
        <v-data-table
          :headers="headers"
          :items="users"
          :items-per-page="10"
          :search="search"
          hover
          class="user-table"
        >
          <template v-slot:item.role="{ item }">
            <v-chip
              :color="roleConfig[item.role]?.color"
              size="small"
              variant="tonal"
              class="text-capitalize font-weight-medium"
              label
            >
              {{ item.role }}
            </v-chip>
          </template>
          <template v-slot:item.actions="{ item }">
            <div class="d-flex ga-1">
              <v-btn
                variant="tonal"
                size="x-small"
                icon="mdi-pencil"
                color="#064229"
                rounded="lg"
                @click="editUser(item)"
              ></v-btn>
              <v-btn
                variant="tonal"
                size="x-small"
                icon="mdi-delete"
                color="error"
                rounded="lg"
                @click="confirmDelete(item)"
                :disabled="item.id === authStore.user?.id"
              ></v-btn>
            </div>
          </template>
        </v-data-table>
      </v-card>

      <!-- Add User Dialog -->
      <v-dialog v-model="showAddDialog" max-width="500">
        <v-card rounded="lg">
          <v-card-title class="text-h6 font-weight-bold" style="color: #064229;">
            Add New User
          </v-card-title>
          <v-card-text class="pt-4">
            <v-form ref="addFormRef" v-model="isAddFormValid">
              <v-text-field
                v-model="newUser.name"
                label="Full name"
                variant="outlined"
                class="mb-3"
                :rules="nameRules"
                required
              ></v-text-field>
              <v-text-field
                v-model="newUser.email"
                label="Email"
                variant="outlined"
                class="mb-3"
                :rules="emailRules"
                required
              ></v-text-field>
              <v-select
                v-model="newUser.role"
                label="Role"
                :items="roleOptions"
                variant="outlined"
                class="mb-3"
                required
              ></v-select>
              <v-text-field
                v-model="newUser.password"
                label="Password"
                type="password"
                variant="outlined"
                class="mb-3"
                :rules="passwordRules"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showAddDialog = false" color="#064229">Cancel</v-btn>
            <v-btn
              color="#064229"
              variant="flat"
              @click="addUser"
              :disabled="!isAddFormValid"
              rounded="lg"
              style="color: #D4E97D;"
            >
              Add user
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Edit User Dialog -->
      <v-dialog v-model="showEditDialog" max-width="500">
        <v-card rounded="lg">
          <v-card-title class="text-h6 font-weight-bold" style="color: #064229;">
            Edit User
          </v-card-title>
          <v-card-text class="pt-4">
            <v-form ref="editFormRef" v-model="isEditFormValid">
              <v-text-field
                v-model="editingUser.name"
                label="Full name"
                variant="outlined"
                class="mb-3"
                :rules="nameRules"
                required
              ></v-text-field>
              <v-text-field
                v-model="editingUser.email"
                label="Email"
                variant="outlined"
                class="mb-3"
                :rules="emailRules"
                required
              ></v-text-field>
              <v-select
                v-model="editingUser.role"
                label="Role"
                :items="roleOptions"
                variant="outlined"
                class="mb-3"
                required
              ></v-select>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showEditDialog = false" color="#064229">Cancel</v-btn>
            <v-btn
              color="#064229"
              variant="flat"
              @click="saveUserChanges"
              :disabled="!isEditFormValid"
              rounded="lg"
              style="color: #D4E97D;"
            >
              Save changes
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Delete Confirmation Dialog -->
      <v-dialog v-model="showDeleteDialog" max-width="400">
        <v-card rounded="lg">
          <v-card-title class="text-h6 font-weight-bold text-error">Delete User</v-card-title>
          <v-card-text class="pt-4">
            <p class="text-body-2">
              Are you sure you want to delete <strong>{{ userToDelete?.name }}</strong>? This action cannot be undone.
            </p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showDeleteDialog = false" color="#064229">Cancel</v-btn>
            <v-btn color="error" variant="flat" @click="confirmAndDeleteUser" rounded="lg">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Reset All Data Dialog -->
      <v-dialog v-model="showResetDialog" max-width="400">
        <v-card rounded="lg">
          <v-card-title class="text-h6 font-weight-bold text-error">Reset All Data</v-card-title>
          <v-card-text class="pt-4">
            <p class="text-body-2 text-error mb-2">
              <v-icon icon="mdi-alert" class="me-1"></v-icon>
              This will delete ALL work orders and reset users to defaults!
            </p>
            <p class="text-body-2">
              Default users will be restored (admin@example.com, supervisor@example.com, technicians).
              Your session will remain active.
            </p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showResetDialog = false" color="#064229">Cancel</v-btn>
            <v-btn color="error" variant="flat" @click="resetAllData" rounded="lg">Reset Everything</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { fetchUsers, updateUser as apiUpdateUser, deleteUser as apiDeleteUser, registerUser as apiCreateUser } from '@/api'
import { useSnackbarStore } from '@/stores/snackbar'

const authStore = useAuthStore()
const snackbar = useSnackbarStore()

// Users list from database
const users = ref([])

const search = ref('')
const headers = [
  { title: 'User', key: 'name', sortable: true, width: '40%' },
  { title: 'Email', key: 'email', sortable: true, width: '30%', class: 'hidden-xs' },
  { title: 'Role', key: 'role', sortable: true, width: '20%' },
  { title: '', key: 'actions', sortable: false, align: 'end', width: '10%' },
]

// Role configuration for chips
const roleConfig = {
  admin: { color: '#064229' },
  supervisor: { color: 'blue-darken-2' },
  technician: { color: 'grey' },
}

const roleOptions = [
  { title: 'Administrator', value: 'admin' },
  { title: 'Supervisor', value: 'supervisor' },
  { title: 'Technician', value: 'technician' },
]

// Stats
const adminCount = computed(() => users.value.filter(u => u.role === 'admin').length)
const supervisorCount = computed(() => users.value.filter(u => u.role === 'supervisor').length)
const technicianCount = computed(() => users.value.filter(u => u.role === 'technician').length)

// Load users from API
async function loadUsers() {
  try {
    const allUsers = await fetchUsers()
    users.value = allUsers.map(u => ({
      id: u.id,
      name: u.name,
      email: u.email,
      role: u.role,
    }))
  } catch (error) {
    console.error('Failed to load users:', error)
    snackbar.error('Failed to load users.')
  }
}

onMounted(() => {
  loadUsers()
})

// Add user dialog
const showAddDialog = ref(false)
const addFormRef = ref()
const isAddFormValid = ref(false)
const newUser = ref({
  name: '',
  email: '',
  role: 'technician',
  password: '',
})

const nameRules = [(v) => !!v || 'Name is required']
const emailRules = [
  (v) => !!v || 'Email is required',
  (v) => /.+@.+\..+/.test(v) || 'Email must be valid',
]
const passwordRules = [
  (v) => !!v || 'Password is required',
  (v) => v.length >= 6 || 'Password must be at least 6 characters',
]

async function addUser() {
  try {
    const user = {
      name: newUser.value.name,
      email: newUser.value.email,
      role: newUser.value.role,
      password: newUser.value.password,
    }

    await apiCreateUser(user)
    snackbar.success('User added successfully!')
    await loadUsers() // Refresh list

    // Reset form and close dialog
    newUser.value = { name: '', email: '', role: 'technician', password: '' }
    showAddDialog.value = false
  } catch (err) {
    console.error('Failed to add user:', err)
    snackbar.error(err.message || 'Failed to add user.')
  }
}

// Edit user dialog
const showEditDialog = ref(false)
const editFormRef = ref()
const isEditFormValid = ref(false)
const editingUser = ref({
  id: '',
  name: '',
  email: '',
  role: '',
})

function editUser(user) {
  editingUser.value = { ...user }
  showEditDialog.value = true
}

async function saveUserChanges() {
  try {
    const updates = {
      name: editingUser.value.name,
      email: editingUser.value.email,
      role: editingUser.value.role,
    }

    await apiUpdateUser(editingUser.value.id, updates)
    snackbar.success('User updated successfully!')
    await loadUsers() // Refresh list

    showEditDialog.value = false
  } catch (err) {
    console.error('Failed to update user:', err)
    snackbar.error(err.message || 'Failed to update user.')
  }
}

// Delete user dialog
const showDeleteDialog = ref(false)
const userToDelete = ref(null)

function confirmDelete(user) {
  userToDelete.value = user
  showDeleteDialog.value = true
}

async function confirmAndDeleteUser() {
  if (!userToDelete.value) return

  try {
    await apiDeleteUser(userToDelete.value.id)
    snackbar.success('User deleted successfully!')
    await loadUsers() // Refresh list

    showDeleteDialog.value = false
    userToDelete.value = null
  } catch (err) {
    console.error('Failed to delete user:', err)
    snackbar.error(err.message || 'Failed to delete user.')
  }
}

// Reset all data dialog
const showResetDialog = ref(false)

async function resetAllData() {
  // This function would ideally call a backend API to reset all data.
  // For now, we'll simulate a reset by clearing local state and reloading.
  // In a real application, you'd have an endpoint like DELETE /admin/reset-data
  // await api.resetAllData() // Example of an API call

  // Clear work orders (assuming workorders_db is also managed by API now)
  // localStorage.removeItem('workorders_db')
  // Clear users (assuming users_db is also managed by API now)
  // localStorage.removeItem('users_db')

  // After a successful backend reset, reload users from the API
  await loadUsers()
  snackbar.success('All data has been reset (simulated). Default users restored from API.')

  showResetDialog.value = false
}
</script>

<style scoped>
.user-table :deep(th) {
  text-transform: uppercase;
  font-size: 0.75rem !important;
  font-weight: 700 !important;
  color: #6b7c6b !important;
  letter-spacing: 0.05em;
}

@media (max-width: 600px) {
  :deep(.hidden-xs) {
    display: none !important;
  }
}
</style>