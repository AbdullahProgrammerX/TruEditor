<script setup lang="ts">
/**
 * TruEditor - New Submission Wizard
 * ==================================
 * 6-step manuscript submission wizard.
 * (Placeholder - Will be detailed in Phase 5)
 */
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentStep = ref(1)
const totalSteps = 6

const steps = [
  { id: 1, title: 'Article Type', icon: '📋' },
  { id: 2, title: 'File Upload', icon: '📁' },
  { id: 3, title: 'Article Details', icon: '📝' },
  { id: 4, title: 'Authors', icon: '👥' },
  { id: 5, title: 'Reviewer Suggestions', icon: '🔍' },
  { id: 6, title: 'Confirmation', icon: '✓' },
]

// Safe computed property to get current step data
const currentStepData = computed(() => {
  return steps[currentStep.value - 1] ?? { id: 0, title: '', icon: '' }
})

function goBack() {
  if (currentStep.value > 1) {
    currentStep.value--
  } else {
    router.push('/dashboard')
  }
}

function goNext() {
  if (currentStep.value < totalSteps) {
    currentStep.value++
  }
}

function submit() {
  // Submit logic will be implemented in Phase 5
  ;(window as any).toast?.('success', 'Submission successful! (Demo)')
  router.push('/dashboard')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-40">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <button @click="goBack" class="btn-ghost">
            ← Back
          </button>
          <h1 class="text-lg font-semibold text-gray-800">New Manuscript Submission</h1>
          <div class="w-20"></div>
        </div>
      </div>
    </header>

    <!-- Progress Stepper -->
    <div class="bg-white border-b">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div 
            v-for="(step, index) in steps" 
            :key="step.id"
            class="flex items-center"
          >
            <!-- Step circle -->
            <div 
              class="flex items-center justify-center w-10 h-10 rounded-full text-sm font-medium transition-all"
              :class="[
                step.id < currentStep ? 'bg-accent-500 text-white' : 
                step.id === currentStep ? 'bg-primary-500 text-white' : 
                'bg-gray-100 text-gray-400'
              ]"
            >
              <span v-if="step.id < currentStep">✓</span>
              <span v-else>{{ step.icon }}</span>
            </div>
            
            <!-- Step title (hidden on mobile) -->
            <span 
              class="ml-2 text-sm font-medium hidden lg:block"
              :class="step.id <= currentStep ? 'text-gray-800' : 'text-gray-400'"
            >
              {{ step.title }}
            </span>
            
            <!-- Connector line -->
            <div 
              v-if="index < steps.length - 1"
              class="w-8 lg:w-16 h-0.5 mx-2 lg:mx-4"
              :class="step.id < currentStep ? 'bg-accent-500' : 'bg-gray-200'"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Step Content -->
    <main class="max-w-4xl mx-auto px-6 py-8">
      <div class="card animate-fade-in">
        <h2 class="text-2xl font-bold text-gray-800 mb-2">
          {{ currentStepData.icon }} {{ currentStepData.title }}
        </h2>
        
        <div class="py-12 text-center text-gray-500">
          <p class="text-lg mb-4">This step will be developed in Phase 5.</p>
          <p class="text-sm">Step {{ currentStep }} / {{ totalSteps }}</p>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex justify-between mt-6">
        <button 
          @click="goBack"
          class="btn-outline"
        >
          ← Previous
        </button>
        
        <button 
          v-if="currentStep < totalSteps"
          @click="goNext"
          class="btn-primary"
        >
          Next →
        </button>
        
        <button 
          v-else
          @click="submit"
          class="btn-primary bg-accent-500 hover:bg-accent-600"
        >
          ✓ Submit
        </button>
      </div>
    </main>
  </div>
</template>
