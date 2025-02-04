<script setup lang="ts">
import { Device } from '@/types/device';

defineProps<{
  device: Device;
  onEdit?: (device: Device) => void;
  onDelete?: (device: Device) => void;
}>();
</script>

<template>
  <view class="device-card">
    <view class="device-header">
      <text class="device-name">{{ device.name }}</text>
      <text :class="['device-status', device.status]">{{ device.status }}</text>
    </view>
    <view class="device-info">
      <text class="device-type">{{ device.type }}</text>
      <text v-if="device.group" class="device-group">{{ device.group }}</text>
    </view>
    <view class="device-actions">
      <button @tap="onEdit?.(device)" type="primary" size="mini">编辑</button>
      <button @tap="onDelete?.(device)" type="warn" size="mini">删除</button>
    </view>
  </view>
</template>

<style>
.device-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.device-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.device-name {
  font-size: 16px;
  font-weight: bold;
}
.device-status {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
}
.device-status.online {
  background: #e6f7e9;
  color: #52c41a;
}
.device-status.offline {
  background: #fff1f0;
  color: #ff4d4f;
}
.device-info {
  margin-bottom: 12px;
}
.device-type, .device-group {
  font-size: 14px;
  color: #666;
  margin-right: 8px;
}
.device-actions {
  display: flex;
  gap: 8px;
}
</style>
