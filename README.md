Description:

We are having problems with the maximum number of H.264 video hardware decoding through d3d11 with GStreamer

We are seeing that the limit for an i7 8gen or upper with a iGPU (i7-8550U) is much smaller than for an i7 7gen or lower (i7-7500U or i7-6600U).

It seems that the newer generations of the iGPU have less simultaneous playback capacity in Windows than the older ones.

Running the next pipeline (check `create_pipeline.py` to generate it):
```
gst-launch-1.0.exe --gst-debug-level=3 \
filesrc location="$VIDEO" ! qtdemux ! h264parse ! queue ! d3d11h264dec ! "video/x-raw(memory:D3D11Memory)" ! queue ! d3d11videosink \
...20 time more...
filesrc location="$VIDEO" ! qtdemux ! h264parse ! queue ! d3d11h264dec ! "video/x-raw(memory:D3D11Memory)" ! queue ! d3d11videosink
```

The error is (full error in `full_error.log`):
```
0:00:25.265373000 10388 000002DCDCA7F6C0 INFO         d3d11debuglayer gstd3d11memory.cpp:1232:gst_d3d11_memory_ensure_processor_output_view:<d3d11device2> D3D11InfoQueue: Create ID3D11VideoProcessorOutputView: Name="unnamed", Addr=0x000002DCFF4F5290, ExtRef=1, IntRef=0
0:00:25.323520000 10388 000002DCDCA7F6C0 WARN             d3d11window gstd3d11window_win32.cpp:1079:gst_d3d11_window_win32_present: D3D11 call failed: 0x887a0005, The GPU device instance has been suspended. Use GetDeviceRemovedReason to determine the appropriate action.
0:00:25.324161000 10388 000002DCDCA7F6C0 INFO         d3d11debuglayer gstd3d11window_win32.cpp:1079:gst_d3d11_window_win32_present:<d3d11device2> D3D11InfoQueue: ID3D11Device::RemoveDevice: Device removal has ben triggered for the following reason (DXGI_ERROR_DEVICE_RESET: The hardware took an unreasonable amount of time to execute a command on a different Device Context, or the hardware crashed/hung. As a result, the TDR (Timeout Detection and Recovery) mechanism has been triggered. The current Device Context was NOT executing commands when the hang occurred. However, the current video memory and Device Context could not be completely recovered. The application may want to just respawn itself, as the other application may no longer be around to cause this again).
0:00:25.324839000 10388 000002DCDCA7F6C0 WARN             d3d11window gstd3d11window_win32.cpp:1081:gst_d3d11_window_win32_present:<d3d11windowwin32-20> Direct3D cannot present texture, hr: 0x887a0005
```


Attached you can find info about an i7-8550U with the issue and i7-6600U that works correctly, and all simple pipeline to reprodice the issue.


Other tests:

1. 25 HTML video players using hardware decoding with a chromium based browser works smoothly. It's not a fair comparation because the player inside the browser has other performance improvements. (See `chromium/index.html`)  
2. The issue is the same running 25 gst-launch-1.0.exe process with only one pipeline instead of one process with 25 bins.  
3. The limit in Windows with d3d11 is much smaller than for Linux using libva with the same Hardware (to double-check).  
4. If the host also has a dGPU, the decoding performance in the iGPU 8gen+ can be improved setting the correct Graphic settings (in the registry `GpuPreference=0;` to `gst-launch-1.0.exe` in `Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\DirectX\UserGpuPreferences`. See `imgs/regedit_UserGpuPreferences.png`)  

Similar issues/patches:

1. https://chromium-review.googlesource.com/c/chromium/src/+/3764316
2. https://bugs.chromium.org/p/chromium/issues/detail?id=527565 and https://github.com/chromium/chromium/commit/ed27437d3a0a58534dd6cb877b18d2d60d1d21fe
3. full list in https://github.com/chromium/chromium/blob/main/gpu/config/gpu_driver_bug_list.json

Links:

* https://devblogs.microsoft.com/directx/d3dconfig-a-new-tool-to-manage-directx-control-panel-settings/

Fluendo internal Issue: CS-586
