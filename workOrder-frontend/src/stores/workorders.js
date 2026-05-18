/**
 * workorders.js — Work Orders Store (Pinia)
 *
 * Central store for all work order data and operations.
 * Every CRUD action talks to the FastAPI backend via api.js.
 *
 * After each mutation (create / update / delete) the store
 * automatically re-fetches the full list from the server so
 * the UI always reflects the latest data.
 *
 * It also logs every action to the Activity Log store and
 * shows feedback via the Snackbar store.
 */

import { defineStore } from 'pinia'
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from './auth'
import { useActivityLogStore } from './activityLog'
import { useSnackbarStore } from './snackbar'
import {
  fetchWorkOrders,
  createWorkOrder as apiCreateWorkOrder,
  updateWorkOrder as apiUpdateWorkOrder,
  updateWorkOrderStatus as apiUpdateStatus,
  deleteWorkOrder as apiDeleteWorkOrder
} from '@/api'

// ── Color Maps ──────────────────────────────────
// Used by Vuetify chips / badges throughout the UI

/** Maps each work order status to a Vuetify color name */
export const statusColors = {
  open: 'blue',           // Not started yet
  in_progress: 'orange',  // Currently being worked on
  closed: 'green',        // Finished successfully
  cancelled: 'red',       // Stopped / cancelled
}

/** Maps each priority level to a Vuetify color name */
export const priorityColors = {
  low: 'grey',
  medium: 'blue',
  high: 'green',
  critical: 'red',
}

export const useWorkOrdersStore = defineStore('workorders', () => {

  // ── State ─────────────────────────────────────

  const workOrders = ref([])       // The master list of all work orders from the backend
  const isLoading = ref(false)     // True while fetching data from the API
  const error = ref(null)          // Holds the last error message (if any)
  const filters = ref({            // Active filter criteria (used by filteredWorkOrders getter)
    search: '',                    // Free-text search across title, id, site
    status: '',                    // Filter by status (open, in_progress, closed, cancelled)
    priority: '',                  // Filter by priority (low, medium, high, critical)
    site: '',                      // Filter by site name
  })

  // ── Getters ───────────────────────────────────

  /** Returns every work order without any filtering */
  const allWorkOrders = computed(() => workOrders.value)

  /**
   * Returns work orders that match the current filter criteria.
   * Filtering is done client-side for instant responsiveness.
   */
  const filteredWorkOrders = computed(() => {
    let result = workOrders.value

    // Free-text search: match against title, id, or site
    if (filters.value.search) {
      const search = filters.value.search.toLowerCase()
      result = result.filter(wo =>
        wo.title.toLowerCase().includes(search) ||
        wo.id.toLowerCase().includes(search) ||
        wo.site.toLowerCase().includes(search)
      )
    }

    // Status filter
    if (filters.value.status) {
      result = result.filter(wo => wo.status === filters.value.status)
    }

    // Priority filter
    if (filters.value.priority) {
      result = result.filter(wo => wo.priority === filters.value.priority)
    }

    // Site filter
    if (filters.value.site) {
      result = result.filter(wo => wo.site === filters.value.site)
    }

    return result
  })

  /** The 5 most recent work orders (used on the dashboard) */
  const recentWorkOrders = computed(() => {
    return workOrders.value.slice(0, 5)
  })

  /** Dashboard statistics — counts per status */
  const stats = computed(() => {
    const total = workOrders.value.length
    const open = workOrders.value.filter(wo => wo.status === 'open').length
    const inProgress = workOrders.value.filter(wo => wo.status === 'in_progress').length
    const closed = workOrders.value.filter(wo => wo.status === 'closed').length
    const cancelled = workOrders.value.filter(wo => wo.status === 'cancelled').length

    return { total, open, inProgress, closed, cancelled }
  })

  /** A deduplicated list of all site names (for filter dropdowns) */
  const uniqueSites = computed(() => {
    const sites = new Set(workOrders.value.map(wo => wo.site))
    return Array.from(sites)
  })

  // ── Actions ───────────────────────────────────

  /**
   * Fetch all work orders from the backend.
   * Called automatically on mount and after every mutation.
   */
  // Backward compatible alias for older views
  // (some components call initWorkOrders())
  async function initWorkOrders() {
    return loadWorkOrders()
  }

  async function loadWorkOrders() {
    isLoading.value = true
    error.value = null
    try {
      const data = await fetchWorkOrders()   // GET /workorders
      workOrders.value = data
    } catch (err) {
      error.value = 'Failed to load work orders'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  // Auto-load when the store component is first mounted
  onMounted(() => {
    loadWorkOrders()
  })

  /**
   * Find a single work order by ID from the local cache.
   * @param {string} id - The work order ID (e.g. "WO-1045")
   * @returns {Object|undefined}
   */
  function getWorkOrderById(id) {
    return workOrders.value.find(wo => wo.id === id)
  }

  /**
   * Create a new work order via POST /workorders.
   * Automatically refreshes the list, logs the action, and shows a snackbar.
   * @param {Object} workOrderData - All fields for the new work order
   * @returns {Object} The newly created work order from the server
   */
  async function createWorkOrder(workOrderData) {
    const authStore = useAuthStore()
    const logStore = useActivityLogStore()
    const snackbar = useSnackbarStore()

    try {
      // Send the new work order data to the backend
      const newWorkOrder = await apiCreateWorkOrder({
        ...workOrderData,
        createdBy: authStore.userName || 'Unknown',
        status: 'open',
      })

      // Refresh the local list with the latest data from the server
      await loadWorkOrders()

      // Record this action in the activity log
      logStore.log({
        action: 'created',
        workOrderId: newWorkOrder.id,
        workOrderTitle: newWorkOrder.title,
        performedBy: authStore.userName || 'Unknown',
      })

      // Notify the user
      snackbar.success(`Work order "${newWorkOrder.title}" created successfully`)
      return newWorkOrder
    } catch (err) {
      snackbar.error('Failed to create work order')
      throw err
    }
  }

  /**
   * Partially update a work order via PATCH /workorders/{id}.
   * @param {string} id - The work order ID
   * @param {Object} updates - Fields to update (partial)
   * @returns {Object} The updated work order from the server
   */
  async function updateWorkOrder(id, updates) {
    const authStore = useAuthStore()
    const logStore = useActivityLogStore()
    const snackbar = useSnackbarStore()

    try {
      const updated = await apiUpdateWorkOrder(id, updates)
      await loadWorkOrders()

      logStore.log({
        action: 'updated',
        workOrderId: updated.id,
        workOrderTitle: updated.title,
        performedBy: authStore.userName || 'Unknown',
      })

      snackbar.success(`Work order "${updated.title}" updated`)
      return updated
    } catch (err) {
      snackbar.error('Failed to update work order')
      throw err
    }
  }

  /**
   * Change a work order's status via PATCH /workorders/{id}/status.
   * This is a dedicated endpoint because status changes may trigger
   * additional server-side logic (e.g. setting completedAt).
   * @param {string} id - The work order ID
   * @param {string} newStatus - The target status (open, in_progress, closed, cancelled)
   * @param {string} [notes] - Optional completion notes
   * @returns {Object} The updated work order from the server
   */
  async function updateStatus(id, newStatus, notes = '') {
    const authStore = useAuthStore()
    const logStore = useActivityLogStore()
    const snackbar = useSnackbarStore()

    try {
      const updated = await apiUpdateStatus(id, newStatus, notes)
      await loadWorkOrders()

      // Map status values to human-readable action labels for the log
      const actionMap = {
        in_progress: 'started',
        closed: 'completed',
        cancelled: 'cancelled',
      }

      logStore.log({
        action: actionMap[newStatus] || 'status_changed',
        workOrderId: id,
        workOrderTitle: updated.title,
        performedBy: authStore.userName || 'Unknown',
        note: notes || '',
      })

      snackbar.success(`Status updated to ${newStatus}`)
      return updated
    } catch (err) {
      snackbar.error('Failed to update status')
      throw err
    }
  }

  /**
   * Delete a work order via DELETE /workorders/{id}.
   * Captures the work order title before deletion for the log.
   * @param {string} id - The work order ID
   * @returns {boolean} True if deleted, false if an error occurred
   */
  async function deleteWorkOrder(id) {
    const authStore = useAuthStore()
    const logStore = useActivityLogStore()
    const snackbar = useSnackbarStore()

    try {
      // Capture the title before the server removes it
      const wo = workOrders.value.find(w => w.id === id)

      await apiDeleteWorkOrder(id)
      await loadWorkOrders()

      logStore.log({
        action: 'deleted',
        workOrderId: id,
        workOrderTitle: wo?.title || id,
        performedBy: authStore.userName || 'Unknown',
      })

      snackbar.show({
        message: `Work order "${wo?.title || id}" deleted`,
        color: 'error',
        icon: 'mdi-delete-outline'
      })
      return true
    } catch (err) {
      snackbar.error('Failed to delete work order')
      return false
    }
  }

  /**
   * Merge new filter values into the current filter state.
   * @param {Object} newFilters - Partial filter object
   */
  function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
  }

  /** Reset all filters back to their defaults */
  function clearFilters() {
    filters.value = {
      search: '',
      status: '',
      priority: '',
      site: '',
    }
  }

  // ── Expose ────────────────────────────────────
  return {
    // State
    workOrders,
    isLoading,
    error,
    filters,
    // Getters
    allWorkOrders,
    filteredWorkOrders,
    recentWorkOrders,
    stats,
    uniqueSites,
    // Actions
    loadWorkOrders,
    getWorkOrderById,
    createWorkOrder,
    updateWorkOrder,
    updateStatus,
    deleteWorkOrder,
    setFilters,
    clearFilters,
  }
})
