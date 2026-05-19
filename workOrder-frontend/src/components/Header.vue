<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useActivityLogStore, actionMeta } from '@/stores/activityLog'

const router = useRouter()
const authStore = useAuthStore()
const logStore = useActivityLogStore()

const mobileDrawer = ref(false)
const notifMenu = ref(false)

const userInitials = computed(() => {
  const name = authStore.userName
  if (!name) return ''
  return name.charAt(0).toUpperCase()
})

function handleLogout() {
  mobileDrawer.value = false
  authStore.logout()
  router.push('/')
}

function formatTimeAgo(iso) {
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return `${Math.floor(hrs / 24)}d ago`
}
</script>

<template>
  <!-- Mobile Drawer -->
  <v-navigation-drawer
    v-model="mobileDrawer"
    temporary
    location="left"
    width="280"
  >
    <!-- Drawer Header -->
    <div class="pa-5 d-flex align-center justify-space-between" style="background: #064229;">
      <div class="d-flex align-center ga-2">
        <v-icon color="#D4E97D" size="30">mdi-facebook-workplace</v-icon>
        <span class="font-weight-bold text-white text-body-1">WorkOrder</span>
      </div>
      <v-btn icon="mdi-close" variant="text" color="white" size="small" @click="mobileDrawer = false" />
    </div>

    <!-- Authenticated nav -->
    <template v-if="authStore.isAuthenticated">
      <!-- User info -->
      <div class="pa-4 d-flex align-center ga-3" style="border-bottom: 1px solid #e8e6de;">
        <v-avatar color="#064229" size="40">
          <span class="text-body-2 text-white font-weight-bold">{{ userInitials }}</span>
        </v-avatar>
        <div>
          <div class="font-weight-bold text-body-2" style="color: #1a2e1a;">{{ authStore.userName }}</div>
          <div class="text-caption text-capitalize" style="color: #6b7c6b;">{{ authStore.userRole }}</div>
        </div>
      </div>

      <v-list density="compact" class="mt-2 px-2">
        <v-list-item
          prepend-icon="mdi-view-dashboard-outline"
          title="Dashboard"
          to="/dashboard"
          rounded="lg"
          color="#064229"
          @click="mobileDrawer = false"
        ></v-list-item>

        <v-list-item
          v-if="authStore.isTechnician"
          prepend-icon="mdi-clipboard-list-outline"
          title="My Tasks"
          to="/work-orders"
          rounded="lg"
          color="#064229"
          @click="mobileDrawer = false"
        ></v-list-item>

        <v-list-item
          v-if="authStore.isAdmin || authStore.isSupervisor"
          prepend-icon="mdi-clipboard-text-outline"
          title="Work Orders"
          to="/work-orders"
          rounded="lg"
          color="#064229"
          @click="mobileDrawer = false"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-history"
          title="Activity Log"
          to="/activity-log"
          rounded="lg"
          color="#064229"
          @click="mobileDrawer = false"
        >
          <template v-slot:append>
            <v-badge
              v-if="logStore.unreadCount > 0"
              :content="logStore.unreadCount"
              color="#064229"
              inline
            ></v-badge>
          </template>
        </v-list-item>

        <v-list-item
          v-if="authStore.isAdmin"
          prepend-icon="mdi-account-cog-outline"
          title="User Management"
          to="/users"
          rounded="lg"
          color="#064229"
          @click="mobileDrawer = false"
        ></v-list-item>

        <v-divider class="my-2"></v-divider>

        <v-list-item
          prepend-icon="mdi-logout"
          title="Logout"
          rounded="lg"
          base-color="error"
          @click="handleLogout"
        ></v-list-item>
      </v-list>
    </template>

    <!-- Public nav -->
    <template v-else>
      <v-list density="compact" class="mt-2 px-2">
        <v-list-item prepend-icon="mdi-star-outline" title="Features" to="/#features" rounded="lg" color="#064229" @click="mobileDrawer = false"></v-list-item>
        <v-list-item prepend-icon="mdi-help-circle-outline" title="How it works" to="/#how-it-works" rounded="lg" color="#064229" @click="mobileDrawer = false"></v-list-item>
        <v-list-item prepend-icon="mdi-briefcase-outline" title="Services" to="/#services" rounded="lg" color="#064229" @click="mobileDrawer = false"></v-list-item>
        <v-divider class="my-2"></v-divider>
        <div class="px-2 pb-2">
          <v-btn color="#064229" variant="flat" block rounded="pill" to="/login" style="color: white;" @click="mobileDrawer = false">
            Sign in
          </v-btn>
        </div>
      </v-list>
    </template>
  </v-navigation-drawer>

  <!-- App Bar -->
  <v-app-bar flat color="white" density="comfortable" class="py-2" style="border-bottom: 0.5px solid #064229;">
    <v-container class="d-flex align-center">

      <!-- Hamburger (mobile/tablet only) -->
      <v-btn
        class="d-lg-none me-2"
        icon="mdi-menu"
        variant="text"
        color="#064229"
        size="large"
        @click="mobileDrawer = !mobileDrawer"
        style="z-index: 2;"
      />

      <!-- Logo (Centered on mobile/tablet, left-aligned on desktop) -->
      <div 
        class="d-flex align-center" 
        :class="{'position-absolute w-100 justify-center left-0': $vuetify.display.mdAndDown, 'me-6': $vuetify.display.lgAndUp}"
        style="pointer-events: none; z-index: 1;"
      >
        <router-link to="/" class="d-flex align-center text-decoration-none text-black" style="pointer-events: auto;">
          <v-icon color="#064229" size="32" class="me-2">mdi-facebook-workplace</v-icon>
          <span class="font-weight-bold">WorkOrder</span>
        </router-link>
      </div>

      <v-spacer class="d-none d-lg-flex"></v-spacer>

      <!-- Desktop Nav (authenticated) -->
      <template v-if="authStore.isAuthenticated">
        <div class="d-none d-lg-flex align-center justify-center ga-1">
          <v-btn variant="text" class="text-decoration-none" to="/dashboard">Dashboard</v-btn>

          <v-btn
            v-if="authStore.isTechnician"
            variant="text"
            class="text-decoration-none"
            to="/work-orders"
          >My Tasks</v-btn>

          <v-btn
            v-if="authStore.isAdmin || authStore.isSupervisor"
            variant="text"
            class="text-decoration-none"
            to="/work-orders"
          >Work Orders</v-btn>

          <v-btn
            v-if="authStore.isAdmin"
            variant="text"
            class="text-decoration-none"
            to="/users"
          >Users</v-btn>
        </div>
      </template>

      <!-- Desktop Nav (public) -->
      <template v-else>
        <div class="d-none d-lg-flex align-center ga-1">
          <router-link class="text-decoration-none" to="/#features" style="color: #064229; font-weight: 500;">Features</router-link>
          <router-link class="text-decoration-none mx-8" to="/#how-it-works" style="color: #064229; font-weight: 500;">How it works</router-link>
          <router-link class="text-decoration-none" to="/#services" style="color: #064229; font-weight: 500;">Services</router-link>

          <!-- <v-btn variant="text" class="text-decoration-none" to="/#features">Features</v-btn>
          <v-btn variant="text" class="text-decoration-none" to="/#how-it-works">How it works</v-btn>
          <v-btn variant="text" class="text-decoration-none" to="/#services">Services</v-btn> -->
        </div>
      </template>

      <v-spacer></v-spacer>

      <!-- Authenticated: Notification bell + user menu -->
      <template v-if="authStore.isAuthenticated">
        <!-- Notification Bell -->
        <v-menu
          v-model="notifMenu"
          :close-on-content-click="false"
          location="bottom end"
          offset="8"
          min-width="360"
          max-width="400"
        >
          <template v-slot:activator="{ props }">
            <v-btn
              icon
              variant="text"
              v-bind="props"
              class="me-1 d-none d-md-flex"
            >
              <v-badge
                :content="logStore.unreadCount"
                :model-value="logStore.unreadCount > 0"
                color="#064229"
                max="99"
              >
                <v-icon color="#064229">mdi-bell-outline</v-icon>
              </v-badge>
            </v-btn>
          </template>

          <v-card elevation="2" style="border: 1px solid #e2e0d8;">
            <v-card-title class="d-flex align-center justify-center px-4 py-3" style="background: #f9f8f4; border-bottom: 1px solid #eeece4;">
              <span class="font-weight-bold" style="color: #064229;">Notifications</span>
            </v-card-title>

            <div v-if="logStore.recentEntries.length === 0" class="pa-6 text-center">
              <v-icon icon="mdi-bell-sleep-outline" size="36" color="grey-lighten-2" class="mb-2"></v-icon>
              <div class="text-body-2" style="color: #9aa89a;">No activity yet</div>
            </div>

            <v-list v-else lines="two" class="py-0" max-height="360" style="overflow-y: auto;">
              <template v-for="(entry, i) in logStore.recentEntries.slice(0, 8)" :key="entry.id">
                <v-list-item
                  :to="`/work-orders/${entry.workOrderId}`"
                  class="px-4 py-3"
                  :style="!entry.read ? 'background: #f6fbf3;' : ''"
                  @click="notifMenu = false"
                >
                  <template v-slot:prepend>
                    <v-avatar size="32" :color="actionMeta[entry.action]?.color || '#064229'" variant="tonal" class="me-3">
                      <v-icon :icon="actionMeta[entry.action]?.icon || 'mdi-circle'" size="16"></v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-body-2 font-weight-medium" style="color: #1a2e1a; white-space: normal; line-height: 1.4;">
                    {{ entry.workOrderTitle }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="d-flex align-center ga-1 mt-1 flex-wrap">
                    <v-chip :color="actionMeta[entry.action]?.color || '#064229'" size="x-small" variant="tonal" label class="font-weight-medium">
                      {{ actionMeta[entry.action]?.label || entry.action }}
                    </v-chip>
                    <span class="text-caption" style="color: #9aa89a;">{{ formatTimeAgo(entry.timestamp) }}</span>
                  </v-list-item-subtitle>
                </v-list-item>
                <v-divider v-if="i < 7" style="border-color: #f0ede6;"></v-divider>
              </template>
            </v-list>

            <div class="pa-3" style="border-top: 1px solid #eeece4;">
              <v-btn
                block
                variant="tonal"
                color="#064229"
                rounded="lg"
                to="/activity-log"
                @click="notifMenu = false"
              >
                <v-icon start>mdi-history</v-icon>
                Full Activity Log
              </v-btn>
            </div>
          </v-card>
        </v-menu>

        <!-- User Avatar Menu -->
        <v-menu location="bottom end" offset="8">
          <template v-slot:activator="{ props }">
            <v-btn variant="text" v-bind="props" class="d-flex align-center text-body-2 ps-2 pe-1">
              <v-avatar color="#064229" size="28" class="me-2">
                <span class="text-white">{{ userInitials }}</span>
              </v-avatar>
              <span class="d-none d-sm-flex">{{ authStore.userName }}</span>
              <v-icon end icon="mdi-chevron-down" size="small"></v-icon>
            </v-btn>
          </template>

          <v-list density="compact" elevation="2" min-width="150" style="border: 1px solid #e2e0d8;">
            <v-list-item>
              <v-list-item-title class="text-decoration-none">
                Role: {{ authStore.userRole }}
              </v-list-item-title>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item @click="handleLogout" class="text-error" prepend-icon="mdi-logout" rounded="lg">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>

      <!-- Public: Sign in button -->
      <template v-else>
        <v-btn
          variant="flat"
          color="#064229"
          rounded="pill"
          elevation="0"
          class="d-none d-md-flex px-6 font-weight-medium text-white"
          to="/login"
        >
          Sign in
        </v-btn>
      </template>
    </v-container>
  </v-app-bar>
</template>
