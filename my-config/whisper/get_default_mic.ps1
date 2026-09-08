# Prints the friendly name of the Windows default capture device.
# WSLg mirrors this device into WSL2 as "RDPSource", so this names the
# microphone actually feeding the Whisper server. Used by whisper_mode.py.
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public class DefaultMic {
    [ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorComObject { }
    [Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface IMMDeviceEnumerator {
        int EnumAudioEndpoints(int dataFlow, int stateMask, out IntPtr devices);
        int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice endpoint);
    }
    [Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface IMMDevice {
        int Activate(ref Guid id, int clsCtx, IntPtr activationParams, out IntPtr iface);
        int OpenPropertyStore(int stgmAccess, out IPropertyStore properties);
    }
    [Guid("886d8eeb-8cf2-4446-8d02-cdba1dbdcf99"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface IPropertyStore {
        int GetCount(out int count);
        int GetAt(int index, out PropertyKey key);
        int GetValue(ref PropertyKey key, out PropVariant value);
    }
    [StructLayout(LayoutKind.Sequential)] struct PropertyKey { public Guid fmtid; public int pid; }
    [StructLayout(LayoutKind.Explicit)] struct PropVariant {
        [FieldOffset(0)] public short vt;
        [FieldOffset(8)] public IntPtr pointerValue;
    }
    public static string GetName() {
        var enumerator = (IMMDeviceEnumerator)(object)new MMDeviceEnumeratorComObject();
        IMMDevice device;
        enumerator.GetDefaultAudioEndpoint(1, 0, out device); // eCapture, eConsole
        IPropertyStore store;
        device.OpenPropertyStore(0, out store);
        var friendlyName = new PropertyKey { fmtid = new Guid("a45c254e-df1c-4efd-8020-67d146a850e0"), pid = 14 };
        PropVariant value;
        store.GetValue(ref friendlyName, out value);
        return Marshal.PtrToStringUni(value.pointerValue);
    }
}
'@
[DefaultMic]::GetName()
