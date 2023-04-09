使用Python 编写的一款命令行记账软件

## 使用方法

+ key: 
-    bill  账单
-    config 配置项
-    fund   年初余额
+ value:
-    --all -a 查看全部  [<key> --all]
-    --all -a 按照条件查看  [<key> --all <cloumn=value> <cloumn2=value2>]
-    --mod -m 修改     [<key> --mod <id> <cloumn=value> <cloumn2=value2>]
-    --del -r 删除     [<key> --del <id>]
-    --new -n 增加     [<key> --new <value> <value2>]
-    --upload -u 导入  [<key> --upload]
-    --down -dl 导入   [<key> --down <可选><cloumn=value>]
+ 以下当 key 为 config时
-    --disable -d 禁用 [<key> --disable <value>]
-    --enable  -e 启用 [<key> --disable <value>]

