using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Threading;
using System.Windows.Forms;

namespace MolyLauncher
{
    static class Program
    {
        private static bool IsPortOpen(string host, int port)
        {
            try
            {
                using (var client = new TcpClient())
                {
                    var result = client.BeginConnect(host, port, null, null);
                    bool success = result.AsyncWaitHandle.WaitOne(300);
                    if (!success) return false;
                    client.EndConnect(result);
                    return true;
                }
            }
            catch
            {
                return false;
            }
        }

        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            string ruffleExe = Path.Combine(baseDir, "tools", "ruffle-0.7.1", "ruffle.exe");
            if (!File.Exists(ruffleExe))
            {
                ruffleExe = Path.Combine(baseDir, "ruffle.exe");
            }

            if (!File.Exists(ruffleExe))
            {
                MessageBox.Show(
                    "Không tìm thấy công cụ chạy game Flash (ruffle.exe).\nVui lòng giải nén toàn bộ thư mục và không xóa tệp trong thư mục 'tools'.",
                    "Moly - Thế Giới Chuột Chũi VN",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
                return;
            }

            Process assetProcess = null;
            Process serverProcess = null;

            // 1. Khởi động Proxy tài nguyên (Port 18080) nếu chưa chạy
            if (!IsPortOpen("127.0.0.1", 18080))
            {
                string proxyScript = Path.Combine(baseDir, "tools", "capture_proxy.py");
                string assetScript = Path.Combine(baseDir, "tools", "client_asset_server.py");
                string chosenScript = File.Exists(proxyScript) ? proxyScript : assetScript;

                if (File.Exists(chosenScript))
                {
                    string args = "";
                    if (chosenScript == proxyScript)
                    {
                        args = "tools\\capture_proxy.py --archive archive\\clients\\captured-live --host 127.0.0.1 --port 18080 --local-server 127.0.0.1 --overrides archive\\clients\\local-overrides --mirror archive\\clients\\offline-mirror";
                    }
                    else
                    {
                        args = "tools\\client_asset_server.py --port 18080";
                    }

                    var psi = new ProcessStartInfo
                    {
                        FileName = "pythonw.exe",
                        Arguments = args,
                        WorkingDirectory = baseDir,
                        CreateNoWindow = true,
                        UseShellExecute = false,
                        WindowStyle = ProcessWindowStyle.Hidden
                    };

                    try
                    {
                        assetProcess = Process.Start(psi);
                    }
                    catch
                    {
                        psi.FileName = "python.exe";
                        try { assetProcess = Process.Start(psi); } catch { }
                    }

                    for (int i = 0; i < 15; i++)
                    {
                        if (IsPortOpen("127.0.0.1", 18080)) break;
                        Thread.Sleep(200);
                    }
                }
            }

            // 2. Khởi động máy chủ Probe Server nếu có trong thư mục (nếu chơi bản offline)
            if (!IsPortOpen("127.0.0.1", 1863))
            {
                string probeScript = Path.Combine(baseDir, "tools", "moly_probe_server.py");
                if (File.Exists(probeScript))
                {
                    var psiServer = new ProcessStartInfo
                    {
                        FileName = "pythonw.exe",
                        Arguments = "tools\\moly_probe_server.py --log data\\server\\probe-events.jsonl",
                        WorkingDirectory = baseDir,
                        CreateNoWindow = true,
                        UseShellExecute = false,
                        WindowStyle = ProcessWindowStyle.Hidden
                    };
                    try
                    {
                        serverProcess = Process.Start(psiServer);
                    }
                    catch
                    {
                        psiServer.FileName = "python.exe";
                        try { serverProcess = Process.Start(psiServer); } catch { }
                    }
                    for (int i = 0; i < 15; i++)
                    {
                        if (IsPortOpen("127.0.0.1", 1863)) break;
                        Thread.Sleep(200);
                    }
                }
            }

            // 3. Khởi động Cửa sổ trò chơi qua Ruffle
            string clientSwf = "http://127.0.0.1:18080/Client.swf";
            string ruffleArgs = string.Format(
                "\"{0}\" --tcp-connections allow --open-url-mode allow --scale show-all --force-scale --width 1024 --height 768",
                clientSwf
            );

            var rufflePsi = new ProcessStartInfo
            {
                FileName = ruffleExe,
                Arguments = ruffleArgs,
                WorkingDirectory = baseDir,
                UseShellExecute = false
            };

            try
            {
                using (var gameProc = Process.Start(rufflePsi))
                {
                    if (gameProc != null)
                    {
                        gameProc.WaitForExit();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi khi khởi chạy trò chơi: " + ex.Message,
                    "Moly - Thế Giới Chuột Chũi VN",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
            finally
            {
                try
                {
                    if (assetProcess != null && !assetProcess.HasExited)
                    {
                        assetProcess.Kill();
                    }
                }
                catch { }

                try
                {
                    if (serverProcess != null && !serverProcess.HasExited)
                    {
                        serverProcess.Kill();
                    }
                }
                catch { }
            }
        }
    }
}
