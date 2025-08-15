using System.Runtime.InteropServices;
using System;
using System.IO;
using System.Security.Cryptography;

namespace RunDLL
{
    class Run
    {
        // Delegate that matches your DLL function signature
        [UnmanagedFunctionPointer(CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public delegate void PrintMsgDelegate(string msg);

        static void Main(string[] args)
        {
            const string EXPECTED_HASH = "14d56968fcfc281cf538b9b6a570c52f";
            string dllPath = Path.Combine(Directory.GetCurrentDirectory(), "test.dll");

            Console.WriteLine("Attempting to execute DLL...\n");

            if (!File.Exists(dllPath))
            {
                Console.WriteLine($"DLL not found at {dllPath}");
                return;
            }

            if (GetFileHash(dllPath) != EXPECTED_HASH)
            {
                Console.WriteLine($"DLL Tampering Detected...");
                return;
            }


                IntPtr handle = IntPtr.Zero;
            try
            {
                // Load the DLL dynamically
                handle = NativeLibrary.Load(dllPath);

                // Get pointer to the function "printMsg"
                IntPtr funcPtr = NativeLibrary.GetExport(handle, "printMsg");

                // Create a delegate for the function pointer
                PrintMsgDelegate printMsg = Marshal.GetDelegateForFunctionPointer<PrintMsgDelegate>(funcPtr);

                // Use console color for output
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("DLL Output");
                Console.WriteLine("----------------------");

                // Call the function
                printMsg("Hello From My DLL");
                printMsg("----------------------");

                Console.ResetColor();
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error: {e.Message}");
            }
            finally
            {
                // Free the DLL if it was loaded
                if (handle != IntPtr.Zero)
                    NativeLibrary.Free(handle);

                Console.ResetColor();
                Console.WriteLine("\nFinished attempting to execute test.dll...");
            }
        }

        private static string GetFileHash(string path)
        {
            using var hash = SHA256.Create();
            using var stream = File.OpenRead(path);
            var sha256Hash = hash.ComputeHash(stream);
            return Convert.ToHexStringLower(sha256Hash);
        }
    }
}