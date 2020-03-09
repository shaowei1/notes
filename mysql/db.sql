mysql -uroot -p -h 127.0.0.1
show databases;
use merchant;
select count(id) from shop_brand;
show create table shop_brand;


select count(distinct label) as L from tp_category_brand;
select count(distinct left(email,4)) as L4, count(distinct left(email,5)) as L5, count(distinct left(email,6)) as L6, count(distinct left(email,7)) as L7,from SUser;;

select label,distinct tp_category_id  from tp_category_brand group label;
select distinct (tp_category_id,label) from tp_category_brand where tp_id = 1000;
select distinct tp_category_id,label from tp_category_brand where tp_id = 1004;


SELECT distinct memo,name from xytest.student
where id in (select distinct min(id) from xytest.student group by memo)

-- 查询user表中，user_name字段值重复的数据及重复次数
select user_name,count(*) as count from user group by user_name having count>1;


-- INSERT INTO file
-- (width, height)
-- SELECT width, height
-- FROM image;

UPDATE file a
INNER JOIN image b ON a.id = b.id
SET a.width = b.width,
		a.height = b.height;
-- SET width = if(start_dts > end_dts, 'VALID', '')
-- where clause can go here
