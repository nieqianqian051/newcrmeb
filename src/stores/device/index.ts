import { defineStore } from 'pinia';
import type { Device } from '../types/device';

export const useDeviceStore = defineStore('device', {
  state: () => ({
    devices: [] as Device[],
    groups: [] as string[]
  }),
  actions: {
    addDevice(device: Device) {
      this.devices.push(device);
      if (device.group && !this.groups.includes(device.group)) {
        this.groups.push(device.group);
      }
    },
    removeDevice(id: string) {
      const index = this.devices.findIndex(d => d.id === id);
      if (index > -1) {
        this.devices.splice(index, 1);
      }
    },
    updateDevice(id: string, updates: Partial<Device>) {
      const device = this.devices.find(d => d.id === id);
      if (device) {
        Object.assign(device, updates);
      }
    }
  }
});
