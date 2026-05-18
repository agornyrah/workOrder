<template>
  <div>
    <!-- Brand Stripe -->
    <v-sheet height="4" color="#064229" class="w-100"></v-sheet>

    <v-container fluid class="pa-6 pa-md-8" style="max-width: 1005px;">
      <!-- Header -->
      <div class="mb-8">
        <div class="d-flex flex-column flex-sm-row align-start justify-space-between ga-4 mb-6">
          <div class="d-flex align-center">
            <v-btn color="#064229" variant="flat" to="/dashboard" rounded="lg" style="color: #D4E97D;">
              Back to Dashboard
            </v-btn>  
          </div>

          <div class="d-flex align-center ga-2 w-100 w-sm-auto justify-space-between">
            <v-btn
              v-if="logStore.unreadCount > 0"
              variant="outlined"
              rounded="lg"
              color="#064229"
              class="px-2"
              @click="logStore.markAllRead()"
            >
              Mark all read
            </v-btn>
            <v-btn
              variant="outlined"
              color="error"
              prepend-icon="mdi-delete-sweep-outline"
              rounded="lg"
              class="px-2"
              @click="showClearDialog = true"
            >
              Clear
            </v-btn>
          </div>
        </div>

        <div class="text-center text-md-left">
          <h1 class="font-weight-bold" style="color: #064229;">Activity Log</h1>
          <p style="color: #6b7c6b;">A full audit trail of all work order actions</p>
        </div>
      </div>

      <!-- Empty State -->
      <v-card
        v-if="logStore.allEntries.length === 0"
        rounded="lg"
        elevation="0"
        class="pa-12 text-center"
        style="border: 1px solid #e2e0d8;"
      >
        <v-icon icon="mdi-history" size="56" color="grey-lighten-2" class="mb-4"></v-icon>
        <h3 class="text-h6 font-weight-medium mb-2" style="color: #064229;">No activity yet</h3>
        <p class="text-body-2" style="color: #6b7c6b;">
          Actions on work orders will appear here.
        </p>
      </v-card>

      <!-- Activity Timeline -->
      <v-card v-else rounded="lg" elevation="0" style="border: 1px solid #e2e0d8;">
        <v-card-title class="d-flex align-center justify-space-between px-6 py-4" style="background: #f9f8f4;">
          <span class="font-weight-bold" style="color: #064229;">All Activity</span>
          <v-chip size="small" variant="tonal" color="#064229">
            {{ logStore.allEntries.length }} entries
          </v-chip>
        </v-card-title>
        <v-divider style="border-color: #eeece4;"></v-divider>

        <v-list lines="two" class="py-0">
          <template v-for="(entry, index) in logStore.allEntries" :key="entry.id">
            <v-list-item
              :class="['px-6 py-4', !entry.read ? 'unread-entry' : '']"
              @click="logStore.markRead(entry.id)"
            >
              <template v-slot:prepend>
                <v-avatar
                  size="38"
                  :color="actionMeta[entry.action]?.color || '#064229'"
                  variant="tonal"
                  class="me-3"
                >
                  <v-icon :icon="actionMeta[entry.action]?.icon || 'mdi-circle'" size="18"></v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-medium text-body-2 mb-1" style="color: #1a2e1a;">
                <router-link
                  :to="`/work-orders/${entry.workOrderId}`"
                  class="text-decoration-none font-weight-bold px-1 py-0 rounded"
                  style="color: #064229; background: #edf5e8; border: 1px solid #c8ddc0; font-family: monospace; font-size: 11px;"
                >
                  {{ entry.workOrderId }}
                </router-link>
                <span class="ms-2">{{ entry.workOrderTitle }}</span>
              </v-list-item-title>

              <v-list-item-subtitle class="d-flex align-center flex-wrap ga-2 mt-1">
                <v-chip
                  :color="actionMeta[entry.action]?.color || '#064229'"
                  size="x-small"
                  variant="tonal"
                  label
                  class="font-weight-medium"
                >
                  {{ actionMeta[entry.action]?.label || entry.action }}
                </v-chip>
                <span style="color: #6b7c6b;">by <strong>{{ entry.performedBy }}</strong></span>
                <span v-if="entry.note" style="color: #6b7c6b;">· {{ entry.note }}</span>
              </v-list-item-subtitle>

              <template v-slot:append>
                <div class="text-right hidden-xs">
                  <div class="text-caption font-weight-medium" style="color: #9aa89a; white-space: nowrap;">
                    {{ formatTime(entry.timestamp) }}
                  </div>
                  <div class="text-caption" style="color: #b0bcb0; white-space: nowrap;">
                    {{ formatDate(entry.timestamp) }}
                  </div>
                  <v-badge
                    v-if="!entry.read"
                    dot
                    color="#064229"
                    class="mt-1"
                  ></v-badge>
                </div>
                <!-- Small indicator for mobile instead of full time -->
                <v-icon v-if="!entry.read" icon="mdi-circle" size="10" color="#064229" class="ms-2 d-sm-none"></v-icon>
              </template>
            </v-list-item>
            <v-divider v-if="index < logStore.allEntries.length - 1" style="border-color: #f0ede6;"></v-divider>
          </template>
        </v-list>
      </v-card>
    </v-container>

    <!-- Clear Log Confirmation Dialog -->
    <v-dialog v-model="showClearDialog" max-width="380">
      <v-card rounded="lg">
        <v-card-title class="text-h6 font-weight-bold text-error pa-6 pb-2">
          Clear Activity Log?
        </v-card-title>
        <v-card-text class="px-6 pb-4">
          <p class="text-body-2" style="color: #6b7c6b;">
            This will permanently delete all activity log entries. This action cannot be undone.
          </p>
        </v-card-text>
        <v-card-actions class="px-6 pb-6">
          <v-spacer></v-spacer>
          <v-btn variant="text" color="#064229" @click="showClearDialog = false">Cancel</v-btn>
          <v-btn color="error" variant="flat" rounded="lg" @click="handleClear">Yes, clear all</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useActivityLogStore, actionMeta } from '@/stores/activityLog'

const logStore = useActivityLogStore()
const showClearDialog = ref(false)

function handleClear() {
  logStore.clearAll()
  showClearDialog.value = false
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>

<style scoped>
.unread-entry {
  background: #f6fbf3;
}
</style>
