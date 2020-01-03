MySQL索引
===============
索引是一种特殊的文件(InnoDB数据表上的索引是表空间的一个组成部分)，它们包含着对数据表里所有记录的引用指针。更通俗的说，数据库索引好比是一本书前面的目录，能加快数据库的查询速度。在没有索引的情况下，做查询操作的时候数据库会遍历全部数据后选择符合条件的；而有索引之后，数据库会直接在索引中查找符合条件的选项。如果SQL语句换SELECT * FROM article WHERE id=2000000”，那么在没有索引时（注：一般数据库默认都会为主键生成索引）数据库按照顺序读取完200万行数据。  
####查看索引

    show index from TABLE_NAME
    比如:
    show index from blog_blog;
    返回:
    +-----------+------------+--------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+
    | Table     | Non_unique | Key_name           | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type |
    +-----------+------------+--------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+
    | blog_blog |          0 | PRIMARY            |            1 | id          | A         |           5 |     NULL | NULL   |      | BTREE      |
    | blog_blog |          0 | title              |            1 | title       | A         |           5 |     NULL | NULL   |      | BTREE      |
    | blog_blog |          1 | blog_blog_6f33f001 |            1 | category_id | A         |        NULL |     NULL | NULL   |      | BTREE      |
    | blog_blog |          1 | blog_blog_e969df21 |            1 | author_id   | A         |        NULL |     NULL | NULL   |      | BTREE      |
    +-----------+------------+--------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+

####创建索引
首先我们使用[代码](xxx)创建一个my_user表,表结构如下, 里面有10万条数据, 其中name是值是随机长度的  

    mysql> show create table my_user;
    +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Table   | Create Table                                                                                                                                                                    |
    +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | my_user | CREATE TABLE `my_user` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=MyISAM AUTO_INCREMENT=200001 DEFAULT CHARSET=utf8 |
    +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.02 sec)

my_user数据表相关的文件:  

    root@lzjun:/var/lib/mysql/django_blog# ll -h my_user.*
    -rw-rw---- 1 mysql mysql  8.4K  3月 13 15:11 my_user.frm
    -rw-rw---- 1 mysql mysql  2.5M  3月 13 15:17 my_user.MYD
    -rw-rw---- 1 mysql mysql 1005K  3月 13 15:17 my_user.MYI

在name没有创建索引时,查询一条数据的时间是:0.12s  

    mysql> select * from my_user where name like 'pkhavwcrybsjoimztnq';
    +--------+---------------------+
    | id     | name                |
    +--------+---------------------+
    | 100093 | pkhavwcrybsjoimztnq |
    +--------+---------------------+
    1 row in set (0.12 sec)

#####普通索引
1. 方式一:  

        CREATE INDEX index_name on TABLE_NAME(Column_name)
    
        mysql> create index i_name on my_user(name);
        Query OK, 100000 rows affected (0.84 sec)
        Records: 100000  Duplicates: 0  Warnings: 0

2. 方式二:  

        ALTER  TABLE  表名  ADD   [ UNIQUE | FULLTEXT | SPATIAL ]   INDEX  
        索引名（属性名  [ (长度) ]  [ ASC | DESC]）;
    
        mysql> alter table my_user add index i_name  (name);
        Query OK, 100000 rows affected (0.51 sec)
        Records: 100000  Duplicates: 0  Warnings: 0
3. 方式三:  
    直接在创建表的时候创建索引.  

        CREATE TABLE my_user2 (
                id int not null primary key auto_increment,
                name varchar(50),
                index iname (name));

创建索引后,相应的索引文件也增大了不少.  

#####唯一索引
普通索引允许被索引的列包含重复的值, 比如人的名字. 如果这列的值都是唯一的那么就可以使用唯一索引.他能改善查询的效率.另外一点是在有新数据插入的时候, 会自动检查新记录的字段的值是否已经存在了,如果存在MySQL会拒绝插入.因此很多场合,唯一索引的另一个目的是避免数据重复插入.  

    ALTER TABLE my_user ADD UNIQUE INDEX i_name (name);

或者是创建表的时候指定:  

    CREATE TABLE my_user(
        id int not null PRIMARY key AUTO_INCREMENT,
        name varchar(50),
        code varchar(50),
        UNIQUE KEY ui_name_code (name,code)
    )
主键与唯一索引的区别是:PRIMARY KEY is equivalent to UNIQUE NOT NULL,也就是说唯一索引的字段可以是重复的NULL.   

#### 前缀索引

```

mysql> create table SUser(
ID bigint unsigned primary key,
email varchar(64), 
... 
)engine=innodb; 


mysql> select f1, f2 from SUser where email='xxx';


mysql> alter table SUser add index index1(email);
或
mysql> alter table SUser add index index2(email(6));
```

- index2 这个索引结构只取email的前6个字节，所以占用空间会更小

```

select id,name,email from SUser where email='zhangssxyz@xxx.com';
```

- if use index1
  - 从 index1 索引树找到满足索引值是’zhangssxyz@xxx.com’的这条记录，取得 ID2 的值；
  - 到主键上查到主键值是 ID2 的行，判断 email 的值是正确的，将这行记录加入结果集；
  - 取 index1 索引树上刚刚查到的位置的下一条记录，发现已经不满足 email='zhangssxyz@xxx.com’的条件了，循环结束。
- if use index2 （email(6)结构
  - 从 index2 索引树找到满足索引值是’zhangs’的记录，找到的第一个是 ID1；
  - 到主键上查到主键值是 ID1 的行，判断出 email 的值不是’zhangssxyz@xxx.com’，这行记录丢弃；
  - 取 index2 上刚刚查到的位置的下一条记录，发现仍然是’zhangs’，取出 ID2，再到 ID 索引上取整行然后判断，这次值对了，将这行记录加入结果集；
  - 重复上一步，直到在 idxe2 上取到的值不是’zhangs’时，循环结束。

- 使用前缀索引后，可能会导致查询语句读数据的次数变多。

> 使用前缀索引，定义好长度，就可以做到既节省空间，又不用额外增加太多的查询成本。

##### 有什么方法能够确定我应该使用多长的前缀呢？

我们在建立索引时关注的是区分度，区分度越高越好。因为区分度越高，意味着重复的键值越少。因此，我们可以通过统计索引上有多少个不同的值来判断要使用多长的前缀。

```mysql
-- 计算列上的不同值
mysql> select count(distinct email) as L from SUser;

-- 一次使用不同长度的前缀来看这个值
mysql> select 
  count(distinct left(email,4)）as L4,
  count(distinct left(email,5)）as L5,
  count(distinct left(email,6)）as L6,
  count(distinct left(email,7)）as L7,
from SUser;

```

当然，使用前缀索引很可能会损失区分度，所以你需要预先设定一个可以接受的损失比例，比如 5%。然后，在返回的 L4~L7 中，找出不小于 L * 95% 的值，假设这里 L6、L7 都满足，你就可以选择前缀长度为 6。

##### 前缀索引对覆盖索引的影响

```mysql

select id,email from SUser where email='zhangssxyz@xxx.com';


select id,name,email from SUser where email='zhangssxyz@xxx.com';

-- 相比，这个语句只要求返回 id 和 email 字段。所以，如果使用 index1（即 email 整个字符串的索引结构）的话，可以利用覆盖索引，从 index1 查到结果后直接就返回了，不需要回到 ID 索引再去查一次。而如果使用 index2（即 email(6) 索引结构）的话，就不得不回到 ID 索引再去判断 email 字段的值。即使你将 index2 的定义修改为 email(18) 的前缀索引，这时候虽然 index2 已经包含了所有的信息，但 InnoDB 还是要回到 id 索引再查一下，因为系统并不确定前缀索引的定义是否截断了完整信息。也就是说，使用前缀索引就用不上覆盖索引对查询性能的优化了，这也是你在选择是否使用前缀索引时需要考虑的一个因素。

```

##### 其他索引

- 倒序存储

```mysql

mysql> select field_list from t where id_card = reverse('input_id_card_string');
```

- hash字段

```mysql

mysql> alter table t add id_card_crc int unsigned, add index(id_card_crc);
```

首先，它们的相同点是，都不支持范围查询。倒序存储的字段上创建的索引是按照倒序字符串的方式排序的，已经没有办法利用索引方式查出身份证号码在 [ID_X, ID_Y] 的所有市民了。同样地，hash 字段的方式也只能支持等值查询。

###### 区别

- 从占用的额外空间来看，倒序存储方式在主键索引上，不会消耗额外的存储空间，而 hash 字段方法需要增加一个字段。当然，倒序存储方式使用 4 个字节的前缀长度应该是不够的，如果再长一点，这个消耗跟额外这个 hash 字段也差不多抵消了。
- 在 CPU 消耗方面，倒序方式每次写和读的时候，都需要额外调用一次 reverse 函数，而 hash 字段的方式需要额外调用一次 crc32() 函数。如果只从这两个函数的计算复杂度来看的话，reverse 函数额外消耗的 CPU 资源会更小些。
- 从查询效率上看，使用 hash 字段方式的查询性能相对更稳定一些。因为 crc32 算出来的值虽然有冲突的概率，但是概率非常小，可以认为每次查询的平均扫描行数接近 1。而倒序存储方式毕竟还是用的前缀索引的方式，也就是说还是会增加扫描行数。

#### 字符串创建索引

1. 直接创建完整索引，这样可能比较占用空间；
2. 创建前缀索引，节省空间，但会增加查询扫描次数，并且不能使用覆盖索引；
3. 倒序存储，再创建前缀索引，用于绕过字符串本身前缀的区分度不够的问题；
4. 创建 hash 字段索引，查询性能稳定，有额外的存储和计算消耗，跟第三种方式一样，都不支持范围扫描。



####设计索引原则
1. 适合做索引的列一般是WHERE字句中出现的列,或者连接子句中的列,或者ORDERBY排序子句中.而不是要查询的列.   
