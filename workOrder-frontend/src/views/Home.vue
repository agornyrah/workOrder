<script setup>
const steps = [
  {
    title: 'Create an order',
    description: 'Supervisor logs a new work order with title, location, equipment, and priority.',
  },
  {
    title: 'Assign & execute',
    description: 'Technician is notified, updates status to In Progress, and completes the task on site.',
  },
  {
    title: 'Close & report',
    description: 'Order is closed with completion notes. Dashboard reflects the update instantly.',
  },
  {
    title: 'Review & audit',
    description: 'Admins review history, activity logs, and export reports for compliance.',
  },
]
</script>
<template>
  <div>
    <!-- HERO SECTION -->
    <section class="hero-section">
    <v-img
      src="https://images.pexels.com/photos/6169133/pexels-photo-6169133.jpeg"
      alt="Hero"
      cover
      class="hero-background"
    >
    <!-- Left-to-right gradient overlay -->
    <div class="side-overlay"></div>

    <v-container class="fill-height">
      <v-row align="center" justify="center" justify-md="start">
        <v-col cols="12" md="8" lg="7" class="text-center text-md-left d-flex flex-column justify-center align-center align-md-start">
          
          <!-- Main Heading -->
          <h1 class="heading-text text-white text-uppercase mb-6 line-height-tight">
            Manage field work orders from anywhere
          </h1>

          <!-- Description -->
          <p class="text-white mb-8 opacity-90 max-width-600">
              Create, assign, and track maintenance and inspection work orders
              across all your field sites — from a single dashboard your team
              actually uses.
          </p>

          <!-- CTA Buttons -->
          <div class="d-flex flex-column flex-sm-row ga-3 w-100 justify-center justify-md-start">
            <v-btn 
                color="#D4E97D" 
                size="large" 
                rounded="pill" 
                elevation="0"
                class="px-8 font-weight-bold"
                to="/login">
              Get started
            </v-btn>
            <v-btn 
                color="white" 
                variant="outlined" 
                size="large" 
                rounded="pill" 
                class="px-8 text-none font-weight-bold"
                to="/login">
              See how it works
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
    </v-img>
  </section>

    <!-- WHAT YOU GET / FEATURES SECTION -->
<section
  id="features"
  class="features-section py-16"
  style="background-color: #F7F8F2;"
>
  <v-container class="text-center">
    
    <!-- Pill Badge -->
    <v-chip
      size="small"
      class="mb-6 font-weight-bold text-uppercase"
      variant="flat"
      style="background-color: #E9F4C2; color: #064229; letter-spacing: 1px;"
    >
      Features
    </v-chip>

    <!-- Main Heading -->
    <h2
      class="font-weight-bold text-uppercase mb-4"
      style="
        font-size: clamp(2rem, 4vw, 3rem);
        line-height: 1.1;
        max-width: 800px;
        margin: 0 auto;
        color: #064229;
        letter-spacing: -0.02em;
      "
    >
      Everything your field <br /> team needs
    </h2>

    <!-- Subheading -->
    <p
      class="mx-auto mb-10"
      style="
        max-width: 600px;
        color: #064229;
        opacity: 0.8;
        line-height: 1.6;
      "
    >
      A groundbreaking feature: real-time tools for field tracking was introduced,
      setting your field team apart from competitors.
    </p>

    <!-- Feature Cards -->
    <v-row class="mt-4">
      <!-- Card 1 -->
      <v-col cols="12" md="4">
        <v-card
          flat
          class="pa-8 text-left fill-height d-flex flex-column"
          style="border-radius: 16px; background-color: #ffffff;"
        >
          <v-icon color="#4CAF50" size="32" class="mb-6">mdi-clipboard-list-outline</v-icon>
          <h3
            class="text-h6 font-weight-bold mb-3"
            style="color: #064229; line-height: 1.2;"
          >
            Work order tracking
          </h3>
          <p
            class="text-body-2"
            style="color: #064229; opacity: 0.7; line-height: 1.6;"
          >
            Create, assign, and update work orders in real time. Filter by site, priority, or status.
          </p>
        </v-card>
      </v-col>

      <!-- Card 2 -->
      <v-col cols="12" md="4">
        <v-card
          flat
          class="pa-8 text-left fill-height d-flex flex-column"
          style="border-radius: 16px; background-color: #ffffff;"
        >
          <v-icon color="#4CAF50" size="32" class="mb-6">mdi-check-circle-outline</v-icon>
          <h3
            class="text-h6 font-weight-bold mb-3"
            style="color: #064229; line-height: 1.2;"
          >
            Status management
          </h3>
          <p
            class="text-body-2"
            style="color: #064229; opacity: 0.7; line-height: 1.6;"
          >
            Move orders through Open &rarr; In Progress &rarr; Closed with a full activity log.
          </p>
        </v-card>
      </v-col>

      <!-- Card 3 -->
      <v-col cols="12" md="4">
        <v-card
          flat
          class="pa-8 text-left fill-height d-flex flex-column"
          style="border-radius: 16px; background-color: #ffffff;"
        >
          <v-icon color="#4CAF50" size="32" class="mb-6">mdi-bell-alert-outline</v-icon>
          <h3
            class="text-h6 font-weight-bold mb-3"
            style="color: #064229; line-height: 1.2;"
          >
            Priority alerts
          </h3>
          <p
            class="text-body-2"
            style="color: #064229; opacity: 0.7; line-height: 1.6;"
          >
            Flag high-priority tasks and get dashboard alerts before SLA deadlines are missed.
          </p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</section>


<!-- HOW IT WORKS SECTION -->
<section
  id="how-it-works"
  class="how-it-works-section py-16"
  style="background-color: #D4E97D;"
>
  <v-container class="text-center">
    
    <!-- Pill Badge -->
    <v-chip
      size="small"
      class="mb-6 font-weight-bold text-uppercase"
      variant="flat"
      style="background-color: #E9F4C2; color: #064229; letter-spacing: 1px;"
    >
      How It Works
    </v-chip>

    <!-- Main Heading -->
    <h2
      class="font-weight-bold text-uppercase mb-4"
      style="
        font-size: clamp(2rem, 4vw, 3rem);
        line-height: 1.1;
        color: #064229;
        max-width: 600px;
        margin: 0 auto;
        letter-spacing: -0.02em;
      "
    >
      How the <br /> Program Works
    </h2>

    <!-- Subheading -->
    <p
      class="mx-auto mb-16"
      style="
        max-width: 500px;
        color: #064229;
        opacity: 0.9;
        line-height: 1.6;
      "
    >
      A groundbreaking feature: real-time tools for field tracking was introduced,
      setting the company apart from competitors.
    </p>

    <!-- Steps Row -->
    <v-row align="start" justify="center" class="position-relative mt-4">
      
      <!-- Step 1, 2, 3 Loop -->
      <v-col
        v-for="(step, index) in steps"
        :key="index"
        cols="12"
        md="4"
        class="d-flex flex-column align-center px-6 position-relative"
      >
        <!-- Number Circle -->
        <div
          class="d-flex align-center justify-center rounded-circle font-weight-bold mb-8"
          style="
            width: 56px;
            height: 56px;
            background-color: #ffffff;
            color: #064229;
            font-size: 1.2rem;
            z-index: 2;
          "
        >
          {{ index + 1 }}
        </div>

        <!-- Dashed Connector (Visible on Desktop only) -->
        <div
          v-if="index < steps.length - 1"
          class="hidden-sm-and-down"
          style="
            position: absolute;
            top: 28px;
            left: 60%;
            width: 80%;
            border-top: 2px dashed #064229;
            opacity: 0.3;
            z-index: 1;
          "
        >
          <v-icon 
            icon="mdi-chevron-right" 
            style="position: absolute; right: -10px; top: -12px; color: #064229;"
          ></v-icon>
        </div>

        <!-- Step Content -->
        <h3
          class="text-h6 font-weight-bold mb-2"
          style="color: #064229;"
        >
          {{ step.title }}
        </h3>
        <p
          class="text-body-2"
          style="
            color: #064229;
            line-height: 1.6;
            opacity: 0.8;
            max-width: 250px;
          "
        >
          {{ step.description }}
        </p>
      </v-col>

    </v-row>
  </v-container>
</section>


    <!-- CTA SECTION -->
<section id="services" class="cta-section py-16" style="background-color: #ffffff;">
      <v-container class="text-center">
        <!-- Pill Badge -->
        <v-chip
          size="small"
          class="mb-6 font-weight-bold text-uppercase"
          variant="flat"
          style="background-color: #E9F4C2; color: #064229; letter-spacing: 1px;"
        >
          Get Started
        </v-chip>

        <h2
          class="font-weight-bold text-uppercase mb-4"
          style="
            font-size: clamp(2rem, 4vw, 3rem);
            line-height: 1.1;
            color: #064229;
            max-width: 600px;
            margin: 0 auto;
            letter-spacing: -0.02em;
          "
        >
          READY TO GET YOUR<br />TEAM ORGANISED?
        </h2>

        <!-- Descriptive Text -->
        <p 
          class="mb-10 mx-auto" 
          style="color: #064229; max-width: 600px; opacity: 0.9;"
        >
          Sign in with your company credentials to access your dashboard 
          and start streamlining your workflows today.
        </p>

        <!-- Dark Forest Button -->
        <v-btn 
          size="x-large" 
          rounded="pill" 
          elevation="0"
          class="px-10 text-none font-weight-bold"
          to="/login"
          style="background-color: #064229; color: #D4E97D;"
        >
          Sign in to your account
          <v-icon end icon="mdi-arrow-right" class="ms-2"></v-icon>
        </v-btn>
      </v-container>
    </section>
  </div>
</template>

<style scoped>
.hero-section {
  position: relative;
  overflow: hidden;
}

.heading-text {
  font-weight: 800;
  font-size: clamp(2.5rem, 8vw, 4.5rem);
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.hero-background {
  height: 100vh;
  min-height: 600px;
}

/* This creates the dark green fade from the left */
.side-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg, 
    rgba(1, 48, 24, 0.95) 0%, 
    rgba(1, 48, 24, 0.7) 50%, 
    rgba(1, 48, 24, 0.3) 100%
  );
  z-index: 1;
}

.max-width-600 {
  max-width: 600px;
}

.fill-height {
  position: relative;
  z-index: 2;
}

.line-height-tight {
  line-height: 1.05 !important;
  letter-spacing: -2px !important;
}

.opacity-90 {
  opacity: 0.9;
}

@media (max-width: 960px) {
  .hero-section {
    min-height: 100vh;
  }
  
  .side-overlay {
    background: linear-gradient(
      to bottom,
      rgba(1, 48, 24, 0.8) 0%,
      rgba(1, 48, 24, 0.9) 100%
    );
  }

  .heading-text {
    letter-spacing: -1px !important;
  }
}

.stats-card {
  border-radius: 12px;
}

.feature-card {
  border-radius: 12px;
  border: 1px solid black;
}

.step-line {
  width: 2px;
  background-color: #e0e0e0;
  min-height: 40px;
}

.gap-4 {
  gap: 16px;
}
</style>
