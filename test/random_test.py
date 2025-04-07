import sys
import subprocess
import shutil
import random

class SampleTester:
    def __init__(self, src1, src2):
        self.src1 = src1
        self.src2 = src2
    
    def run(self, src, sample):
        """プログラムを実行"""
        try:
            process = subprocess.Popen(
                ["python", src],  # 実行する Python スクリプト
                stdin=subprocess.PIPE,     # 標準入力をパイプで渡す
                stdout=subprocess.PIPE,    # 標準出力をパイプで受け取る
                stderr=subprocess.PIPE     # 標準エラーをパイプで受け取る
            )

            # 入力データを渡して実行
            stdout, stderr = process.communicate(input=sample.encode(),timeout=5)
        except subprocess.TimeoutExpired:
            stdout, stderr = bytes(), bytes()
            process.kill()
        
        return stdout, stderr
    
    def ok(self, output1, output2, stderr1, stderr2):
        if stderr1 or stderr2:
            return False
        return output1.split() == output2.split()
    
    def test(self):
        generater = SampleGenerater()
        simulate_count = 0
        while True:
            sample = generater.generate()
            stdout1, stderr1 = self.run(self.src1, sample)
            stdout2, stderr2 = self.run(self.src2, sample)
            output1 = stdout1.decode(errors='ignore')
            output2 = stdout2.decode(errors='ignore')
            err1 = stderr1.decode(errors='ignore')
            err2 = stderr2.decode(errors='ignore')

            if self.ok(output1, output2, stderr1, stderr2):
                simulate_count += 1
                if simulate_count % 10 == 0:
                    print(f'ok x{simulate_count}')
                continue
            print(f'ok x{simulate_count}')
            return sample, output1, output2, err1, err2

class SampleGenerater:
    def __init__(self):
        self.sample = []

    def change(self, sample):
        """2次元配列を文字列に変換"""
        string = []
        for i in sample:
            for val in i:
                string.append(str(val)+" ")
            string.append("\n")
        return ''.join(string)
    
    def generate(self):
        self.sample = []
        self.make()
        return self.change(self.sample)
    
    
    def _make_int(self,lower,upper):
        return random.randint(lower,upper)

    def _make_float(self,lower,upper):
        return random.uniform(lower,upper)
    
    def _make_upper_string(self, n):
        return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ",n))
    
    def _make_lower_string(self, n):
        return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz",n))

    def _make_1d_array(self, lower, upper, n):
        return [random.randint(lower,upper) for _ in range(n)]

    def _make_2d_array(self, lower, upper, n, m):
        return [[random.randint(lower,upper) for _ in range(m)] for _ in range(n)]
    
    #--メソッド一覧-------------------------------------------
    
    def make_int(self,lower,upper):
        """int型を1つ"""
        return self._make_int(lower,upper)
    
    def make_float(self,lower,upper):
        """float型をひとつ"""
        return self._make_float(lower,upper)
    
    def make_upper_string(self, n):
        """長さｎの大文字の文字列"""
        return self._make_upper_string(n)
    
    def make_lower_string(self, n):
        """長さｎの小文字の文字列"""
        return self._make_lower_string(n)

    def make_1d_array(self, lower, upper, n):
        """要素がlower以上upper以下、長さnの1次元配列"""
        return self._make_1d_array(lower,upper,n)

    def make_2d_array(self, lower, upper, n, m):
        """要素がlower以上upper以下、n*mの2次元配列"""
        return self._make_2d_array(lower,upper,n,m)

    def make(self):
        """
        ここを書き換える。
        sampleが2次元配列になるようにsampleにいれる
        """
        n = self.make_int(1,10000)
        self.sample.append([n])


def main():
    args = sys.argv
    terminal_width = shutil.get_terminal_size().columns
    tester = SampleTester(args[1], args[2])
    sample, output1, output2, err1, err2 = tester.test()
    print("\nSample\n" + "\033[33m-"*terminal_width + "\033[37m")
    print(sample)
    
    print("output1\n" + "\033[33m-"*terminal_width + "\033[37m")
    print(output1)
    print(err1)

    print("output2\n" + "\033[33m-"*terminal_width + "\033[37m")
    print(output2)
    print(err2)


if __name__ == '__main__':
    main()