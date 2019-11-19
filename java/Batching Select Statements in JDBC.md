JDBC批处理Select语句
====================
注：为了更好理解本文，请结合原文阅读  

在网络上开销最昂贵的资源就是客户端与服务器往返的请求与响应，JDBC中类似的一种情况就是对数据库的调用，如果你在做数据插入、更新、删除操作，你可以使用executeBatch()方法减少数据库调用次数，如：  

    Statement pstmt = conn.createStatement();
    pstmt.addBatch("insert into settings values(3,'liu')");
    pstmt.addBatch("insert into settings values(4,'zhi')");
    pstmt.addBatch("insert into settings values(5,'jun')");
    pstmt.executeBatch();

但不幸的是对于批量查询，JDBC并没有内建（built-in）的方法，而且JDBC执行批处理的时候也不能有SELECT语句，如：  

    Statement pstmt = conn.createStatement();
	pstmt.addBatch("select * from settings");
	pstmt.executeBatch();

会抛出异常：  

    Exception in thread "main" java.sql.BatchUpdateException: Can not issue SELECT via executeUpdate().
    	at com.mysql.jdbc.Statement.executeBatch(Statement.java:961)
    	at test.SelectBatchTest.test2(SelectBatchTest.java:49)
    	at test.SelectBatchTest.main(SelectBatchTest.java:12)

假设你想从一系列指定的id列表中获取名字，逻辑上，我们要做的事情看起来应该是：  

    PreparedStatement stmt = conn.prepareStatement(
        "select id, name from users where id in (?)");
    stmt.setString("1,2,3");

但是这样做并不能得到预期的结果，JDBC只允许你用单个的字面值来替换“？” JDBC之所以这么做是有必要的，因为如果SQL自身可以改变的话，JDBC驱动就没法预编译SQL语句了，另一方面它还能防止SQL注入攻击。  

但有四种可替代的实现方法可供选择：  

1. 分别对每个id做查询  
2. 一个查询做完所有事  
3. 使用存储过程  
4. 选择批处理 

#####方法一： 分别对每个id做查询

假设有100个id，那么就有100次数据库调用：  

    PreparedStatement stmt = conn.prepareStatement(
        "select id, name from users where id = ?");
    for ( int i=0; i < 100; i++ ) {
      stmt.setInt(i);  // or whatever values you are trying to query by

      // execute statement and get result
    }
这种方法写起来非常简单，但是性能非常慢，数据库往返要处理100次。  

#####方法二：一个查询完成所有事  

在运行时，你可以使用一个循环来构建如下SQL语句：  

    PreparedStatement stmt = conn.prepareStatement(
        "select id, name from users where id in (?, ?, ?)");
    stmt.setInt(1);
    stmt.setInt(2);
    stmt.setInt(3);

这种方案从代码相比第一种方法算是第二简单的，它解决了来回多次请求数据库的问题，但是如果每次请求参数的个数不一样时预处理语句就必须重新编译，由于每次SQL字面值不匹配，因此如果分别用10个id、3个id、100个，这样会在缓存中产生三个预处理语句。除了重新编译预处理语句之外，先前缓存池中的预处理语句将被移除（受限于缓存池大小），进而导致重新编译已编译过的语句。最后，这种查询方式在内存溢出或磁盘分页操作时查询会占用很长时间。  

该方案的另一种变体就是在SQL语句中硬编码：

    PreparedStatement stmt = conn.prepareStatement(
    "select id, name from users where id in (1, 2, 3)");

这样方式甚至更差，而且没有任何机会对SQL语句重用，至少用“？”还可以对使用相同数量参数的SQL语句进行重用。  

    PreparedStatement stmt = conn.prepareStatement(
       "select id, name from users where id in (?) ; "   
       + "select id, name from users where id in (?); "
       + "select id, name from users where id in (?)");
    stmt.setInt(1);
    stmt.setInt(2);
    stmt.setInt(3);

这种方法的优点就是每次查询模版语句都一样，数据库不需要每次计算执行路径。然而，从数据库驱动的角度来说SQL每次都不一样，预处理语句每次必须预处理保存在缓存中。而且不是所有数据库系统都支持分号间隔的多个SQL语句的  

#####方法三：使用存储过程  
存储过程执行在数据库系统中，因此它可以做很多查询而不需要太多网络负载，存储过程可以收集所有结果一次性返回。这是一种速度很快的解决方案。但是它对数据库的依赖比较强，不能随意的切换数据库系统，否则需要重写存储过程而且需要你分离应用服务器与数据库服务器之间的逻辑。如果应用架构已经使用了存储过程，无疑这是只最佳方案。  

#####方法四：批量查询

批量查询是方案一和方案二的折衷选择，它预先确定一批查询参数的常量，然后用这些参数构建一批查询。因为这只会涉及到有限个查询，所以它有预处理语句的优势（预编译不会与缓存中的预处理发生碰撞）。批处理多个值在相同的查询保留了服务器来回请求最小化的优势。最后你可以通过控制批处理的上限来避免大查询的内存问题。如果你有很关键的查询对性能方面有要求又不想用存储过程，那么这是一种很好的解决办法，现在我们通过一个例子说明：  

    public static final int SINGLE_BATCH = 1;
    public static final int SMALL_BATCH = 4;
    public static final int MEDIUM_BATCH = 11;
    public static final int LARGE_BATCH = 51;

第一件要做的事是你要衡量有多少批处理以及每个批处理的大小。（注意：在真实的代码中，这些值应该写在一个配置文件中而不是采取硬编码的形式，也就是说，你可以在运行时试验并改变批处理的大小）不管真正的批处理大小是多大，你总需要一个单个的批处理---大小为1的批处理（SINGLE_BATTCH）。这样如果有人请求的就是一个值或者在一个很大的查询中最后有遗留下来的单个值都能派上用场。对于批处理的大小，使用素数会更好些。换句话说，大小不应该可以相互的整除或者被相同的数整除。请求数的最大值将有最少的服务器往返。批处理的大小的数量和真正的大小是基于配置变化的。需要注意的是：大的批处理大小不应该太大否则你将遇到内存麻烦。同时最小批处理的大小应该很小，你可能会使用这个来做很多次的查询。  

    while ( totalNumberOfValuesLeftToBatch > 0 ) {

按如下方式重复操作直到推出循环。  

    int batchSize = SINGLE_BATCH;
    if ( totalNumberOfValuesLeftToBatch >= LARGE_BATCH ) {
      batchSize = LARGE_BATCH;
    } else if ( totalNumberOfValuesLeftToBatch >= MEDIUM_BATCH ) {
      batchSize = MEDIUM_BATCH;
    } else if ( totalNumberOfValuesLeftToBatch >= SMALL_BATCH ) {
      batchSize = SMALL_BATCH;
    }
    totalNumberOfValuesLeftToBatch -= batchSize; 

这种方案在这里是查找到最大的批处理大小，可能这个最大值比我们实际要查询的值稍大。举例说明：假设查询有75个参数，那么首先选择51个元素（LARGE_BATCH），现在还剩24个待查询，然后接着用11个元素的查询（MEDIUM_BATCH）。现在还有13个值，因为仍然大于11，再做一次11个元素的查询，现在只剩下2个值，它少于那个最小的批处理4（SMALL_BATCH），所以做两次单查询。总共5次往返用了3次预处理在缓存中。这是一个很重要的改进比单独地坐75次单查询。  


    StringBuilder inClause = new StringBuilder();
    boolean firstValue = true;
    for (int i=0; i < batchSize; i++) {
      inClause.append('?');
      if ( firstValue ) {
        firstValue = false;
      } else {
        inClause.append(',');
      }
    }
    PreparedStatement stmt = conn.prepareStatement(
        "select id, name from users where id in (" + inClause.toString() + ')');

现在已经构建了一个真实的预处理语句，由于一直用相同的方式构建的查询，驱动注意到SQL是相同的。（注意：如果你还没有用Java5，使用StringBuffer替换StringBuilder才能正常编译），返回id很重要这样有利于查找哪个名字对应哪个id。  

    for (int i=0; i < batchSize; i++) {
      stmt.setInt(i);  // or whatever values you are trying to query by
    }

设置合适的值数量去查询，包括其他搜索条件查询。仅仅只要把这些参数在之举参数之后。在这种情况你可以最终当前的索引。  

从这点来看，你仅仅只是执行查询返回了结果，在第一次尝试的时候，你应该关注一下性能的提升，根据具体情况调整优化批处理的大小（batch size）。  

*正如那句名言所说：“过早的优化是万恶之源”，批处理应该是用于解决性能问题。*

原文：[Batching Select Statements in JDBC](http://www.javaranch.com/journal/200510/Journal200510.jsp#a2)
