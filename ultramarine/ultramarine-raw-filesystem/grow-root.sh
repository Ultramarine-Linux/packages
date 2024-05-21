#!/bin/bash

echo "Resize Root Partition"
root_device=$(lsblk -no UUID,MOUNTPOINT | grep " /$" | awk '{print $1}')
growpart $root_device
resize2fs $root_device
echo "Resized Root Partition"