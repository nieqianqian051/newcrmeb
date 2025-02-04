import { ref } from '@vue/runtime-core';
import type { Device } from '../types/device';

const MOCK_DEVICES = [
  { id: 'light1', name: 'Living Room Light', type: 'light', status: 'online' },
  { id: 'ac1', name: 'Bedroom AC', type: 'ac', status: 'online' },
  { id: 'tv1', name: 'Smart TV', type: 'tv', status: 'offline' },
  { id: 'curtain1', name: 'Living Room Curtain', type: 'curtain', status: 'online' }
] as const;

export function useDeviceDiscovery() {
  const discoveredDevices = ref<Device[]>([]);
  const isScanning = ref(false);

  const startDiscovery = () => {
    isScanning.value = true;
    discoveredDevices.value = [];
    
    // Simulate device discovery with delays
    let index = 0;
    const discoveryInterval = setInterval(() => {
      if (index < MOCK_DEVICES.length) {
        discoveredDevices.value.push({
          ...MOCK_DEVICES[index],
          id: `${MOCK_DEVICES[index].id}-${Date.now()}`
        });
        index++;
      } else {
        clearInterval(discoveryInterval);
        isScanning.value = false;
      }
    }, 1000);
  };

  const stopDiscovery = () => {
    isScanning.value = false;
  };

  return {
    discoveredDevices,
    isScanning,
    startDiscovery,
    stopDiscovery
  };
}
