

class A:
    a = 1
    def aa(self):
        sum = self.a+1                    # 自己类里的变量要用self.来调用
        self.stra = 'bb方法需要用到的变量'   # 需要同类其他方法用到的变量用self.来存放
        return sum*5
    def bb(self):
        """直接通过‘self.aa()’来调用获取返回值"""
        b = self.aa()       # 自己类的方法也用self.来调用
        print(b)
        strb = '合并后的strb字符串：'+ self.stra
        print(strb)
if __name__ == '__main__':
    A().bb()
