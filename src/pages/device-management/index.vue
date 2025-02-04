<script setup lang="ts">
import { ref } from 'vue';
import { useDeviceStore } from '@/stores/device';
import { Device } from '@/types/device';
import DeviceCard from '@/components/device/DeviceCard.vue';

const deviceStore = useDeviceStore();
const showAddDialog = ref(false);
const newDevice = ref<Partial<Device>>({
  name: '',
  type: 'light',
  status: 'offline'
});

const handleAddDevice = () => {
  if (newDevice.value.name) {
    deviceStore.addDevice({
      id: Date.now().toString(),
      name: newDevice.value.name,
      type: newDevice.value.type as Device['type'],
      status: newDevice.value.status as Device['status'],
      group: newDevice.value.group
    });
    showAddDialog.value = false;
    newDevice.value = { name: '', type: 'light', status: 'offline' };
  }
};

const handleEditDevice = (device: Device) => {
  uni.showModal({
    title: '编辑设备',
    content: '功能开发中...',
    showCancel: false
  });
};

const handleDeleteDevice = (device: Device) => {
  uni.showModal({
    title: '删除设备',
    content: '确定要删除该设备吗？',
    success: (res) => {
      if (res.confirm) {
        deviceStore.removeDevice(device.id);
      }
    }
  });
};
</script>

<template>
  <view class="container">
    <view class="header">
      <text class="title">设备管理</text>
      <button @tap="showAddDialog = true" type="primary">添加设备</button>
    </view>

    <view class="device-list">
      <DeviceCard
        v-for="device in deviceStore.devices"
        :key="device.id"
        :device="device"
        @edit="handleEditDevice"
        @delete="handleDeleteDevice"
      />
    </view>

    <uni-popup v-model:show="showAddDialog" type="dialog">
      <uni-popup-dialog
        mode="input"
        title="添加设备"
        placeholder="设备名称"
        :value="newDevice.name"
        @confirm="handleAddDevice"
      />
    </uni-popup>
  </view>
</template>

<style>
.container {
  padding: 16px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.title {
  font-size: 20px;
  font-weight: bold;
}
.device-list {
  display: flex;
  flex-direction: column;
}
</style>
