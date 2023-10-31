
select  distinct(i_product_name)
 from item i1
 where i_manufact_id between 824 and 824+40 
   and (select count(*) as item_cnt
        from item
        where (i_manufact = i1.i_manufact and
        ((i_category = 'Women' and 
        (i_color = 'misty' or i_color = 'thistle') and 
        (i_units = 'Gram' or i_units = 'Tsp') and
        (i_size = 'economy' or i_size = 'medium')
        ) or
        (i_category = 'Women' and
        (i_color = 'ghost' or i_color = 'firebrick') and
        (i_units = 'Case' or i_units = 'Bundle') and
        (i_size = 'petite' or i_size = 'extra large')
        ) or
        (i_category = 'Men' and
        (i_color = 'blanched' or i_color = 'ivory') and
        (i_units = 'Cup' or i_units = 'Carton') and
        (i_size = 'N/A' or i_size = 'small')
        ) or
        (i_category = 'Men' and
        (i_color = 'red' or i_color = 'navajo') and
        (i_units = 'Bunch' or i_units = 'Tbl') and
        (i_size = 'economy' or i_size = 'medium')
        ))) or
       (i_manufact = i1.i_manufact and
        ((i_category = 'Women' and 
        (i_color = 'dark' or i_color = 'wheat') and 
        (i_units = 'Pallet' or i_units = 'Ounce') and
        (i_size = 'economy' or i_size = 'medium')
        ) or
        (i_category = 'Women' and
        (i_color = 'moccasin' or i_color = 'deep') and
        (i_units = 'Dram' or i_units = 'Box') and
        (i_size = 'petite' or i_size = 'extra large')
        ) or
        (i_category = 'Men' and
        (i_color = 'honeydew' or i_color = 'yellow') and
        (i_units = 'Ton' or i_units = 'Unknown') and
        (i_size = 'N/A' or i_size = 'small')
        ) or
        (i_category = 'Men' and
        (i_color = 'light' or i_color = 'bisque') and
        (i_units = 'Pound' or i_units = 'Lb') and
        (i_size = 'economy' or i_size = 'medium')
        )))) > 0
 order by i_product_name
 limit 100;


