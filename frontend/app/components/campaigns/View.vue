
<template>
  <UCard class="shadow-sm">
    <template #header>
      <div class="flex justify-between items-center">
        <div></div> <!-- Empty div to maintain flex spacing -->
        <div class="flex items-center gap-2">
          <CampaignsActionsCreate />
        </div>
      </div>
      <div class="space-y-4">
        <CampaignsTable />
      </div>
    </template>
  </UCard>
</template>
