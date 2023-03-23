using System.Diagnostics;

namespace LR_3
{
    internal class Program
    {
        const int ThreadsCount = 5;
        static void Main()
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            List<string> ReaderBuf = new List<string>();
            string? buffer = null;
            bool finish = false;

            Thread[] reader = new Thread[ThreadsCount];
            for (int k = 0; k < reader.Length; k++)
                reader[k] = new Thread(() =>
                {
                    while (!finish || buffer != null)
                    {
                        if (buffer != null)
                        {
                            string old_value = Interlocked.Exchange(ref buffer, null);
                            if (old_value != null)
                            {
                                lock (ReaderBuf) ;
                                ReaderBuf.Add(old_value);
                            }
                        }
                    }
                });

            Thread[] writer = new Thread[ThreadsCount];
            for (int k = 0; k < writer.Length; k++)
            {
                int k_copy = k;
                writer[k] = new Thread(() =>
                {
                    string[] WriterBuf = {
                        $"Сообщение A из потока #{k_copy}",
                        $"Сообщение B из потока #{k_copy}",
                        $"Сообщение C из потока #{k_copy}"
                    };
                    for (int i = 0; i < WriterBuf.Length;)
                        if (Interlocked.CompareExchange(ref buffer, WriterBuf[i], null) == null) i++;
                });
            }

            foreach (Thread w in writer) w.Start();
            foreach (Thread r in reader) r.Start();

            foreach (Thread w in writer) w.Join();
            finish = true;
            foreach (Thread r in reader) r.Join();

            foreach (string str in ReaderBuf.OrderBy(r => r))
                Console.WriteLine(str);

            stopwatch.Stop();

            Console.WriteLine($"Время работы программы: {stopwatch.ElapsedMilliseconds}");
        }
    }
}