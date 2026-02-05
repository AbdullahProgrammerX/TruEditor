<script setup lang="ts">
/**
 * TruEditor - Skeleton Loader Component
 * ======================================
 * Animated skeleton loading placeholder with shimmer effect.
 */

interface Props {
  /** Type of skeleton to render */
  type?: 'text' | 'card' | 'table' | 'avatar' | 'button' | 'custom'
  /** Number of lines (for text type) */
  lines?: number
  /** Number of rows (for table type) */
  rows?: number
  /** Width class (e.g., 'w-full', 'w-32') */
  width?: string
  /** Height class (e.g., 'h-4', 'h-12') */
  height?: string
  /** Whether to show animation */
  animate?: boolean
  /** Circle shape (for avatar) */
  circle?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  lines: 3,
  rows: 5,
  width: 'w-full',
  height: 'h-4',
  animate: true,
  circle: false,
})

// Generate random widths for text lines
const lineWidths = ['w-full', 'w-3/4', 'w-5/6', 'w-2/3', 'w-4/5']
const getRandomWidth = (index: number) => lineWidths[index % lineWidths.length]
</script>

<template>
  <!-- Text Skeleton -->
  <div v-if="type === 'text'" class="space-y-3">
    <div
      v-for="i in lines"
      :key="i"
      class="skeleton-line"
      :class="[
        i === lines ? 'w-1/2' : getRandomWidth(i),
        height,
        { 'animate-shimmer': animate }
      ]"
    />
  </div>

  <!-- Card Skeleton -->
  <div v-else-if="type === 'card'" class="bg-white rounded-lg border border-gray-100 p-6">
    <div class="flex items-start gap-4">
      <!-- Avatar -->
      <div 
        class="skeleton-line w-12 h-12 rounded-full flex-shrink-0"
        :class="{ 'animate-shimmer': animate }"
      />
      <div class="flex-1 space-y-3">
        <!-- Title -->
        <div 
          class="skeleton-line h-5 w-3/4"
          :class="{ 'animate-shimmer': animate }"
        />
        <!-- Subtitle -->
        <div 
          class="skeleton-line h-4 w-1/2"
          :class="{ 'animate-shimmer': animate }"
        />
      </div>
    </div>
    <div class="mt-4 space-y-2">
      <div 
        class="skeleton-line h-4 w-full"
        :class="{ 'animate-shimmer': animate }"
      />
      <div 
        class="skeleton-line h-4 w-5/6"
        :class="{ 'animate-shimmer': animate }"
      />
    </div>
  </div>

  <!-- Table Skeleton -->
  <div v-else-if="type === 'table'" class="space-y-3">
    <!-- Header -->
    <div class="flex gap-4 pb-3 border-b border-gray-100">
      <div 
        class="skeleton-line h-4 w-1/4"
        :class="{ 'animate-shimmer': animate }"
      />
      <div 
        class="skeleton-line h-4 w-1/3"
        :class="{ 'animate-shimmer': animate }"
      />
      <div 
        class="skeleton-line h-4 w-1/6"
        :class="{ 'animate-shimmer': animate }"
      />
      <div 
        class="skeleton-line h-4 w-1/6"
        :class="{ 'animate-shimmer': animate }"
      />
    </div>
    <!-- Rows -->
    <div 
      v-for="i in rows" 
      :key="i" 
      class="flex gap-4 py-3 border-b border-gray-50"
      :style="{ animationDelay: `${i * 50}ms` }"
    >
      <div 
        class="skeleton-line h-4 w-1/4"
        :class="{ 'animate-shimmer': animate }"
        :style="{ animationDelay: `${i * 50}ms` }"
      />
      <div 
        class="skeleton-line h-4 w-1/3"
        :class="{ 'animate-shimmer': animate }"
        :style="{ animationDelay: `${i * 50 + 25}ms` }"
      />
      <div 
        class="skeleton-line h-4 w-1/6"
        :class="{ 'animate-shimmer': animate }"
        :style="{ animationDelay: `${i * 50 + 50}ms` }"
      />
      <div 
        class="skeleton-line h-4 w-1/6"
        :class="{ 'animate-shimmer': animate }"
        :style="{ animationDelay: `${i * 50 + 75}ms` }"
      />
    </div>
  </div>

  <!-- Avatar Skeleton -->
  <div 
    v-else-if="type === 'avatar'" 
    class="skeleton-line"
    :class="[
      width,
      height,
      circle ? 'rounded-full' : 'rounded-lg',
      { 'animate-shimmer': animate }
    ]"
  />

  <!-- Button Skeleton -->
  <div 
    v-else-if="type === 'button'" 
    class="skeleton-line rounded-lg"
    :class="[
      width || 'w-24',
      height || 'h-10',
      { 'animate-shimmer': animate }
    ]"
  />

  <!-- Custom Skeleton -->
  <div 
    v-else
    class="skeleton-line"
    :class="[
      width,
      height,
      circle ? 'rounded-full' : 'rounded',
      { 'animate-shimmer': animate }
    ]"
  />
</template>

<style scoped>
.skeleton-line {
  background: linear-gradient(90deg, #e5e7eb 25%, #f3f4f6 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  background-color: #e5e7eb;
  border-radius: 0.25rem;
}

.animate-shimmer {
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
