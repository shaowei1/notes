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

-- 查询json
-- SELECT json_extract(字段名,'$.json结构') FROM 表名;
-- 如果json里有双引号，那这样取出来的数据也带双引号，要去掉就使用REPLACE函数
-- ps_push_data表里的push_data字段存的数据为：{"carRenewalInfoVo":{"licence":"浙AF55Z0"},"code":"1","msg":"成功"}
SELECT REPLACE(json_extract(push_data,'$.carRenewalInfoVo.licence'),'"','') FROM ps_push_data;
-- SELECT * FROM table WHERE JSON_EXTRACT(request_content, "$.Content") = '1'
-- 说明：JSON_EXTRACT(列名,"$.json某个属性")

SELECT * FROM devices WHERE json_extract(json_extract(json_extract(json_data,"$.lastOperation"),"$.target"),"$.name") = '西门门岗闸机01'


-- 先分组 再排序
SELECT a.* from product_publishing a
            left JOIN product_publishing b
            on a.product_id = b.product_id and a.created_at < b.created_at
WHERE b.created_at is null;

-- 更新 from select
UPDATE product as p , (SELECT a.* from product_publishing a
            left JOIN product_publishing b
            on a.product_id = b.product_id and a.created_at < b.created_at
WHERE b.created_at is null) as k set p.latest_publish_status = k.`status` WHERE p.id = k.product_id;
