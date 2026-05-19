/**
 * activityLog.js — Activity Log Store (Pinia)
 *
 * Tracks every notable action performed in the app
 * (work order created, status changed, deleted, etc.).
 *
 * All log entries are stored on the FastAPI backend.
 * The store fetches them on mount and refreshes after
 * each new entry or read-status change.
 *
 * "Read" status is per-user and managed server-side,
 * so each user sees their own unread count.
 */

import { defineStore } from 'pinia'
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from './auth'
import {
  fetchActivityLog,
  createActivityLogEntry,
  markAllActivityRead,
  markActivityRead,
  clearActivityLog
} from '@/api'

// ── Action Metadata ─────────────────────────────
// Maps each action type to a display label, icon, and color
// used by the UI when rendering log entries.

export const actionMeta = {
  created:        { label: 'Created',        icon: 'mdi-plus-circle-outline',            color: '#064229' },
  started:        { label: 'Started',        icon: 'mdi-play-circle-outline',            color: 'orange-darken-2' },
  completed:      { label: 'Marked complete',icon: 'mdi-check-circle-outline',           color: 'green-darken-2' },
  cancelled:      { label: 'Cancelled',      icon: 'mdi-close-circle-outline',           color: 'red-darken-2' },
  deleted:        { label: 'Deleted',        icon: 'mdi-delete-outline',                 color: 'red-darken-3' },
  updated:        { label: 'Updated',        icon: 'mdi-pencil-circle-outline',          color: 'blue-darken-1' },
  status_changed: { label: 'Status changed', icon: 'mdi-swap-horizontal-circle-outline', color: 'purple-darken-1' },
}

export const useActivityLogStore = defineStore('activityLog', () => {

  const authStore = useAuthStore()

  // ── State ─────────────────────────────────────

  const entries = ref([])          // Full list of activity log entries from the server
  const isLoading = ref(false)     // True while fetching logs from the API

  // ── Data Loading ──────────────────────────────

  /**
   * Fetch all activity log entries from the backend.
   * Called on mount and after every mutation (new log, mark read, etc.).
   */
  async function loadLogs() {
    if (!authStore.isAuthenticated) {
      entries.value = []
      return
    }

    isLoading.value = true
    try {
      const data = await fetchActivityLog()   // GET /activity-log
      entries.value = data
    } catch (err) {
      console.error('Failed to load activity logs', err)
    } finally {
      isLoading.value = false
    }
  }

  // Auto-load when the store component is first mounted
  onMounted(() => {
    loadLogs()
  })

  watch(
    () => authStore.isAuthenticated,
    (isAuthenticated) => {
      if (isAuthenticated) {
        loadLogs()
      } else {
        entries.value = []
      }
    }
  )

  // ── Getters ───────────────────────────────────

  /** Returns the full list of log entries */
  const allEntries = computed(() => entries.value)

  /** Number of entries the current user hasn't read yet (drives the badge count) */
  const unreadCount = computed(() => {
    return entries.value.filter(e => !e.read).length
  })

  /** The 50 most recent entries (used in the notification dropdown) */
  const recentEntries = computed(() => {
    return entries.value.slice(0, 50)
  })

  // ── Actions ───────────────────────────────────

  /**
   * Create a new activity log entry on the server.
   * Called by other stores (workorders.js) after each action.
   *
   * @param {Object} params
   * @param {string} params.action         - The action type (e.g. 'created', 'deleted')
   * @param {string} params.workOrderId    - ID of the affected work order
   * @param {string} params.workOrderTitle - Title of the affected work order
   * @param {string} params.performedBy    - Name of the user who performed the action
   * @param {string} [params.note]         - Optional additional context
   * @returns {Object} The created entry from the server
   */
  async function log({ action, workOrderId, workOrderTitle, performedBy, note = '' }) {
    try {
      const entry = await createActivityLogEntry({    // POST /activity-log
        action,
        workOrderId,
        workOrderTitle,
        performedBy: performedBy || authStore.userName || 'Unknown',
        note,
      })

      // Refresh the full list so the UI shows the new entry immediately
      await loadLogs()
      return entry
    } catch (err) {
      console.error('Failed to log activity', err)
    }
  }

  /**
   * Mark every log entry as "read" for the current user.
   * Calls PATCH /activity-log/read-all on the backend.
   */
  async function markAllRead() {
    try {
      await markAllActivityRead()
      await loadLogs()   // Refresh so unreadCount updates
    } catch (err) {
      console.error('Failed to mark all read', err)
    }
  }

  /**
   * Mark a single log entry as "read" for the current user.
   * @param {string} id - The log entry ID
   */
  async function markRead(id) {
    try {
      await markActivityRead(id)              // PATCH /activity-log/{id}/read
      await loadLogs()
    } catch (err) {
      console.error('Failed to mark log as read', id, err)
    }
  }

  /**
   * Clear activity log entries on the server and reset local state.
   */
  function clearAll() {
    return clearLogs()
  }

  async function clearLogs() {
    try {
      await clearActivityLog()
      entries.value = []
    } catch (err) {
      console.error('Failed to clear activity logs', err)
    }
  }

  // ── Expose ────────────────────────────────────
  return {
    // State
    entries,
    isLoading,
    // Getters
    allEntries,
    unreadCount,
    recentEntries,
    // Actions
    loadLogs,
    log,
    markAllRead,
    markRead,
    clearAll,
    clearLogs,
  }
})
